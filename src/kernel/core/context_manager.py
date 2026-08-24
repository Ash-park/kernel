"""Builds a bounded message window to send to the LLM from the full conversation history."""

from __future__ import annotations

from kernel.core.conversation import ConversationState
from kernel.core.models import Message

DEFAULT_MAX_MESSAGES = 20


class ContextManager:
    """Selects which messages from `ConversationState` are sent to the LLM.

    Phase 1 implements a single strategy — keep the most recent `max_messages` messages,
    dropping the oldest first. Token-aware or summarization-based strategies are future
    phase concerns (Phase 5, memory) and must not be added here.
    """

    def __init__(self, max_messages: int = DEFAULT_MAX_MESSAGES) -> None:
        self._max_messages = max_messages

    def build_window(self, conversation: ConversationState) -> list[Message]:
        """Return the bounded list of messages to send to the LLM for the next call."""
        messages = conversation.get_messages()
        if len(messages) <= self._max_messages:
            return messages
        return messages[-self._max_messages :]
