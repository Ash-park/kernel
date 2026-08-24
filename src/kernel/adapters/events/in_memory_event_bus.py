"""Synchronous, in-process implementation of the `EventBus` interface."""

from __future__ import annotations

from collections import defaultdict

from kernel.core.models import Event, EventType
from kernel.interfaces.event_bus import EventHandler


class InMemoryEventBus:
    """A simple dict-of-lists pub/sub bus. Publishing is synchronous and in-process.

    Sufficient for Phase 1 observability (console logging). A durable/async bus can
    implement the same `EventBus` protocol later without any change to `core/`.
    """

    def __init__(self) -> None:
        self._subscribers: dict[EventType, list[EventHandler]] = defaultdict(list)

    def publish(self, event: Event) -> None:
        """Call every handler subscribed to `event.type` with `event`."""
        for handler in self._subscribers.get(event.type, []):
            handler(event)

    def subscribe(self, event_type: EventType, handler: EventHandler) -> None:
        """Register `handler` to be invoked for future events of `event_type`."""
        self._subscribers[event_type].append(handler)
