"""Tests for `StubLLMClient`."""

from __future__ import annotations

from kernel.adapters.llm.stub_llm_client import StubLLMClient
from kernel.core.models import Message, Role, ToolResult


def test_complete_echoes_prompt_by_default() -> None:
    client = StubLLMClient()

    reply = client.complete([Message(role=Role.USER, content="hello")])

    assert reply.content == "You said: hello"


def test_complete_requests_echo_tool_on_trigger_prefix() -> None:
    client = StubLLMClient()

    reply = client.complete([Message(role=Role.USER, content="echo:hi there")])

    assert reply.tool_call is not None
    assert reply.tool_call.tool_name == "echo"
    assert reply.tool_call.arguments == {"text": "hi there"}


def test_complete_summarizes_tool_result() -> None:
    client = StubLLMClient()
    tool_message = Message(
        role=Role.TOOL,
        content="hi there",
        tool_result=ToolResult(tool_name="echo", output="hi there"),
    )

    reply = client.complete([tool_message])

    assert reply.content == "Tool said: hi there"
