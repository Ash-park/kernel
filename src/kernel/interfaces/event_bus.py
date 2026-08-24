"""Abstract contract for the event bus used for observability throughout the runtime."""

from __future__ import annotations

from collections.abc import Callable
from typing import Protocol

from kernel.core.models import Event, EventType

EventHandler = Callable[[Event], None]


class EventBus(Protocol):
    """A publish/subscribe channel for runtime `Event`s.

    Phase 1 ships a synchronous in-memory implementation; later phases may add a durable
    or async bus behind this same interface without changing `core/`.
    """

    def publish(self, event: Event) -> None:
        """Publish an event to all subscribers registered for its `EventType`."""
        ...

    def subscribe(self, event_type: EventType, handler: EventHandler) -> None:
        """Register `handler` to be called whenever an event of `event_type` is published."""
        ...
