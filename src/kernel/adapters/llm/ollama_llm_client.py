"""Real `LLMClient` implementation backed by a local Ollama server."""

from __future__ import annotations

import httpx

from kernel.core.models import Message, Role

DEFAULT_BASE_URL = "http://localhost:11434"
DEFAULT_TIMEOUT_SECONDS = 30.0


class OllamaLLMClient:
    """Calls a local Ollama server's `/api/chat` endpoint.

    Phase 1 scope: plain chat completion only. Tool-call parsing from the provider
    response is not implemented here (the `echo:` convention lives in `StubLLMClient`
    for tests); adding real tool-call parsing for Ollama is a follow-up task, not a
    blocker for Phase 1 acceptance criteria.
    """

    def __init__(
        self,
        model: str,
        base_url: str = DEFAULT_BASE_URL,
        timeout: float = DEFAULT_TIMEOUT_SECONDS,
    ) -> None:
        self._model = model
        self._base_url = base_url.rstrip("/")
        self._timeout = timeout

    def complete(self, messages: list[Message]) -> Message:
        """Send `messages` to Ollama and return the assistant's reply as a `Message`."""
        payload = {
            "model": self._model,
            "messages": [
                {"role": message.role.value, "content": message.content} for message in messages
            ],
            "stream": False,
        }
        with httpx.Client(timeout=self._timeout) as client:
            response = client.post(f"{self._base_url}/api/chat", json=payload)
            response.raise_for_status()
            data = response.json()

        content = data.get("message", {}).get("content", "")
        return Message(role=Role.ASSISTANT, content=content)
