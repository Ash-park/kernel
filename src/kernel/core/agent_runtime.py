"""Orchestrates a single conversational turn: prompt -> LLM -> optional tool loop -> reply."""

from __future__ import annotations

import uuid

from kernel.core.context_manager import ContextManager
from kernel.core.conversation import ConversationState
from kernel.core.models import Event, EventType, Message, Role
from kernel.core.tool_executor import ToolExecutor
from kernel.interfaces.event_bus import EventBus
from kernel.interfaces.llm_client import LLMClient

DEFAULT_MAX_TOOL_ITERATIONS = 5


class AgentRuntime:
    """The single orchestrator of an agent turn.

    Depends only on abstractions (`LLMClient`, `EventBus`) and other `core/` collaborators,
    all injected via the constructor. Never imports `adapters/` or `cli/`.
    """

    def __init__(
        self,
        llm_client: LLMClient,
        conversation: ConversationState,
        context_manager: ContextManager,
        tool_executor: ToolExecutor,
        event_bus: EventBus,
        max_tool_iterations: int = DEFAULT_MAX_TOOL_ITERATIONS,
    ) -> None:
        self._llm_client = llm_client
        self._conversation = conversation
        self._context_manager = context_manager
        self._tool_executor = tool_executor
        self._event_bus = event_bus
        self._max_tool_iterations = max_tool_iterations

    def handle_turn(self, user_prompt: str) -> Message:
        """Process one user prompt end-to-end and return the final assistant `Message`."""
        correlation_id = str(uuid.uuid4())
        self._event_bus.publish(Event(EventType.AGENT_STARTED, correlation_id))

        self._conversation.add_message(Message(role=Role.USER, content=user_prompt))
        self._event_bus.publish(
            Event(EventType.PROMPT_RECEIVED, correlation_id, {"prompt": user_prompt})
        )

        for _ in range(self._max_tool_iterations):
            window = self._context_manager.build_window(self._conversation)
            response = self._llm_client.complete(window)
            self._event_bus.publish(
                Event(
                    EventType.LLM_RESPONSE_GENERATED,
                    correlation_id,
                    {"content": response.content},
                )
            )
            self._conversation.add_message(response)

            if response.tool_call is None:
                return response

            tool_result = self._tool_executor.execute(response.tool_call, correlation_id)
            self._conversation.add_message(
                Message(role=Role.TOOL, content=tool_result.output, tool_result=tool_result)
            )

        # Tool-iteration budget exhausted: return the last assistant message as-is.
        return response
