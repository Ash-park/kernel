"""Tests for `ToolExecutor`."""

from __future__ import annotations

from kernel.adapters.events.in_memory_event_bus import InMemoryEventBus
from kernel.core.models import EventType, ToolCall, ToolResult
from kernel.core.tool_executor import ToolExecutor
from kernel.interfaces.tool import Tool


class _FakeTool(Tool):
    name = "fake"
    description = "A fake tool for testing."

    def run(self, arguments: dict[str, object]) -> ToolResult:
        return ToolResult(tool_name=self.name, output=f"ran with {arguments}")


class _FailingTool(Tool):
    name = "failing"
    description = "A tool that always raises."

    def run(self, arguments: dict[str, object]) -> ToolResult:
        raise RuntimeError("boom")


def test_execute_runs_registered_tool_and_emits_events() -> None:
    event_bus = InMemoryEventBus()
    seen_types: list[EventType] = []
    for event_type in EventType:
        event_bus.subscribe(event_type, lambda event: seen_types.append(event.type))

    executor = ToolExecutor(tools={"fake": _FakeTool()}, event_bus=event_bus)
    result = executor.execute(ToolCall(tool_name="fake", arguments={"x": 1}), correlation_id="c1")

    assert result.is_error is False
    assert "ran with" in result.output
    assert seen_types == [EventType.TOOL_STARTED, EventType.TOOL_COMPLETED]


def test_execute_unknown_tool_returns_error_result() -> None:
    event_bus = InMemoryEventBus()
    executor = ToolExecutor(tools={}, event_bus=event_bus)

    result = executor.execute(ToolCall(tool_name="missing", arguments={}), correlation_id="c1")

    assert result.is_error is True
    assert "Unknown tool" in result.output


def test_execute_catches_tool_exceptions_as_error_result() -> None:
    event_bus = InMemoryEventBus()
    executor = ToolExecutor(tools={"failing": _FailingTool()}, event_bus=event_bus)

    result = executor.execute(ToolCall(tool_name="failing", arguments={}), correlation_id="c1")

    assert result.is_error is True
    assert "boom" in result.output
