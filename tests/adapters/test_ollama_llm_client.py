"""Tests for `OllamaLLMClient`, using a mocked HTTP transport (no real network call)."""

from __future__ import annotations

import httpx

from kernel.adapters.llm.ollama_llm_client import OllamaLLMClient
from kernel.core.models import Message, Role


def test_complete_posts_messages_and_parses_reply() -> None:
    captured_request: dict[str, object] = {}

    def handler(request: httpx.Request) -> httpx.Response:
        captured_request["url"] = str(request.url)
        captured_request["body"] = request.content
        return httpx.Response(200, json={"message": {"role": "assistant", "content": "hi back"}})

    client = OllamaLLMClient(model="llama3")
    client._base_url = "http://testserver"  # avoid depending on a real local server

    transport = httpx.MockTransport(handler)
    original_client_cls = httpx.Client
    httpx.Client = lambda timeout: original_client_cls(transport=transport, timeout=timeout)  # type: ignore[assignment]
    try:
        reply = client.complete([Message(role=Role.USER, content="hello")])
    finally:
        httpx.Client = original_client_cls  # type: ignore[assignment]

    assert reply.content == "hi back"
    assert captured_request["url"] == "http://testserver/api/chat"
