"""Tests for `ConversationState`."""

from __future__ import annotations

from kernel.core.conversation import ConversationState
from kernel.core.models import Message, Role


def test_add_message_appends_in_order() -> None:
    conversation = ConversationState()

    conversation.add_message(Message(role=Role.USER, content="first"))
    conversation.add_message(Message(role=Role.ASSISTANT, content="second"))

    messages = conversation.get_messages()
    assert [m.content for m in messages] == ["first", "second"]


def test_get_messages_returns_a_copy() -> None:
    conversation = ConversationState()
    conversation.add_message(Message(role=Role.USER, content="hello"))

    messages = conversation.get_messages()
    messages.append(Message(role=Role.USER, content="mutated"))

    assert len(conversation.get_messages()) == 1
