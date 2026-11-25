"""Day 5: the agent is exposed with a card that describes it, and a client can be built."""

from starlette.testclient import TestClient

from vinyl_crate_agents.a2a_client_agent import build_client_agent
from vinyl_crate_agents.a2a_server import a2a_app


def test_agent_card_is_published():
    with TestClient(a2a_app) as client:
        response = client.get("/.well-known/agent-card.json")
    assert response.status_code == 200
    card = response.json()
    assert card["name"] == "vinyl_coordinator"
    assert card["skills"], "the card should list what the agent can do"


def test_client_agent_can_be_built():
    agent = build_client_agent()
    assert [a.name for a in agent.sub_agents] == ["remote_vinyl_coordinator"]
