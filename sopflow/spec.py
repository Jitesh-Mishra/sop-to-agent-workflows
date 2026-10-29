"""SOP documents and the typed workflow spec the compiler produces."""
from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

from pydantic import BaseModel, Field

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"


class Step(BaseModel):
    id: str
    lines: list[int] = Field(description="1-based SOP line numbers that state this step")
    action: str
    role: str = Field(description="who performs the step")
    handoff_to: Optional[str] = Field(None, description="party that receives work, information or a decision; null if none")


class Edge(BaseModel):
    model_config = {"populate_by_name": True}
    from_: str = Field(alias="from")
    to: str
    condition: Optional[str] = None


class WorkflowSpec(BaseModel):
    steps: list[Step]
    edges: list[Edge] = []

    def dump(self) -> dict:
        return {"steps": [s.model_dump() for s in self.steps],
                "edges": [e.model_dump(by_alias=True) for e in self.edges]}


@dataclass
class SOP:
    id: str
    title: str
    source: str
    lines: list[str]

    def numbered(self) -> str:
        return "\n".join(f"L{i}: {t}" for i, t in enumerate(self.lines, 1))


def load_sop(sop_id: str, root: Path = DATA) -> SOP:
    text = (root / "sops" / f"{sop_id}.md").read_text()
    head, body = text.split("\n---\n", 1)
    title = head.splitlines()[0].lstrip("# ").strip()
    source = next((l.split(":", 1)[1].strip() for l in head.splitlines() if l.startswith("source:")), "")
    return SOP(sop_id, title, source, [l.strip() for l in body.splitlines() if l.strip()])


def load_gold(sop_id: str, root: Path = DATA) -> WorkflowSpec:
    return WorkflowSpec.model_validate(json.loads((root / "gold" / f"{sop_id}.json").read_text()))


def split(name: str, root: Path = DATA) -> list[str]:
    return json.loads((root / "splits.json").read_text())[name]


def all_ids(root: Path = DATA) -> list[str]:
    return sorted(p.stem for p in (root / "sops").glob("*.md"))
