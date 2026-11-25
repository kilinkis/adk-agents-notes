"""Day 2: ADK can discover the MCP server's tool and call it."""

import asyncio

from vinyl_crate_agents.mcp_agent import album_facts_toolset


async def discover_and_call():
    toolset = album_facts_toolset()
    try:
        tools = await toolset.get_tools()
        names = [t.name for t in tools]
        result = await tools[0].run_async(args={"album_id": "kind-of-blue"}, tool_context=None)
        return names, result
    finally:
        await toolset.close()


def test_mcp_tool_is_discovered_and_callable():
    names, result = asyncio.run(discover_and_call())
    assert names == ["album_facts"]
    assert "Miles Davis" in str(result)
