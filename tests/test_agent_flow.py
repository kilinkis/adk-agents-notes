"""Day 1, 3 and 4 together: run the real agent tree with a scripted model.

Nothing here calls Gemini. The scripted model plays the part of the LLM, while
ADK's runner, sessions, state, transfers and callbacks are all the real thing.
"""

import asyncio

from google.adk.runners import InMemoryRunner
from google.genai import types

from fake_model import FakeLlm, call, say
from vinyl_crate_agents.agents import build_root_agent
from vinyl_crate_agents.tools import OWNED_KEY, RECOMMENDED_KEY

APP, USER = "vinyl_test", "juan"


async def ask(runner, session_id, text):
    message = types.Content(role="user", parts=[types.Part(text=text)])
    events = []
    async for event in runner.run_async(user_id=USER, session_id=session_id, new_message=message):
        events.append(event)
    return events


def function_responses(events):
    out = []
    for event in events:
        for part in (event.content.parts if event.content and event.content.parts else []):
            if part.function_response:
                out.append(part.function_response)
    return out


async def scenario():
    model = FakeLlm(
        [
            # Turn 1: coordinator hands off, specialist records the album, replies.
            call("transfer_to_agent", agent_name="collection_keeper"),
            call("add_owned_album", album_id="kind-of-blue"),
            say("Noted, you own Kind of Blue."),
            # Turn 2: coordinator hands off, recommender tries the owned album first.
            call("transfer_to_agent", agent_name="recommender"),
            call("find_albums", genre="jazz"),
            call("recommend_album", album_id="kind-of-blue"),
            call("recommend_album", album_id="blue-train"),
            say("Try Blue Train by John Coltrane."),
        ]
    )
    runner = InMemoryRunner(agent=build_root_agent(model), app_name=APP)
    session = await runner.session_service.create_session(app_name=APP, user_id=USER)

    await ask(runner, session.id, "I own Kind of Blue.")
    events = await ask(runner, session.id, "Recommend me some jazz.")

    final = await runner.session_service.get_session(app_name=APP, user_id=USER, session_id=session.id)
    return model, events, final


def test_owned_album_is_stored_in_session_state():
    _, _, session = asyncio.run(scenario())
    assert session.state[OWNED_KEY] == ["kind-of-blue"]


def test_guardrail_blocks_owned_album_then_model_recovers():
    _, events, session = asyncio.run(scenario())
    statuses = [r.response.get("status") for r in function_responses(events)]
    assert "blocked" in statuses
    assert session.state[RECOMMENDED_KEY] == ["blue-train"]


def test_owned_album_never_ends_up_recommended():
    _, _, session = asyncio.run(scenario())
    assert not set(session.state[OWNED_KEY]) & set(session.state[RECOMMENDED_KEY])
