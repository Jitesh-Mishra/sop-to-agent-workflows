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

    def chat(self, messages: list[dict]) -> tuple[str, dict]:
        raise NotImplementedError


class LlamaCppBackend(Backend):
    def __init__(self, repo: str, filename: str, n_ctx: int = 8192, threads: int | None = None, max_tokens: int = 1800):
        from huggingface_hub import hf_hub_download
        from llama_cpp import Llama
        self.name = f"{repo}/{filename}"
        self.llm = Llama(model_path=hf_hub_download(repo, filename), n_ctx=n_ctx,
                         n_threads=threads or os.cpu_count(), verbose=False, seed=0)
        self.max_tokens = max_tokens

    def chat(self, messages):
        t = time.time()
        r = self.llm.create_chat_completion(messages=messages, temperature=0.0, max_tokens=self.max_tokens,
                                            response_format={"type": "json_object", "schema": SCHEMA})
        return r["choices"][0]["message"]["content"], {**r["usage"], "seconds": round(time.time() - t, 2)}


class GroqBackend(Backend):
    """Optional: set GROQ_API_KEY. Not used for the reported numbers."""
    def __init__(self, model: str = "llama-3.3-70b-versatile"):
        import httpx
        self.name, self.http, self.key = f"groq/{model}", httpx.Client(timeout=120), os.environ["GROQ_API_KEY"]
        self.model = model

    def chat(self, messages):
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

    def chat(self, messages):
        self.calls.append(messages)
        return self.replies.pop(0), {"seconds": 0.0}


@dataclass
class Attempt:
    raw: str
    errors: list[str]
    usage: dict


@dataclass
class CompileResult:
    spec: WorkflowSpec | None
    attempts: list[Attempt] = field(default_factory=list)

    @property
    def valid_first(self) -> bool:
        return not self.attempts[0].errors

    @property
    def valid_final(self) -> bool:
        return not self.attempts[-1].errors


def parse(raw: str) -> tuple[WorkflowSpec | None, list[str]]:
    try:
        return WorkflowSpec.model_validate(json.loads(raw)), []
    except Exception as e:  # malformed JSON or wrong shape
        return None, [f"The output is not valid workflow JSON ({type(e).__name__}). Return only the JSON object."]


def compile_sop(sop: SOP, backend: Backend, version: str = "v2", max_repairs: int = 2) -> CompileResult:
    messages = [{"role": "system", "content": system_prompt(version)}, {"role": "user", "content": user_prompt(sop)}]
    res = CompileResult(spec=None)
    for attempt in range(max_repairs + 1):
        raw, usage = backend.chat(messages)
        spec, errs = parse(raw)
        if spec is not None:
            errs = validate(spec, len(sop.lines))
        res.attempts.append(Attempt(raw, errs, usage))
        if spec is not None:
            res.spec = spec  # keep the latest parsable spec even if it still has errors
        if not errs:
            break
        messages = messages[:2] + [{"role": "assistant", "content": raw}, {"role": "user", "content": repair_prompt(raw, errs)}]
    return res
