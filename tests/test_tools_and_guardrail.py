"""Day 2 and Day 4: the tools and the guardrail, tested without any model."""

from types import SimpleNamespace

from vinyl_crate_agents.catalog import albums_in_genre
from vinyl_crate_agents.guardrails import block_owned_recommendation
from vinyl_crate_agents.tools import OWNED_KEY, add_owned_album, find_albums, recommend_album


def ctx(owned=None):
    state = {OWNED_KEY: list(owned)} if owned else {}
    return SimpleNamespace(state=state)


def test_find_albums_by_genre():
    result = find_albums("Jazz")
    assert result["status"] == "ok"
    assert {a["id"] for a in result["albums"]} == {a["id"] for a in albums_in_genre("jazz")}


def test_find_albums_unknown_genre():
    assert find_albums("polka")["status"] == "error"


def test_add_owned_album_is_idempotent():
    c = ctx()
    add_owned_album("kind-of-blue", c)
    add_owned_album("kind-of-blue", c)
    assert c.state[OWNED_KEY] == ["kind-of-blue"]


def test_add_unknown_album_is_rejected():
    assert add_owned_album("nope", ctx())["status"] == "error"


def test_guardrail_blocks_owned_album():
    tool = SimpleNamespace(name="recommend_album")
    result = block_owned_recommendation(tool, {"album_id": "kind-of-blue"}, ctx(["kind-of-blue"]))
    assert result["status"] == "blocked"


def test_guardrail_allows_other_albums_and_other_tools():
    rec = SimpleNamespace(name="recommend_album")
    other = SimpleNamespace(name="find_albums")
    assert block_owned_recommendation(rec, {"album_id": "blue-train"}, ctx(["kind-of-blue"])) is None
    assert block_owned_recommendation(other, {"genre": "jazz"}, ctx(["kind-of-blue"])) is None


def test_recommend_album_returns_text():
    assert "Blue Train" in recommend_album("blue-train", ctx())["recommendation"]
