# Day 1: Introduction to agents

**My takeaway:** worked with multi-agent systems, and the importance of splitting responsibilities.

## What the notebooks covered
- 1a: install ADK, configure the Gemini key, build a first agent, watch it use a tool such as Google Search.
- 1b: when to use multi-agent systems, an LLM acting as a "manager", and three workflow patterns: Sequential, Parallel and Loop.

## In this repo
[`vinyl_crate_agents/agents.py`](../vinyl_crate_agents/agents.py) has a coordinator that only routes, and two specialists:
- `collection_keeper` knows about the collection and has two tools.
- `recommender` picks albums and has two different tools.

Each agent has a short instruction and a small tool set, so its behavior is easy to reason about and to test.
The scripted-model test in [`tests/test_agent_flow.py`](../tests/test_agent_flow.py) checks that a request really travels from the coordinator to the right specialist.

## Questions I still have
- When is one agent with more tools better than several agents? I want to see where a plain workflow wins in real work.
