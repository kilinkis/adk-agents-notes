# Day 3: Context engineering, sessions and memory

**My takeaway:** state and memory, and also context engineering.

## What the notebooks covered
- 3a: what sessions are, stateful agents with sessions and events, persisting sessions in a database, context compaction, and best practices for sharing session state.
- 3b: initialize a memory service, move session data into memory, search and retrieve memories, automate storage and retrieval, and a conceptual look at memory consolidation.

## In this repo
- **Session state** holds the albums the user owns: [`tools.py`](../vinyl_crate_agents/tools.py) writes `owned_album_ids` through the tool context, so every agent in the session sees it. The guardrail on Day 4 reads the same key.
- **Memory** is shown in [`memory_demo.py`](../vinyl_crate_agents/memory_demo.py): one session is stored in memory and a later search finds it.
  [`tests/test_memory.py`](../tests/test_memory.py) also checks that one user cannot find another user's memories.

State is a scratchpad for one conversation. Memory is searchable and outlives the conversation. In the example the in-memory service forgets on restart, a real deployment would use a persistent one.
