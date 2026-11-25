"""Day 2: a tiny MCP server. Any MCP-aware agent can discover and call its tool.

Run it on its own with `python -m vinyl_crate_agents.album_facts_server`. It
talks over stdio, which is how ADK starts local MCP servers.
"""

from mcp.server.mcpserver import MCPServer

from .catalog import get_album

mcp = MCPServer("album-facts")


@mcp.tool()
def album_facts(album_id: str) -> str:
    """Return the title, artist, genre and year of a catalog album."""
    album = get_album(album_id)
    if album is None:
        return f"Unknown album id '{album_id}'."
    return f"{album.title} by {album.artist}, {album.genre}, {album.year}."


if __name__ == "__main__":
    mcp.run()
