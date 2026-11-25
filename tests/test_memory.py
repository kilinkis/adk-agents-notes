"""Day 3: a finished session is searchable from long-term memory."""

import asyncio

from fake_model import FakeLlm, say
from vinyl_crate_agents.memory_demo import remember_session


def test_session_is_searchable_after_it_is_added_to_memory():
    async def run():
        model = FakeLlm([say("Noted.")])
        service, _ = await remember_session(model, "My favourite label is Blue Note Records.")
        hit = await service.search_memory(app_name="vinyl_memory", user_id="juan", query="Blue Note")
        miss = await service.search_memory(app_name="vinyl_memory", user_id="other", query="Blue Note")
        return hit, miss

    hit, miss = asyncio.run(run())
    assert hit.memories, "expected the earlier session to be found"
    assert not miss.memories, "memory must stay scoped to the user"
