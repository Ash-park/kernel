"""Tests for `InMemoryEventBus` and `console_event_logger`."""

from __future__ import annotations

from kernel.adapters.events.console_event_logger import attach_console_logger
from kernel.adapters.events.in_memory_event_bus import InMemoryEventBus
from kernel.core.models import Event, EventType


def test_publish_calls_subscribed_handler() -> None:
    bus = InMemoryEventBus()
    received: list[Event] = []
    bus.subscribe(EventType.AGENT_STARTED, received.append)

    event = Event(type=EventType.AGENT_STARTED, correlation_id="c1")
    bus.publish(event)

    assert received == [event]


def test_publish_does_not_call_handlers_of_other_event_types() -> None:
    bus = InMemoryEventBus()
    received: list[Event] = []
    bus.subscribe(EventType.TOOL_STARTED, received.append)

    bus.publish(Event(type=EventType.AGENT_STARTED, correlation_id="c1"))

    assert received == []


def test_attach_console_logger_subscribes_to_every_event_type(capsys) -> None:  # noqa: ANN001
    bus = InMemoryEventBus()
    attach_console_logger(bus)

    bus.publish(Event(type=EventType.AGENT_STARTED, correlation_id="c1"))

    captured = capsys.readouterr()
    assert "agent_started" in captured.err
