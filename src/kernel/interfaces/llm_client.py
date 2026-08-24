"""Abstract contract for LLM providers. Core and CLI depend on this, never on a concrete SDK."""

from __future__ import annotations

from typing import Protocol

from kernel.core.models import Message


class LLMClient(Protocol):
    """A provider-agnostic chat completion client.

    Implementations (adapters) translate `Message` history into a provider-specific
    request and translate the provider's response back into a single `Message`.
    """

    def complete(self, messages: list[Message]) -> Message:
        """Return the next assistant `Message` given the conversation history so far."""
        ...
