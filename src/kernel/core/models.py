"""Core domain models shared across the runtime: messages, tool calls/results, and events."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from enum import StrEnum


class Role(StrEnum):
    """Author of a conversation message."""

    SYSTEM = "system"
    USER = "user"
    ASSISTANT = "assistant"
    TOOL = "tool"


@dataclass(frozen=True, slots=True)
class ToolCall:
    """A request, produced by the LLM, to invoke a specific tool with arguments."""

    tool_name: str
    arguments: dict[str, object]


@dataclass(frozen=True, slots=True)
class ToolResult:
    """The outcome of executing a `ToolCall`."""

    tool_name: str
    output: str
    is_error: bool = False


@dataclass(frozen=True, slots=True)
class Message:
    """A single turn in a conversation.

    A message may optionally carry a `ToolCall` (assistant asking to run a tool) or a
    `ToolResult` (the result being fed back into the conversation as a tool message).
    """

    role: Role
    content: str
    tool_call: ToolCall | None = None
    tool_result: ToolResult | None = None


class EventType(StrEnum):
    """Kinds of significant runtime actions published on the event bus."""

    AGENT_STARTED = "agent_started"
    PROMPT_RECEIVED = "prompt_received"
    TOOL_STARTED = "tool_started"
    TOOL_COMPLETED = "tool_completed"
    TOOL_FAILED = "tool_failed"
    LLM_RESPONSE_GENERATED = "llm_response_generated"


@dataclass(frozen=True, slots=True)
class Event:
    """An observable runtime event.

    `correlation_id` ties every event in a single turn/conversation together so future
    phases (tracing) can reconstruct a timeline without changing this schema.
    """

    type: EventType
    correlation_id: str
    payload: dict[str, object] = field(default_factory=dict)
    timestamp: datetime = field(default_factory=lambda: datetime.now(UTC))
