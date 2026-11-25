"""Day 5: the consuming side. A remote A2A agent is used like a local sub-agent.

Use sub-agents when everything runs in one codebase. Use A2A when the other
agent lives in another service, team, language or framework.
"""

from google.adk.agents import Agent
from google.adk.agents.remote_a2a_agent import RemoteA2aAgent

from .agents import DEFAULT_MODEL

AGENT_CARD_URL = "http://localhost:8001/.well-known/agent-card.json"


def build_client_agent(model=DEFAULT_MODEL) -> Agent:
    remote_vinyl = RemoteA2aAgent(
        name="remote_vinyl_coordinator",
        description="A remote agent that manages a record collection and recommends albums.",
        agent_card=AGENT_CARD_URL,
    )
    return Agent(
        name="shopping_assistant",
        model=model,
        instruction="For anything about records or the user's collection, transfer to remote_vinyl_coordinator.",
        sub_agents=[remote_vinyl],
    )
