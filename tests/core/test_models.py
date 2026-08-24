"""Tests for core domain models."""

from __future__ import annotations

from kernel.core.models import Event, EventType, Message, Role, ToolCall, ToolResult


def test_message_defaults_have_no_tool_call_or_result() -> None:
    message = Message(role=Role.USER, content="hello")

    assert message.tool_call is None
    assert message.tool_result is None


def test_event_generates_timestamp_when_not_provided() -> None:
    event = Event(type=EventType.AGENT_STARTED, correlation_id="abc")

    assert event.timestamp is not None
    assert event.payload == {}


def test_tool_call_and_result_are_immutable() -> None:
    call = ToolCall(tool_name="echo", arguments={"text": "hi"})
    result = ToolResult(tool_name="echo", output="hi")

    assert call.tool_name == "echo"
    assert result.is_error is False
