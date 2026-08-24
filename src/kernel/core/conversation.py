"""In-memory conversation history for a single agent session."""

from __future__ import annotations

from kernel.core.models import Message


class ConversationState:
    """Ordered history of `Message`s exchanged in one conversation.

    Holds no pruning/windowing logic — that responsibility belongs to `ContextManager`.
    """

    def __init__(self) -> None:
        self._messages: list[Message] = []

    def add_message(self, message: Message) -> None:
        """Append `message` to the end of the conversation history."""
        self._messages.append(message)

    def get_messages(self) -> list[Message]:
        """Return the full message history, oldest first."""
        return list(self._messages)
