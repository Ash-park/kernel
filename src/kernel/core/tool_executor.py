"""Executes a single tool call against a registry of available tools, emitting lifecycle events."""

from __future__ import annotations

from kernel.core.models import Event, EventType, ToolCall, ToolResult
from kernel.interfaces.event_bus import EventBus
from kernel.interfaces.tool import Tool


class UnknownToolError(Exception):
    """Raised when a `ToolCall` references a tool that is not registered."""


class ToolExecutor:
    """Runs `ToolCall`s against a fixed registry of `Tool` instances.

    Phase 1 registers tools manually via the constructor; dynamic plugin discovery is a
    Phase 2 concern.
    """

    def __init__(self, tools: dict[str, Tool], event_bus: EventBus) -> None:
        self._tools = tools
        self._event_bus = event_bus

    def execute(self, tool_call: ToolCall, correlation_id: str) -> ToolResult:
        """Execute `tool_call`, publishing `TOOL_STARTED` and a completion/failure event."""
        self._event_bus.publish(
            Event(
                type=EventType.TOOL_STARTED,
                correlation_id=correlation_id,
                payload={"tool_name": tool_call.tool_name, "arguments": tool_call.arguments},
            )
        )

        tool = self._tools.get(tool_call.tool_name)
        if tool is None:
            result = ToolResult(
                tool_name=tool_call.tool_name,
                output=f"Unknown tool: {tool_call.tool_name}",
                is_error=True,
            )
        else:
            try:
                result = tool.run(tool_call.arguments)
            except Exception as exc:  # noqa: BLE001 - tool failures must not crash the runtime
                result = ToolResult(tool_name=tool_call.tool_name, output=str(exc), is_error=True)

        self._event_bus.publish(
            Event(
                type=EventType.TOOL_FAILED if result.is_error else EventType.TOOL_COMPLETED,
                correlation_id=correlation_id,
                payload={"tool_name": tool_call.tool_name, "output": result.output},
            )
        )
        return result
