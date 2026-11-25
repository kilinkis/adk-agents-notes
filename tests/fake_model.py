"""A scripted stand-in for Gemini, so tests run offline and deterministically.

Each call to the model pops the next scripted response. The requests the model
received are kept, so a test can check what the model was shown (for example
that a blocked tool result reached it).
"""

from typing import AsyncGenerator

from google.adk.models.base_llm import BaseLlm
from google.adk.models.llm_request import LlmRequest
from google.adk.models.llm_response import LlmResponse
from google.genai import types
from pydantic import PrivateAttr


def call(name: str, **args) -> LlmResponse:
    part = types.Part(function_call=types.FunctionCall(name=name, args=args))
    return LlmResponse(content=types.Content(role="model", parts=[part]))


def say(text: str) -> LlmResponse:
    return LlmResponse(content=types.Content(role="model", parts=[types.Part(text=text)]))


class FakeLlm(BaseLlm):
    model: str = "fake"
    _script: list = PrivateAttr(default_factory=list)
    _requests: list = PrivateAttr(default_factory=list)

    def __init__(self, script: list[LlmResponse]):
        super().__init__()
        self._script = list(script)

    @property
    def requests(self) -> list:
        return self._requests

    @property
    def capabilities(self):
        from google.adk.models.base_llm import LlmCapabilities

        return LlmCapabilities(output_schema_and_tools=True)

    async def generate_content_async(
        self, llm_request: LlmRequest, stream: bool = False
    ) -> AsyncGenerator[LlmResponse, None]:
        self._requests.append(llm_request)
        if not self._script:
            raise AssertionError("The fake model was called more times than scripted.")
        yield self._script.pop(0)
