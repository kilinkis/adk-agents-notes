# Day 4: Agent quality

**My takeaway:** quality, observability and evals.

## What the notebooks covered
- 4a: logging configuration, debugging a deliberately broken agent with the `adk web` UI and logs, logging in production, and built-in versus custom logging.
- 4b: what agent evaluation is, running evals in the web UI, catching regressions over time, and the eval files (`*.test.json`, `*.evalset.json`, `test_config.json`).

## In this repo
- [`guardrails.py`](../vinyl_crate_agents/guardrails.py): a before-tool callback that blocks recommending an owned album, plus callbacks that log every tool call and result. The guardrail is code, so it holds even when the model ignores the prompt.
- [`tests/test_agent_flow.py`](../tests/test_agent_flow.py): the model tries the owned album first, gets a "blocked" result, and recovers with another one.
- [`evals/`](../evals): an eval set and config in ADK's format. The tests check that the files parse. I have **not** run them against a live model.

Two kinds of checks are worth keeping apart: pytest for the code around the model, evals for the model's behavior.
