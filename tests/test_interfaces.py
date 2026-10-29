import json

import anyio
from fastapi.testclient import TestClient


def test_mcp_tools_through_a_real_client(tmp_path, monkeypatch):
    monkeypatch.setenv("SOPFLOW_DB_DIR", str(tmp_path))
    from mcp import Client

    import sopflow.mcp_server as m
    m._svc = None

    async def go():
        async with Client(m.mcp) as client:            # in-process MCP client/server session
            names = {t.name for t in (await client.list_tools()).tools}
            assert {"list_workflows", "start_workflow", "get_state", "complete_step", "request_handoff"} <= names

            def data(res):
                assert not res.is_error if hasattr(res, "is_error") else not res.isError, res.content
                sc = getattr(res, "structured_content", None) or getattr(res, "structuredContent", None)
                if sc is not None:
                    return sc.get("result", sc) if isinstance(sc, dict) and set(sc) == {"result"} else sc
                return json.loads(res.content[0].text)

            st = data(await client.call_tool("start_workflow", {"sop_id": "pa_opd_prior_authorization", "seed": 1}))
            run = st["run_id"]
            assert data(await client.call_tool("get_state", {"run_id": run}))["status"] in ("waiting_for_human", "completed")
            if st["status"] == "waiting_for_human":
                step = st["pending_handoff"]["step_id"]
                st = data(await client.call_tool("complete_step", {"run_id": run, "step_id": step, "output": "reviewed"}))
            r = data(await client.call_tool("request_handoff", {"run_id": run, "step_id": "s5", "to_role": "supervisor"})) \
                if "s5" not in st["completed_steps"] else {"status": "handoff_scheduled"}
            assert r["status"] == "handoff_scheduled"
            assert len(data(await client.call_tool("list_workflows", {}))) >= 38
    anyio.run(go)


def test_rest_api(tmp_path, monkeypatch):
    monkeypatch.setenv("SOPFLOW_DB_DIR", str(tmp_path))
    import importlib

    import sopflow.api as api
    importlib.reload(api)
    c = TestClient(api.app)
    st = c.post("/runs", json={"sop_id": "onb_form_i9_verification"}).json()
    assert st["status"] == "waiting_for_human"
    st = c.post(f"/runs/{st['run_id']}/steps/s1/complete", json={"output": "signed"}).json()
    assert st["pending_handoff"]["step_id"] == "s2"
    assert c.post(f"/runs/{st['run_id']}/steps/s9/complete", json={"output": "x"}).status_code == 409
    assert c.get(f"/runs/{st['run_id']}").json()["completed_steps"] == ["s1"]
