"""An `EventBus` subscriber that prints a one-line log for every event to stderr."""

from __future__ import annotations

import sys

from kernel.core.models import Event, EventType
from kernel.interfaces.event_bus import EventBus


def log_event(event: Event) -> None:
    """Print a single human-readable line describing `event` to stderr."""
    line = f"[{event.timestamp.isoformat()}] {event.type.value} ({event.correlation_id})"
    print(line, file=sys.stderr)


def attach_console_logger(event_bus: EventBus) -> None:
    """Subscribe `log_event` to every `EventType` on `event_bus`."""
    for event_type in EventType:
        event_bus.subscribe(event_type, log_event)
