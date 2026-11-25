"""Day 1: split responsibilities across agents.

A coordinator reads the request and hands it to the agent that owns that job.
Each specialist has few tools and a short instruction, which keeps its behavior
easy to test.
"""

import os

from google.adk.agents import Agent

from .guardrails import block_owned_recommendation, log_tool_call, log_tool_result
from .tools import add_owned_album, find_albums, list_owned_albums, recommend_album

DEFAULT_MODEL = os.environ.get("VINYL_MODEL", "gemini-flash-latest")


def build_root_agent(model=DEFAULT_MODEL) -> Agent:
    """Build the agent tree. Tests pass a scripted fake model instead of a name."""
    collection_keeper = Agent(
        name="collection_keeper",
        model=model,
        description="Keeps track of which albums the user owns.",
        instruction=(
            "You manage the user's record collection. When the user says they own "
            "an album, call add_owned_album with its catalog id. When they ask what "
            "they own, call list_owned_albums. Reply in one short sentence."
        ),
        tools=[add_owned_album, list_owned_albums],
        before_tool_callback=log_tool_call,
        after_tool_callback=log_tool_result,
    )

    recommender = Agent(
        name="recommender",
        model=model,
        description="Recommends albums from the catalog by genre.",
        instruction=(
            "You recommend one album. Call find_albums for the genre the user wants, "
            "then call recommend_album with the id of your pick. Never recommend an "
            "album the user already owns. If a tool says an album is blocked, pick a "
            "different one. Reply with the recommendation in one short sentence."
        ),
        tools=[find_albums, recommend_album],
        before_tool_callback=[log_tool_call, block_owned_recommendation],
        after_tool_callback=log_tool_result,
    )

    return Agent(
        name="vinyl_coordinator",
        model=model,
        description="Routes record collection requests to the right specialist.",
        instruction=(
            "You route requests. If the user tells you what they own or asks about "
            "their collection, transfer to collection_keeper. If they want a "
            "recommendation, transfer to recommender. Do not answer these yourself."
        ),
        sub_agents=[collection_keeper, recommender],
    )
