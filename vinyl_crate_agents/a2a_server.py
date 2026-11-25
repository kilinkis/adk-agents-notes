"""Day 5: expose the agent over the A2A protocol so other agents can call it.

Serve it with:  uvicorn vinyl_crate_agents.a2a_server:a2a_app --port 8001

The agent card is published at /.well-known/agent-card.json. It tells a remote
agent what this agent can do and where to send requests. Nothing here is
deployed anywhere, this is the local version of the same idea.
"""

from google.adk.a2a.utils.agent_to_a2a import to_a2a

from .agents import build_root_agent

a2a_app = to_a2a(build_root_agent(), port=8001)
