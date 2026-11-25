"""Day 3: session state versus long-term memory.

Session state is a scratchpad for one conversation. Memory is searchable
knowledge kept across conversations. A finished session is added to memory,
and a later session can search it.

InMemoryMemoryService matches keywords and forgets on restart. In production
you swap in a persistent service, such as Vertex AI Memory Bank, without
changing the agent code.
"""

from google.adk.memory import InMemoryMemoryService
from google.adk.runners import InMemoryRunner
from google.genai import types

from .agents import build_root_agent


async def remember_session(model, text: str, app_name="vinyl_memory", user_id="juan"):
    """Run one conversation, then store it in long-term memory."""
    memory_service = InMemoryMemoryService()
    runner = InMemoryRunner(agent=build_root_agent(model), app_name=app_name)
    runner.memory_service = memory_service
    session = await runner.session_service.create_session(app_name=app_name, user_id=user_id)
    message = types.Content(role="user", parts=[types.Part(text=text)])
    async for _ in runner.run_async(user_id=user_id, session_id=session.id, new_message=message):
        pass
    session = await runner.session_service.get_session(
        app_name=app_name, user_id=user_id, session_id=session.id
    )
    await memory_service.add_session_to_memory(session)
    return memory_service, session
