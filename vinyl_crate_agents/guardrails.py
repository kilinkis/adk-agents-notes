"""Day 4: guardrails and logging as callbacks.

A before-tool callback runs before every tool call. If it returns a dict, ADK
skips the real tool and hands that dict to the model as the tool result, so the
model can recover and pick something else. If it returns None, the tool runs.

The guardrail is code, not a prompt instruction. A prompt asks the model to
behave, a callback makes the rule hold even when the model forgets it.
"""

import logging

from .tools import OWNED_KEY

logger = logging.getLogger("vinyl_crate_agents")


def block_owned_recommendation(tool, args, tool_context):
    """Refuse to recommend an album the user already owns."""
    if getattr(tool, "name", None) != "recommend_album":
        return None
    album_id = args.get("album_id")
    if album_id in tool_context.state.get(OWNED_KEY, []):
        logger.warning("guardrail blocked recommending owned album %s", album_id)
        return {
            "status": "blocked",
            "message": f"The user already owns '{album_id}'. Recommend a different album.",
        }
    return None


def log_tool_call(tool, args, tool_context):
    """Log every tool call with its arguments. Never blocks."""
    logger.info("tool=%s args=%s", getattr(tool, "name", "?"), args)
    return None


def log_tool_result(tool, args, tool_context, tool_response):
    """Log every tool result. Never changes it."""
    logger.info("tool=%s result=%s", getattr(tool, "name", "?"), tool_response)
    return None


def configure_logging(level: int = logging.INFO) -> None:
    """Call once at startup. ADK also logs, this adds the example's own logger."""
    logging.basicConfig(
        level=level,
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    )
