"""Full-turn integration test wiring real in-process adapters (no network)."""

from __future__ import annotations

from kernel.adapters.events.in_memory_event_bus import InMemoryEventBus
from kernel.adapters.llm.stub_llm_client import StubLLMClient
from kernel.adapters.tools.echo_tool import EchoTool
from kernel.core.agent_runtime import AgentRuntime
from kernel.core.context_manager import ContextManager
from kernel.core.conversation import ConversationState
from kernel.core.models import Event, EventType
from kernel.core.tool_executor import ToolExecutor


def test_full_turn_with_tool_call_emits_all_core_event_types() -> None:
    event_bus = InMemoryEventBus()
    seen: list[Event] = []
    for event_type in EventType:
        event_bus.subscribe(event_type, seen.append)

    echo_tool = EchoTool()
    runtime = AgentRuntime(
        llm_client=StubLLMClient(),
        conversation=ConversationState(),
        context_manager=ContextManager(),
        tool_executor=ToolExecutor(tools={echo_tool.name: echo_tool}, event_bus=event_bus),
        event_bus=event_bus,
    )

    reply = runtime.handle_turn("echo:hello world")

    assert reply.content == "Tool said: hello world"
    seen_types = {event.type for event in seen}
    assert seen_types == {
        EventType.AGENT_STARTED,
        EventType.PROMPT_RECEIVED,
        EventType.LLM_RESPONSE_GENERATED,
        EventType.TOOL_STARTED,
        EventType.TOOL_COMPLETED,
    }


def test_full_turn_without_tool_call_returns_stub_reply() -> None:
    event_bus = InMemoryEventBus()
    echo_tool = EchoTool()
    runtime = AgentRuntime(
        llm_client=StubLLMClient(),
        conversation=ConversationState(),
        context_manager=ContextManager(),
        tool_executor=ToolExecutor(tools={echo_tool.name: echo_tool}, event_bus=event_bus),
        event_bus=event_bus,
    )

    reply = runtime.handle_turn("hello")

    assert reply.content == "You said: hello"
