"""Entry point for `adk web` and `adk run`. ADK looks for `root_agent`."""

from .agents import build_root_agent
from .guardrails import configure_logging

configure_logging()
root_agent = build_root_agent()
