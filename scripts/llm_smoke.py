"""Smoke test for the CI LLM backend: download the official Qwen GGUF and answer one JSON-constrained prompt."""
import json, time
from huggingface_hub import hf_hub_download
from llama_cpp import Llama

t0 = time.time()
path = hf_hub_download("Qwen/Qwen2.5-1.5B-Instruct-GGUF", "qwen2.5-1.5b-instruct-q4_k_m.gguf")
llm = Llama(model_path=path, n_ctx=4096, n_threads=4, verbose=False, seed=0)
t1 = time.time()
out = llm.create_chat_completion(
    messages=[{"role": "user", "content": "List the steps: (1) Notify employees. (2) Shut down the machine. Return JSON {\"steps\": [string]}."}],
    response_format={"type": "json_object", "schema": {"type": "object", "properties": {"steps": {"type": "array", "items": {"type": "string"}}}, "required": ["steps"]}},
    temperature=0, max_tokens=200)
t2 = time.time()
u = out["usage"]
print(json.dumps({"load_s": round(t1 - t0, 1), "gen_s": round(t2 - t1, 1), "usage": u,
                  "tok_per_s": round(u["completion_tokens"] / (t2 - t1), 1),
                  "content": out["choices"][0]["message"]["content"]}, indent=1))
