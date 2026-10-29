"""Architecture diagram for the README, light + dark.   python scripts/make_diagrams.py -> docs/img/architecture-{light,dark}.svg"""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "docs" / "img"

THEMES = {
    "light": dict(bg="#ffffff", card="#f6f8fa", border="#d0d7de", ink="#1f2328", ink2="#59636e", faint="#e6e9ed",
                  a="#2a78d6", a_soft="#e3eefb", b="#eb6834", b_soft="#fde8de", c="#1baf7a", c_soft="#dcf4ea",
                  muted="#afb8c1"),
    "dark": dict(bg="#0d1117", card="#161b22", border="#30363d", ink="#e6edf3", ink2="#9198a1", faint="#21262d",
                 a="#3987e5", a_soft="#13263d", b="#d95926", b_soft="#3a1d12", c="#199e70", c_soft="#0f2e23",
                 muted="#484f58"),
}
FONT = "-apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif"
MONO = "ui-monospace, SFMono-Regular, Menlo, Consolas, monospace"


def esc(s):
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


class SVG:
    def __init__(self, w, h, t, label):
        self.w, self.h, self.t, self.label, self.parts = w, h, t, label, []

    def add(self, s):
        self.parts.append(s)

    def text(self, x, y, s, size=13, color=None, weight=400, anchor="start", mono=False, italic=False):
        self.add(f'<text x="{x}" y="{y}" font-family="{MONO if mono else FONT}" font-size="{size}" '
                 f'font-weight="{weight}" fill="{color or self.t["ink"]}" text-anchor="{anchor}"'
                 f'{" font-style=\"italic\"" if italic else ""}>{esc(s)}</text>')

    def rect(self, x, y, w, h, fill, stroke=None, rx=10, dash=None, sw=1.5):
        d = f' stroke-dasharray="{dash}"' if dash else ""
        self.add(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}" '
                 f'stroke="{stroke or "none"}" stroke-width="{sw}"{d}/>')

    def line(self, x1, y1, x2, y2, color=None, sw=1.5, dash=None, arrow=False, marker="ar"):
        d = f' stroke-dasharray="{dash}"' if dash else ""
        m = f' marker-end="url(#{marker})"' if arrow else ""
        self.add(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{color or self.t["ink2"]}" '
                 f'stroke-width="{sw}" stroke-linecap="round"{d}{m}/>')

    def path(self, d, color=None, sw=1.5, dash=None, arrow=False, marker="ar"):
        da = f' stroke-dasharray="{dash}"' if dash else ""
        m = f' marker-end="url(#{marker})"' if arrow else ""
        self.add(f'<path d="{d}" fill="none" stroke="{color or self.t["ink2"]}" stroke-width="{sw}" '
                 f'stroke-linecap="round" stroke-linejoin="round"{da}{m}/>')

    def circle(self, x, y, r, fill, stroke=None, sw=1.5):
        self.add(f'<circle cx="{x}" cy="{y}" r="{r}" fill="{fill}" stroke="{stroke or "none"}" stroke-width="{sw}"/>')

    def pill(self, x, y, s, fill, color, size=11.5, anchor="middle", pad=9):
        w = len(s) * size * 0.58 + 2 * pad
        x0 = x - w / 2 if anchor == "middle" else x
        self.rect(x0, y - size - 3, w, size + 10, fill, rx=(size + 10) / 2)
        self.text(x0 + w / 2, y + 1, s, size=size, color=color, weight=600, anchor="middle")

    def node(self, x, y, w, h, title, sub=None, accent=None, dash=None, mono_title=True):
        t = self.t
        fill = t[f"{accent}_soft"] if accent else t["card"]
        stroke = t[accent] if accent else t["border"]
        self.rect(x, y, w, h, fill, stroke, dash=dash)
        cy = y + h / 2 + (-4 if sub else 5)
        self.text(x + w / 2, cy, title, size=14, weight=650, anchor="middle", mono=mono_title)
        if sub:
            for i, s in enumerate(sub if isinstance(sub, list) else [sub]):
                self.text(x + w / 2, cy + 19 + i * 16, s, size=12, color=t["ink2"], anchor="middle")

    def render(self):
        t = self.t
        defs = (f'<defs>'
                f'<marker id="ar" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">'
                f'<path d="M0,0 L10,5 L0,10 z" fill="{t["ink2"]}"/></marker>'
                f'<marker id="ara" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">'
                f'<path d="M0,0 L10,5 L0,10 z" fill="{t["a"]}"/></marker>'
                f'<marker id="arb" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">'
                f'<path d="M0,0 L10,5 L0,10 z" fill="{t["b"]}"/></marker></defs>')
        return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {self.w} {self.h}" width="{self.w}" '
                f'height="{self.h}" role="img" aria-label="{esc(self.label)}">{defs}'
                f'<rect width="{self.w}" height="{self.h}" rx="14" fill="{t["bg"]}" stroke="{t["border"]}"/>'
                + "".join(self.parts) + "</svg>")


def header(s, title, sub):
    s.text(32, 42, title, size=19, weight=700)
    s.text(32, 64, sub, size=13, color=s.t["ink2"])


def architecture(t):
    s = SVG(1080, 640, t, "SOP text is compiled by an LLM into a typed workflow spec, checked by a hand-written validator with a "
                          "repair loop, scored against gold labels, and executed by a LangGraph runtime with SQLite checkpoints, "
                          "exposed through MCP, REST and a CLI.")
    header(s, "SOP in, validated agent workflow out",
           "Compile, validate and repair, then run with checkpoints. Every claim is scored against gold labels.")
    # left: inputs
    s.node(28, 110, 190, 96, "38 SOPs", ["18 in 5 Oracle-mapped families", "20 out-of-domain"], mono_title=False)
    s.node(28, 236, 190, 78, "gold labels", ["steps, edges, handoffs,", "agent vs human"], accent="c")
    # compile lane
    s.rect(248, 92, 520, 250, t["card"], t["border"], rx=14)
    s.text(264, 118, "COMPILE", size=11, weight=700, color=t["ink2"])
    s.node(268, 132, 150, 92, "compiler.py", ["Qwen2.5 GGUF (CI)", "JSON-schema output"], accent="a")
    s.node(440, 132, 150, 92, "validator.py", ["cycles, dangling edges,", "bad lines, no owner"])
    s.node(612, 132, 140, 92, "WorkflowSpec", ["steps, edges,", "handoffs, executor"], mono_title=False)
    s.line(218, 158, 264, 170, arrow=True)
    s.line(418, 178, 436, 178, arrow=True)
    s.line(590, 178, 608, 178, arrow=True)
    s.path("M515,224 C515,262 343,262 343,228", color=t["b"], dash="5 4", arrow=True, marker="arb")
    s.text(429, 270, "repair loop: errors fed back (2x max)", size=11.5, color=t["b"], anchor="middle")
    s.node(268, 286, 150, 44, "rule baseline", None, mono_title=False)
    s.node(440, 286, 312, 44, "score.py: F1 + agent/human accuracy", None, mono_title=False)
    s.path("M123,314 L123,336 L596,336 L596,333", color=t["c"], dash="4 4", arrow=True)
    s.line(418, 308, 436, 308, arrow=True)
    # run lane
    s.rect(248, 360, 520, 256, t["a_soft"], t["a"], rx=14, sw=2)
    s.text(264, 386, "RUN", size=11, weight=700, color=t["a"])
    s.node(268, 400, 230, 100, "runtime.py (LangGraph)", ["plan -> execute loop, 1 step per", "checkpoint; human steps interrupt()"])
    s.node(518, 400, 230, 100, "SQLite", ["checkpoints (durability=sync)", "idempotent side-effect ledger"], mono_title=False)
    s.line(498, 450, 514, 450, arrow=True)
    s.node(268, 520, 480, 76, "context packet at every handoff", ["instructions, deadline, completed steps + outputs, open decisions"], mono_title=False)
    s.path("M682,224 L682,350 L383,350 L383,396", color=t["a"], arrow=True, marker="ara")
    # right: interfaces + evidence
    s.node(800, 110, 252, 86, "mcp_server.py", ["start_workflow, get_state,", "complete_step, request_handoff"], accent="a")
    s.node(800, 214, 252, 66, "FastAPI + Typer CLI", ["same WorkflowService"], mono_title=False)
    s.path("M768,430 C786,430 780,153 796,153", color=t["a"], arrow=True, marker="ara")
    s.rect(800, 300, 252, 316, t["card"], t["border"], rx=12)
    s.text(926, 328, "Evidence (reports/)", size=13, weight=700, anchor="middle")
    for i, (a, b) in enumerate([("results.csv", "LLM vs rules, dev/test/ood"), ("crash_resume.csv", "hard kills, N/N resumed"),
                                ("opportunity.csv", "agent vs human, SIMULATED time"), ("runbooks/", "Mermaid per SOP"),
                                ("final_test_runs", "test split run once")]):
        y = 352 + i * 52
        s.text(820, y, a, size=12.5, weight=650, mono=True)
        s.text(820, y + 18, b, size=11.5, color=t["ink2"])
    return s.render()


if __name__ == "__main__":
    OUT.mkdir(parents=True, exist_ok=True)
    for name, t in THEMES.items():
        (OUT / f"architecture-{name}.svg").write_text(architecture(t))
    print("ok")
