"""Tests for `ContextManager`."""

from __future__ import annotations

from kernel.core.context_manager import ContextManager
from kernel.core.conversation import ConversationState
from kernel.core.models import Message, Role


def _conversation_with(n: int) -> ConversationState:
    conversation = ConversationState()
    for i in range(n):
        conversation.add_message(Message(role=Role.USER, content=str(i)))
    return conversation


def test_build_window_returns_all_messages_when_under_limit() -> None:
    context_manager = ContextManager(max_messages=5)
    conversation = _conversation_with(3)

    window = context_manager.build_window(conversation)

    assert [m.content for m in window] == ["0", "1", "2"]


def test_build_window_drops_oldest_when_over_limit() -> None:
    context_manager = ContextManager(max_messages=2)
    conversation = _conversation_with(5)

    window = context_manager.build_window(conversation)

    assert [m.content for m in window] == ["3", "4"]
