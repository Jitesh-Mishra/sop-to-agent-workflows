"""Rule baseline: numbered or modal/imperative lines become steps, edges are linear in reading order,
and notify/report/submit-style verbs mark a handoff."""
from __future__ import annotations

import re

from .spec import SOP, Edge, Step, WorkflowSpec

MODAL = re.compile(r"\b(shall|must|should|is to|are to)\b", re.I)
NUMBERED = re.compile(r"^\(\d+\)")
IMPERATIVE = {"put", "cover", "wet", "rub", "continue", "rinse", "dry", "use", "remove", "fasten", "fit", "place", "secure",
              "slide", "pull", "grasp", "wash", "check", "verify", "notify", "close", "inhale", "exhale", "document",
              "identify", "prepare", "secure", "coordinate", "submit", "lock", "de-activate", "ensure", "carefully", "then"}
SKIP = re.compile(r"^(note|caution)\b|is considered|not substitutes|need not|do not have to|may not exceed|"
                  r"the type of|this procedure establishes|is preferred|is now locked out", re.I)
HANDOFF = re.compile(r"\b(notify|notif\w*|report|submit|forward|inform\w*|refer|furnish|advise|consult|appeal|"
                     r"provide (?:the )?(?:\w+ )?(?:notice|notification|copy)|made available to|give)\b", re.I)
AGENT_VERBS = re.compile(r"\b(notify|notif\w*|report|submit|forward|send|record|retain|document|annotate|track|"
                         r"monitor|provide (?:the )?(?:\w+ )?(?:notice|notification|copy)|issue|inform|log|maintain)\b", re.I)
ROLE = re.compile(r"^(?:\(\d+\)\s*)?(?:the |each |an? )?([A-Za-z ,'-]{3,60}?)\s+(?:shall|must|should|may|will)\b", re.I)
TO = re.compile(r"\bto (?:the |each )?([A-Z][\w .'-]{2,60}?|all affected employees|affected employees|the contractor)"
                r"(?=[,.;]| within| by| of| that|$)")


def _first_word(line: str) -> str:
    body = line.split(":", 1)[1] if ":" in line[:40] else line
    body = NUMBERED.sub("", body.strip()).strip()
    return body.split(" ", 1)[0].lower().strip(",.") if body else ""


def is_step(line: str) -> bool:
    if SKIP.search(line):
        return False
    return bool(NUMBERED.match(line) or MODAL.search(line) or _first_word(line) in IMPERATIVE)


def extract(sop: SOP) -> WorkflowSpec:
    steps = []
    for i, line in enumerate(sop.lines, 1):
        if not is_step(line):
            continue
        m = ROLE.match(line)
        role = m.group(1).strip() if m else "unspecified"
        handoff = None
        if HANDOFF.search(line):
            t = TO.search(line)
            handoff = t.group(1).strip() if t else "another party"
            if handoff.lower() == role.lower():
                handoff = "another party"
        executor = "agent" if AGENT_VERBS.search(line) else "human"
        steps.append(Step(id=f"s{len(steps) + 1}", lines=[i], action=line[:120], role=role, handoff_to=handoff,
                          executor=executor, executor_reason="keyword rule"))
    edges = [Edge(**{"from": a.id, "to": b.id}) for a, b in zip(steps, steps[1:])]
    return WorkflowSpec(steps=steps, edges=edges)
