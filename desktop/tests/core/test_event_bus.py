"""
Unit tests for opencharge.core.event_bus.

Covers subscription, publishing, one-shot handlers, wildcard (ANY)
subscriptions, exception isolation, thread safety, and utility methods.

Author:
    Ahmed Ghufran

License:
    Apache License 2.0
"""

from __future__ import annotations

import threading
from typing import Any
from uuid import UUID

import pytest

from opencharge.core.event_bus import Event, EventBus, EventType


# =============================================================================
# Fixtures
# =============================================================================


@pytest.fixture()
def bus() -> EventBus:
    """Return a fresh EventBus for each test."""
    return EventBus()


def make_event(event_type: EventType = EventType.STATE_CHANGED, **payload: Any) -> Event:
    """Helper: create a minimal Event."""
    return Event(type=event_type, source="test", payload=dict(payload))


# =============================================================================
# Event dataclass
# =============================================================================


class TestEvent:
    def test_event_has_unique_id(self) -> None:
        e1 = make_event()
        e2 = make_event()
        assert e1.id != e2.id

    def test_event_id_is_uuid(self) -> None:
        e = make_event()
        assert isinstance(e.id, UUID)

    def test_event_is_immutable(self) -> None:
        e = make_event()
        with pytest.raises(AttributeError):
            e.source = "other"  # type: ignore[misc]

    def test_event_timestamp_is_utc(self) -> None:
        import datetime
        e = make_event()
        assert e.timestamp.tzinfo == datetime.timezone.utc

    def test_event_default_payload_is_empty_dict(self) -> None:
        e = Event(type=EventType.HEARTBEAT)
        assert e.payload == {}

    def test_event_type_is_set(self) -> None:
        e = make_event(EventType.VEHICLE_CONNECTED)
        assert e.type == EventType.VEHICLE_CONNECTED


# =============================================================================
# subscribe / publish
# =============================================================================


class TestSubscribePublish:
    def test_handler_is_called_on_publish(self, bus: EventBus) -> None:
        received: list[Event] = []
        bus.subscribe(EventType.STATE_CHANGED, received.append)
        bus.publish(make_event(EventType.STATE_CHANGED))
        assert len(received) == 1

    def test_handler_receives_correct_event(self, bus: EventBus) -> None:
        received: list[Event] = []
        bus.subscribe(EventType.STATE_CHANGED, received.append)
        evt = make_event(EventType.STATE_CHANGED, key="value")
        bus.publish(evt)
        assert received[0] is evt

    def test_multiple_handlers_all_called(self, bus: EventBus) -> None:
        calls: list[int] = []
        bus.subscribe(EventType.STATE_CHANGED, lambda e: calls.append(1))
        bus.subscribe(EventType.STATE_CHANGED, lambda e: calls.append(2))
        bus.publish(make_event(EventType.STATE_CHANGED))
        assert calls == [1, 2]

    def test_unrelated_event_not_dispatched(self, bus: EventBus) -> None:
        received: list[Event] = []
        bus.subscribe(EventType.STATE_CHANGED, received.append)
        bus.publish(make_event(EventType.HEARTBEAT))
        assert received == []

    def test_duplicate_subscribe_is_idempotent(self, bus: EventBus) -> None:
        calls: list[int] = []
        handler = lambda e: calls.append(1)  # noqa: E731
        bus.subscribe(EventType.STATE_CHANGED, handler)
        bus.subscribe(EventType.STATE_CHANGED, handler)
        bus.publish(make_event(EventType.STATE_CHANGED))
        assert len(calls) == 1


# =============================================================================
# unsubscribe
# =============================================================================


class TestUnsubscribe:
    def test_handler_not_called_after_unsubscribe(self, bus: EventBus) -> None:
        received: list[Event] = []
        bus.subscribe(EventType.STATE_CHANGED, received.append)
        bus.unsubscribe(EventType.STATE_CHANGED, received.append)
        bus.publish(make_event(EventType.STATE_CHANGED))
        assert received == []

    def test_unsubscribe_unknown_handler_does_not_raise(
        self, bus: EventBus
    ) -> None:
        bus.unsubscribe(EventType.STATE_CHANGED, lambda e: None)

    def test_only_target_handler_removed(self, bus: EventBus) -> None:
        calls: list[int] = []
        h1 = lambda e: calls.append(1)  # noqa: E731
        h2 = lambda e: calls.append(2)  # noqa: E731
        bus.subscribe(EventType.STATE_CHANGED, h1)
        bus.subscribe(EventType.STATE_CHANGED, h2)
        bus.unsubscribe(EventType.STATE_CHANGED, h1)
        bus.publish(make_event(EventType.STATE_CHANGED))
        assert calls == [2]


# =============================================================================
# subscribe_once
# =============================================================================


class TestSubscribeOnce:
    def test_handler_called_exactly_once(self, bus: EventBus) -> None:
        calls: list[int] = []
        bus.subscribe_once(EventType.STATE_CHANGED, lambda e: calls.append(1))
        bus.publish(make_event(EventType.STATE_CHANGED))
        bus.publish(make_event(EventType.STATE_CHANGED))
        assert len(calls) == 1

    def test_persistent_handler_called_after_one_shot_expires(
        self, bus: EventBus
    ) -> None:
        one_shot: list[int] = []
        persistent: list[int] = []
        bus.subscribe_once(EventType.STATE_CHANGED, lambda e: one_shot.append(1))
        bus.subscribe(EventType.STATE_CHANGED, lambda e: persistent.append(1))
        bus.publish(make_event(EventType.STATE_CHANGED))
        bus.publish(make_event(EventType.STATE_CHANGED))
        assert len(one_shot) == 1
        assert len(persistent) == 2


# =============================================================================
# Wildcard (ANY)
# =============================================================================


class TestWildcard:
    def test_any_receives_all_events(self, bus: EventBus) -> None:
        received: list[Event] = []
        bus.subscribe(EventType.ANY, received.append)
        bus.publish(make_event(EventType.STATE_CHANGED))
        bus.publish(make_event(EventType.HEARTBEAT))
        bus.publish(make_event(EventType.FAULT_OCCURRED))
        assert len(received) == 3

    def test_any_does_not_duplicate_specific_handler(self, bus: EventBus) -> None:
        specific: list[Event] = []
        wildcard: list[Event] = []
        bus.subscribe(EventType.STATE_CHANGED, specific.append)
        bus.subscribe(EventType.ANY, wildcard.append)
        bus.publish(make_event(EventType.STATE_CHANGED))
        assert len(specific) == 1
        assert len(wildcard) == 1


# =============================================================================
# Exception isolation
# =============================================================================


class TestExceptionIsolation:
    def test_faulty_handler_does_not_prevent_others(self, bus: EventBus) -> None:
        called: list[int] = []

        def bad_handler(event: Event) -> None:
            raise RuntimeError("simulated failure")

        def good_handler(event: Event) -> None:
            called.append(1)

        bus.subscribe(EventType.STATE_CHANGED, bad_handler)
        bus.subscribe(EventType.STATE_CHANGED, good_handler)
        bus.publish(make_event(EventType.STATE_CHANGED))
        assert called == [1]

    def test_multiple_faulty_handlers_still_call_good_ones(
        self, bus: EventBus
    ) -> None:
        called: list[int] = []

        bus.subscribe(EventType.STATE_CHANGED, lambda e: (_ for _ in ()).throw(ValueError("bad")))
        bus.subscribe(EventType.STATE_CHANGED, lambda e: called.append(1))
        bus.subscribe(EventType.STATE_CHANGED, lambda e: (_ for _ in ()).throw(KeyError("bad")))
        bus.subscribe(EventType.STATE_CHANGED, lambda e: called.append(2))

        bus.publish(make_event(EventType.STATE_CHANGED))
        assert called == [1, 2]


# =============================================================================
# Thread safety
# =============================================================================


class TestThreadSafety:
    def test_concurrent_publish_does_not_raise(self, bus: EventBus) -> None:
        received: list[Event] = []
        lock = threading.Lock()

        def handler(event: Event) -> None:
            with lock:
                received.append(event)

        bus.subscribe(EventType.STATE_CHANGED, handler)

        threads = [
            threading.Thread(
                target=bus.publish,
                args=(make_event(EventType.STATE_CHANGED),),
            )
            for _ in range(50)
        ]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        assert len(received) == 50

    def test_concurrent_subscribe_does_not_raise(self, bus: EventBus) -> None:
        def subscribe_and_publish() -> None:
            bus.subscribe(EventType.STATE_CHANGED, lambda e: None)
            bus.publish(make_event(EventType.STATE_CHANGED))

        threads = [threading.Thread(target=subscribe_and_publish) for _ in range(20)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()


# =============================================================================
# Utility methods
# =============================================================================


class TestUtility:
    def test_subscriber_count_zero_initially(self, bus: EventBus) -> None:
        assert bus.subscriber_count(EventType.STATE_CHANGED) == 0

    def test_subscriber_count_after_subscribe(self, bus: EventBus) -> None:
        bus.subscribe(EventType.STATE_CHANGED, lambda e: None)
        assert bus.subscriber_count(EventType.STATE_CHANGED) == 1

    def test_subscriber_count_all_events(self, bus: EventBus) -> None:
        bus.subscribe(EventType.STATE_CHANGED, lambda e: None)
        bus.subscribe(EventType.HEARTBEAT, lambda e: None)
        assert bus.subscriber_count() == 2

    def test_has_subscribers_true(self, bus: EventBus) -> None:
        bus.subscribe(EventType.STATE_CHANGED, lambda e: None)
        assert bus.has_subscribers(EventType.STATE_CHANGED) is True

    def test_has_subscribers_false(self, bus: EventBus) -> None:
        assert bus.has_subscribers(EventType.STATE_CHANGED) is False

    def test_clear_removes_all_subscribers(self, bus: EventBus) -> None:
        bus.subscribe(EventType.STATE_CHANGED, lambda e: None)
        bus.subscribe(EventType.HEARTBEAT, lambda e: None)
        bus.clear()
        assert bus.subscriber_count() == 0

    def test_clear_one_shot_subscribers(self, bus: EventBus) -> None:
        bus.subscribe_once(EventType.STATE_CHANGED, lambda e: None)
        bus.clear()
        assert bus.subscriber_count(EventType.STATE_CHANGED) == 0

    def test_subscriber_count_includes_one_shot(self, bus: EventBus) -> None:
        bus.subscribe_once(EventType.STATE_CHANGED, lambda e: None)
        assert bus.subscriber_count(EventType.STATE_CHANGED) == 1
