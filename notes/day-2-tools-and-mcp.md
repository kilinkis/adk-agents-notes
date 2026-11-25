# Day 2: Tools and interoperability with MCP

**My takeaway:** tools and MCPs.

## What the notebooks covered
- 2a: turn Python functions into agent tools, use an agent as a tool in another agent, build a multi-tool agent, and the different tool types in ADK.
- 2b: connect to external MCP servers, long-running operations that pause the agent for outside input, and resumable workflows that keep state across breaks.

## In this repo
- [`tools.py`](../vinyl_crate_agents/tools.py): plain functions with type hints and docstrings. The docstring is what the model reads, so I wrote them for the model.
- [`album_facts_server.py`](../vinyl_crate_agents/album_facts_server.py): a tiny MCP server with one tool.
- [`mcp_agent.py`](../vinyl_crate_agents/mcp_agent.py): the agent side. It starts the server, discovers the tool and exposes it, without importing the server's code.
- [`tests/test_mcp.py`](../tests/test_mcp.py): discovers the tool over stdio and calls it for real.

Not covered here: agent-as-a-tool, and the pause-and-resume pattern for long-running approvals.
