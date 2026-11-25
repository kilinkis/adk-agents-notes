"""Day 2 and Day 3: plain Python functions become agent tools.

ADK reads the type hints and the docstring to build the tool schema, so the
docstrings below are written for the model, not for people.

The collection lives in session state under OWNED_KEY (Day 3), so every agent
in the same session sees the same list.
"""

from google.adk.tools import ToolContext

from .catalog import albums_in_genre, get_album

OWNED_KEY = "owned_album_ids"
RECOMMENDED_KEY = "recommended_album_ids"


def find_albums(genre: str) -> dict:
    """Look up albums in the catalog by genre.

    Args:
        genre: One of jazz, rock or electronic.

    Returns:
        A dict with status and a list of matching albums.
    """
    albums = albums_in_genre(genre)
    if not albums:
        return {"status": "error", "message": f"No albums found for genre '{genre}'."}
    return {"status": "ok", "albums": albums}


def add_owned_album(album_id: str, tool_context: ToolContext) -> dict:
    """Record that the user already owns an album.

    Args:
        album_id: The catalog id of the album, for example kind-of-blue.

    Returns:
        A dict with status and the updated list of owned album ids.
    """
    if get_album(album_id) is None:
        return {"status": "error", "message": f"Unknown album id '{album_id}'."}
    owned = list(tool_context.state.get(OWNED_KEY, []))
    if album_id not in owned:
        owned.append(album_id)
    tool_context.state[OWNED_KEY] = owned
    return {"status": "ok", "owned": owned}


def list_owned_albums(tool_context: ToolContext) -> dict:
    """List the albums the user already owns."""
    return {"status": "ok", "owned": list(tool_context.state.get(OWNED_KEY, []))}


def recommend_album(album_id: str, tool_context: ToolContext) -> dict:
    """Recommend one album to the user and remember that it was recommended.

    Args:
        album_id: The catalog id of the album to recommend.

    Returns:
        A dict with status and the album that was recommended.
    """
    album = get_album(album_id)
    if album is None:
        return {"status": "error", "message": f"Unknown album id '{album_id}'."}
    recommended = list(tool_context.state.get(RECOMMENDED_KEY, []))
    if album_id not in recommended:
        recommended.append(album_id)
    tool_context.state[RECOMMENDED_KEY] = recommended
    return {
        "status": "ok",
        "recommendation": f"{album.title} by {album.artist} ({album.year})",
    }
