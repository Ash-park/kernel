"""Tests for `AgentRuntime`, using fakes only (no adapters, no network)."""

from __future__ import annotations

from kernel.core.agent_runtime import AgentRuntime
from kernel.core.context_manager import ContextManager
from kernel.core.conversation import ConversationState
from kernel.core.models import Event, EventType, Message, Role, ToolCall, ToolResult
from kernel.core.tool_executor import ToolExecutor
from kernel.interfaces.tool import Tool


class _RecordingEventBus:
    def __init__(self) -> None:
        self.published: list[Event] = []

    def publish(self, event: Event) -> None:
        self.published.append(event)

    def subscribe(self, event_type, handler) -> None:  # noqa: ANN001 - test double
        raise NotImplementedError("not needed for these tests")


class _OneShotLLMClient:
    """Returns a fixed reply, ignoring the conversation."""

    def __init__(self, reply: Message) -> None:
        self._reply = reply

    def complete(self, messages: list[Message]) -> Message:
        return self._reply


class _ToolThenReplyLLMClient:
    """Requests a tool call once, then replies with a fixed message."""

    def __init__(self) -> None:
        self._called = False

    def complete(self, messages: list[Message]) -> Message:
        if not self._called:
            self._called = True
            return Message(
                role=Role.ASSISTANT,
                content="",
                tool_call=ToolCall(tool_name="echo", arguments={"text": "hi"}),
            )
        return Message(role=Role.ASSISTANT, content="done")


class _EchoTool(Tool):
    name = "echo"
    description = "Echoes text."

    def run(self, arguments: dict[str, object]) -> ToolResult:
        return ToolResult(tool_name=self.name, output=str(arguments["text"]))


def _build_runtime(llm_client) -> tuple[AgentRuntime, _RecordingEventBus]:  # noqa: ANN001
    event_bus = _RecordingEventBus()
    runtime = AgentRuntime(
        llm_client=llm_client,
        conversation=ConversationState(),
        context_manager=ContextManager(),
        tool_executor=ToolExecutor(tools={"echo": _EchoTool()}, event_bus=event_bus),
        event_bus=event_bus,
    )
    return runtime, event_bus


def test_handle_turn_returns_assistant_reply_without_tool_call() -> None:
    reply = Message(role=Role.ASSISTANT, content="hello back")
    runtime, event_bus = _build_runtime(_OneShotLLMClient(reply))

    result = runtime.handle_turn("hi")

    assert result.content == "hello back"
    published_types = [event.type for event in event_bus.published]
    assert published_types == [
        EventType.AGENT_STARTED,
        EventType.PROMPT_RECEIVED,
        EventType.LLM_RESPONSE_GENERATED,
    ]


def test_handle_turn_executes_tool_call_and_loops_back_to_llm() -> None:
    runtime, event_bus = _build_runtime(_ToolThenReplyLLMClient())

    result = runtime.handle_turn("echo:hi")

    assert result.content == "done"
    published_types = [event.type for event in event_bus.published]
    assert EventType.TOOL_STARTED in published_types
    assert EventType.TOOL_COMPLETED in published_types
    assert published_types.count(EventType.LLM_RESPONSE_GENERATED) == 2
