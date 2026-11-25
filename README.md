# ADK agents notes

Notes and a small working example from the [5-Day AI Agents Intensive Course with Google](https://www.kaggle.com/learn-guide/5-day-agents) on Kaggle, which teaches Google's Agent Development Kit (ADK).
This is my own project built after the course. It is not part of the course material.

The example is a small vinyl record assistant. It touches each day of the course:

| Day | Topic | Where to look |
| --- | --- | --- |
| 1 | Agents and splitting responsibilities | [`agents.py`](vinyl_crate_agents/agents.py), [notes](notes/day-1-agents.md) |
| 2 | Tools and MCP | [`tools.py`](vinyl_crate_agents/tools.py), [`album_facts_server.py`](vinyl_crate_agents/album_facts_server.py), [notes](notes/day-2-tools-and-mcp.md) |
| 3 | Sessions, state and memory | [`memory_demo.py`](vinyl_crate_agents/memory_demo.py), [notes](notes/day-3-sessions-and-memory.md) |
| 4 | Quality: guardrails, logging, evals | [`guardrails.py`](vinyl_crate_agents/guardrails.py), [`evals/`](evals), [notes](notes/day-4-quality.md) |
| 5 | A2A and production | [`a2a_server.py`](vinyl_crate_agents/a2a_server.py), [notes](notes/day-5-a2a-and-production.md) |

## How it works

A coordinator agent routes each request to one of two specialists. One keeps the list of albums you own in session state. The other recommends albums from a small sample catalog.
A guardrail callback stops it from recommending an album you already own, even if the model forgets the instruction.

## Run the tests

The tests need no API key. A scripted fake model stands in for Gemini, while ADK's runner, sessions, state, transfers and callbacks run for real.

```bash
pip install -r requirements.txt
pytest
```

## Run it with Gemini

Needs a Gemini API key. Set `VINYL_MODEL` to use a different model than the default.

```bash
export GOOGLE_API_KEY=...
adk web
```

Then pick `vinyl_crate_agents`. Try "I own Kind of Blue", then "Recommend me some jazz".

## What is and is not verified

- Verified: the tools, the guardrail, the routing and state flow with a scripted model, the memory example, the MCP server round trip, and the A2A agent card. Tested with Python 3.13 and `google-adk` 2.15.1.
- Not verified: behavior with a real Gemini model, and the eval set (`adk eval vinyl_crate_agents evals/vinyl_basics.evalset.json --config_file_path evals/test_config.json`). The tests only check that the eval files parse.
- Not done: deployment to Vertex AI Agent Engine.

## Related projects

- [python-vinyl-crate](https://github.com/kilinkis/python-vinyl-crate): my vinyl recommender, the idea behind this example
- [tracerag](https://github.com/kilinkis/tracerag): my RAG project
- [ticket-summarizer-adk-demo](https://github.com/kilinkis/ticket-summarizer-adk-demo): an earlier ADK project
- [adk-ikea-brand-analysis](https://github.com/kilinkis/adk-ikea-brand-analysis): another ADK project
