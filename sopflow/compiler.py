"""SOP text -> WorkflowSpec with an LLM, plus a validator-driven repair loop.

Backends: llama.cpp (local GGUF, used in CI), Groq (optional, key from env), and a scripted fake for tests.
Output is constrained by a JSON schema (llama.cpp grammar), so parse failures are rare; structural errors
(bad line numbers, dangling edges, cycles) are what the validator and the repair loop handle."""
from __future__ import annotations

import json
import os
import time
from dataclasses import dataclass, field
from pathlib import Path

from .postprocess import autofix as _autofix
from .spec import SOP, WorkflowSpec
from .validator import validate

PROMPTS = Path(__file__).parent / "prompts"
SCHEMA = {
    "type": "object",
    "properties": {
        "steps": {"type": "array", "items": {"type": "object", "properties": {
            "id": {"type": "string"}, "lines": {"type": "array", "items": {"type": "integer"}},
            "action": {"type": "string"}, "role": {"type": "string"},
            "handoff_to": {"type": ["string", "null"]},
            "executor": {"type": "string", "enum": ["agent", "human"]}, "executor_reason": {"type": "string"}},
            "required": ["id", "lines", "action", "role", "handoff_to", "executor", "executor_reason"]}},
        "edges": {"type": "array", "items": {"type": "object", "properties": {
            "from": {"type": "string"}, "to": {"type": "string"}, "condition": {"type": ["string", "null"]}},
            "required": ["from", "to", "condition"]}},
    },
    "required": ["steps", "edges"],
}


EXECUTOR_SCHEMA = {"type": "object", "properties": {"executor": {"type": "string", "enum": ["agent", "human"]},
                                                    "executor_reason": {"type": "string"}},
                   "required": ["executor", "executor_reason"]}


def system_prompt(version: str) -> str:
    return (PROMPTS / f"{version}_system.txt").read_text()


def user_prompt(sop: SOP) -> str:
    return f"SOP: {sop.title}\n{sop.numbered()}\n\nReturn the workflow JSON."


def repair_prompt(prev: str, errors: list[str]) -> str:
    return ("Your workflow JSON has these problems:\n- " + "\n- ".join(errors) +
            "\n\nReturn the corrected workflow JSON for the same SOP. Fix every problem and keep everything else.\n"
            f"Previous JSON:\n{prev}")


class Backend:
    name = "base"

    def chat(self, messages: list[dict], schema: dict = SCHEMA, max_tokens: int | None = None) -> tuple[str, dict]:
        raise NotImplementedError


class LlamaCppBackend(Backend):
    def __init__(self, repo: str, filename: str, n_ctx: int = 8192, threads: int | None = None, max_tokens: int = 1800):
        from huggingface_hub import hf_hub_download
        from llama_cpp import Llama
        self.name = f"{repo}/{filename}"
        self.llm = Llama(model_path=hf_hub_download(repo, filename), n_ctx=n_ctx,
                         n_threads=threads or os.cpu_count(), verbose=False, seed=0)
        self.max_tokens = max_tokens

    def chat(self, messages, schema=SCHEMA, max_tokens=None):
        t = time.time()
        r = self.llm.create_chat_completion(messages=messages, temperature=0.0, max_tokens=max_tokens or self.max_tokens,
                                            response_format={"type": "json_object", "schema": schema})
        return r["choices"][0]["message"]["content"], {**r["usage"], "seconds": round(time.time() - t, 2)}


class GroqBackend(Backend):
    """Optional: set GROQ_API_KEY. Not used for the reported numbers."""
    def __init__(self, model: str = "llama-3.3-70b-versatile"):
        import httpx
        self.name, self.http, self.key = f"groq/{model}", httpx.Client(timeout=120), os.environ["GROQ_API_KEY"]
        self.model = model

    def chat(self, messages, schema=SCHEMA, max_tokens=None):
        t = time.time()
        r = self.http.post("https://api.groq.com/openai/v1/chat/completions",
                           headers={"Authorization": f"Bearer {self.key}"},
                           json={"model": self.model, "messages": messages, "temperature": 0,
                                 "response_format": {"type": "json_object"}}).json()
        return r["choices"][0]["message"]["content"], {**r.get("usage", {}), "seconds": round(time.time() - t, 2)}


class FakeBackend(Backend):
    """Replays scripted replies; used by tests."""
    name = "fake"

    def __init__(self, replies: list[str]):
        self.replies = list(replies)
        self.calls: list[list[dict]] = []

    def chat(self, messages, schema=SCHEMA, max_tokens=None):
        self.calls.append(messages)
        return self.replies.pop(0), {"seconds": 0.0}


@dataclass
class Attempt:
    raw: str
    errors: list[str]                    # validator errors on the raw LLM output
    usage: dict
    fixes: list[str] = field(default_factory=list)       # deterministic autofix changes
    remaining: list[str] = field(default_factory=list)   # validator errors after autofix


@dataclass
class CompileResult:
    spec: WorkflowSpec | None
    attempts: list[Attempt] = field(default_factory=list)
    executor_calls: list[dict] = field(default_factory=list)
    inline_executor: dict = field(default_factory=dict)

    @property
    def valid_first(self) -> bool:
        """Raw first LLM output passes the validator (no autofix, no repair)."""
        return not self.attempts[0].errors

    @property
    def valid_final(self) -> bool:
        return not self.attempts[-1].remaining


def parse(raw: str) -> tuple[WorkflowSpec | None, list[str]]:
    try:
        return WorkflowSpec.model_validate(json.loads(raw)), []
    except Exception as e:  # malformed JSON or wrong shape
        return None, [f"The output is not valid workflow JSON ({type(e).__name__}). Return only the JSON object."]


EXECUTOR_PROMPT = """Decide who should carry out ONE step of a standard operating procedure in an AI-assisted workflow.

"human" if the step needs physical action or presence, a signature, attestation or certification, a professional, clinical, legal or accountable judgment or decision (approve, deny, determine, accept, adjudicate), a conversation such as an interview or counseling, or is done by an outside party (customer, enrollee, contractor, applicant, regulator).
"agent" if it is information work an AI agent with system access could do: drafting and sending a notice from known facts, compiling, checking or forwarding documents, recording, logging or tracking, searching and correlating information, classifying or routing.

Examples:
Step: Wipe the laptop | Role: IT | Source: IT shall wipe the laptop. -> {"executor": "human", "executor_reason": "Needs hands-on access to the device."}
Step: Notify the asset manager of damage | Role: IT | Source: If the laptop is damaged, IT shall notify the asset manager. -> {"executor": "agent", "executor_reason": "Sending a notice from facts already in the ticket."}
Step: Approve the refund | Role: finance manager | Source: The finance manager shall approve or deny the refund. -> {"executor": "human", "executor_reason": "An accountable approval decision."}
Step: Log the return in the asset register | Role: IT | Source: IT shall record the return in the asset register. -> {"executor": "agent", "executor_reason": "Routine record keeping."}
Return only the JSON object."""


def executor_pass(spec: WorkflowSpec, sop: SOP, backend: Backend) -> tuple[WorkflowSpec, list[dict]]:
    """Second, focused LLM pass: one short classification per step (small models do better on one question)."""
    calls, steps = [], []
    for s in spec.steps:
        src = " ".join(sop.lines[i - 1] for i in s.lines if 1 <= i <= len(sop.lines))
        msg = [{"role": "system", "content": EXECUTOR_PROMPT},
               {"role": "user", "content": f"Step: {s.action} | Role: {s.role} | Source: {src}"}]
        raw, usage = backend.chat(msg, schema=EXECUTOR_SCHEMA, max_tokens=120)
        try:
            d = json.loads(raw)
            upd = {"executor": d["executor"], "executor_reason": d.get("executor_reason", "")}
        except Exception:
            upd = {}
        calls.append({"step_id": s.id, "raw": raw, "usage": usage})
        steps.append(s.model_copy(update=upd))
    return spec.model_copy(update={"steps": steps}), calls


def compile_sop(sop: SOP, backend: Backend, version: str = "v2", max_repairs: int = 2,
                autofix: bool = True, two_pass_executor: bool = False) -> CompileResult:
    """version v3 = prompt v2 + deterministic autofix + LLM repair for what remains + executor pass."""
    prompt = "v2" if version == "v3" else version
    if version == "v3":
        autofix, two_pass_executor = True, True
    messages = [{"role": "system", "content": system_prompt(prompt)}, {"role": "user", "content": user_prompt(sop)}]
    res = CompileResult(spec=None)
    for attempt in range(max_repairs + 1):
        raw, usage = backend.chat(messages)
        spec, errs = parse(raw)
        if spec is not None:
            errs = validate(spec, len(sop.lines))
        fixes, remaining = [], errs
        if spec is not None and autofix and errs:
            spec, fixes = _autofix(spec, sop)
            remaining = validate(spec, len(sop.lines))
        res.attempts.append(Attempt(raw, errs, usage, fixes, remaining))
        if spec is not None:
            res.spec = spec  # keep the latest parsable spec even if it still has errors
        if not remaining:
            break
        messages = messages[:2] + [{"role": "assistant", "content": raw}, {"role": "user", "content": repair_prompt(raw, remaining)}]
    if res.spec is not None and two_pass_executor:
        res.inline_executor = {s.id: s.executor for s in res.spec.steps}
        res.spec, res.executor_calls = executor_pass(res.spec, sop, backend)
    return res
