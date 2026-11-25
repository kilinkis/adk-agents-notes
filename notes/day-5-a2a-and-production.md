# Day 5: Prototype to production

**My takeaway:** the A2A protocol and deploys.

## What the notebooks covered
- 5a: the A2A protocol and when to use it instead of sub-agents, architecture patterns (cross-framework, cross-language, cross-organization), exposing an agent with `to_a2a()` and consuming one with `RemoteA2aAgent`.
- 5b: a production-ready agent, deploying to Vertex AI Agent Engine with the ADK CLI, testing the deployed agent, monitoring, Vertex AI Memory Bank, and cost management and cleanup.

## In this repo
- [`a2a_server.py`](../vinyl_crate_agents/a2a_server.py): exposes the agent over A2A.
- [`a2a_client_agent.py`](../vinyl_crate_agents/a2a_client_agent.py): a second agent that treats it as a remote sub-agent.
- [`tests/test_a2a.py`](../tests/test_a2a.py): checks the published agent card.

Nothing is deployed. The deployment notebook needs a Google Cloud account and can cost money, so I stopped at reading it.
