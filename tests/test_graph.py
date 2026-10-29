from sopflow.graph import find_cycle, frontier, reachable, topo_sort


def test_topo_sort_respects_edges_and_declaration_order():
    assert topo_sort(["a", "b", "c", "d"], [("a", "c"), ("b", "c"), ("c", "d")]) == ["a", "b", "c", "d"]


def test_topo_sort_none_on_cycle():
    assert topo_sort(["a", "b", "c"], [("a", "b"), ("b", "c"), ("c", "a")]) is None


def test_find_cycle_returns_the_cycle():
    cyc = find_cycle(["a", "b", "c", "d"], [("a", "b"), ("b", "c"), ("c", "b"), ("c", "d")])
    assert set(cyc) == {"b", "c"}
    assert find_cycle(["a", "b"], [("a", "b")]) is None


def test_reachable():
    assert reachable(["a"], [("a", "b"), ("c", "d")]) == {"a", "b"}


def test_frontier_or_join_and_dead_branches():
    ids = ["s1", "s2", "s3", "s4"]
    edges = [("s1", "s2"), ("s1", "s3"), ("s2", "s4"), ("s3", "s4")]
    assert frontier(ids, edges, set(), set()) == ["s1"]
    # s1 took only the edge to s2: s3 is dead, s4 waits for s2
    assert frontier(ids, edges, {"s1"}, {("s1", "s2")}) == ["s2"]
    assert frontier(ids, edges, {"s1", "s2"}, {("s1", "s2"), ("s2", "s4")}) == ["s4"]
    assert frontier(ids, edges, {"s1", "s2", "s4"}, {("s1", "s2"), ("s2", "s4")}) == []
