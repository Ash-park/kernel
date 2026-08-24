"""Tests for `OpenAICompatibleLLMClient`, using a stubbed `openai` client (no real network)."""

from __future__ import annotations

from kernel.adapters.llm.openai_compatible_llm_client import OpenAICompatibleLLMClient
from kernel.core.models import Message, Role


class _FakeChoice:
    def __init__(self, content: str) -> None:
        self.message = type("_Msg", (), {"content": content})()


class _FakeCompletions:
    def __init__(self, content: str) -> None:
        self._content = content
        self.last_kwargs: dict[str, object] = {}

    def create(self, **kwargs: object) -> object:
        self.last_kwargs = kwargs
        return type("_Response", (), {"choices": [_FakeChoice(self._content)]})()


class _FakeChat:
    def __init__(self, content: str) -> None:
        self.completions = _FakeCompletions(content)


class _FakeOpenAIClient:
    def __init__(self, content: str) -> None:
        self.chat = _FakeChat(content)


def test_complete_sends_model_and_messages_and_parses_reply(monkeypatch) -> None:  # noqa: ANN001
    fake_client = _FakeOpenAIClient("hi back")
    monkeypatch.setattr(
        "kernel.adapters.llm.openai_compatible_llm_client.OpenAI",
        lambda base_url, api_key: fake_client,
    )

    client = OpenAICompatibleLLMClient(model="qwen2.5-7b", base_url="http://x", api_key="k")
    reply = client.complete([Message(role=Role.USER, content="hello")])

    assert reply.content == "hi back"
    assert fake_client.chat.completions.last_kwargs["model"] == "qwen2.5-7b"
    assert fake_client.chat.completions.last_kwargs["messages"] == [
        {"role": "user", "content": "hello"}
    ]


def test_reads_config_from_env_vars_when_not_passed(monkeypatch) -> None:  # noqa: ANN001
    fake_client = _FakeOpenAIClient("ok")
    captured_kwargs: dict[str, object] = {}

    def fake_openai(**kwargs: object) -> _FakeOpenAIClient:
        captured_kwargs.update(kwargs)
        return fake_client

    monkeypatch.setattr("kernel.adapters.llm.openai_compatible_llm_client.OpenAI", fake_openai)
    monkeypatch.setenv("KERNEL_LLM_MODEL", "qwen2.5-7b")
    monkeypatch.setenv("KERNEL_LLM_BASE_URL", "http://localhost:18011/v1")
    monkeypatch.setenv("KERNEL_LLM_API_KEY", "local-rag-agent-tattvam")

    OpenAICompatibleLLMClient()

    assert captured_kwargs == {
        "base_url": "http://localhost:18011/v1",
        "api_key": "local-rag-agent-tattvam",
    }
