"""Hand-written graph algorithms over a WorkflowSpec: cycle detection, topological sort, reachability,
and the run-time frontier used by the runtime. No graph library on purpose."""
from __future__ import annotations

from collections import defaultdict, deque


def adjacency(step_ids, edges):
    out, inn = defaultdict(list), defaultdict(list)
    for a, b in edges:
        out[a].append(b)
        inn[b].append(a)
    return out, inn


def topo_sort(step_ids: list[str], edges: list[tuple[str, str]]) -> list[str] | None:
    """Kahn's algorithm. Returns an order, or None if the graph has a cycle. Ties broken by declaration order."""
    rank = {s: i for i, s in enumerate(step_ids)}
    out, _ = adjacency(step_ids, edges)
    indeg = {s: 0 for s in step_ids}
    for _, b in edges:
        indeg[b] += 1
    ready = sorted([s for s in step_ids if indeg[s] == 0], key=rank.get)
    order = []
    while ready:
        s = ready.pop(0)
        order.append(s)
        for b in out[s]:
            indeg[b] -= 1
            if indeg[b] == 0:
                ready.append(b)
                ready.sort(key=rank.get)
    return order if len(order) == len(step_ids) else None


def find_cycle(step_ids: list[str], edges: list[tuple[str, str]]) -> list[str] | None:
    """Iterative DFS with three colours; returns one cycle as a node list, or None."""
    out, _ = adjacency(step_ids, edges)
    WHITE, GREY, BLACK = 0, 1, 2
    colour = {s: WHITE for s in step_ids}
    parent = {}
    for root in step_ids:
        if colour[root] != WHITE:
            continue
        stack = [(root, iter(out[root]))]
        colour[root] = GREY
        while stack:
            node, it = stack[-1]
            nxt = next(it, None)
            if nxt is None:
                colour[node] = BLACK
                stack.pop()
            elif colour.get(nxt, WHITE) == GREY:
                cyc, cur = [nxt], node
                while cur != nxt:
                    cyc.append(cur)
                    cur = parent[cur]
                return list(reversed(cyc))
            elif colour.get(nxt, WHITE) == WHITE:
                parent[nxt] = node
                colour[nxt] = GREY
                stack.append((nxt, iter(out[nxt])))
    return None


def reachable(starts, edges) -> set[str]:
    out = defaultdict(list)
    for a, b in edges:
        out[a].append(b)
    seen, q = set(starts), deque(starts)
    while q:
        for b in out[q.popleft()]:
            if b not in seen:
                seen.add(b)
                q.append(b)
    return seen


def frontier(step_ids, edges, done: set[str], taken: set[tuple[str, str]]) -> list[str]:
    """Steps ready to run. A step is ACTIVE if it has no predecessors or some incoming edge was taken.
    It is DEAD if every predecessor is finished (done or dead) and none of them took the edge to it.
    It is READY if active, not done, and every predecessor is finished (OR-join over the live branches)."""
    order = topo_sort(step_ids, edges)
    _, inn = adjacency(step_ids, edges)
    dead: set[str] = set()
    ready = []
    for s in order:
        preds = inn[s]
        finished = all(p in done or p in dead for p in preds)
        active = not preds or any((p, s) in taken for p in preds)
        if s in done:
            continue
        if preds and finished and not active:
            dead.add(s)
        elif active and finished:
            ready.append(s)
    return ready
