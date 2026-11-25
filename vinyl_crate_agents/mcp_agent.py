"""Day 2: the same idea from the agent side, consuming an MCP server's tools.

The agent never imports album_facts. ADK starts the server as a subprocess,
asks it which tools it offers, and exposes them to the model.
"""

import sys

from google.adk.agents import Agent
from google.adk.tools.mcp_tool import McpToolset, StdioConnectionParams
from mcp import StdioServerParameters

from .agents import DEFAULT_MODEL


def album_facts_toolset() -> McpToolset:
    return McpToolset(
        connection_params=StdioConnectionParams(
            server_params=StdioServerParameters(
                command=sys.executable,
                args=["-m", "vinyl_crate_agents.album_facts_server"],
            ),
            timeout=30,
        )
    )


def build_facts_agent(model=DEFAULT_MODEL) -> Agent:
    return Agent(
        name="album_facts_agent",
        model=model,
        description="Answers factual questions about catalog albums using an MCP tool.",
        instruction="Answer questions about an album by calling album_facts with its catalog id.",
        tools=[album_facts_toolset()],
    )
