"""
OpenCharge Event Bus
====================

A production-grade publish/subscribe event bus used throughout the
OpenCharge Core.

The EventBus provides loose coupling between modules by allowing
components to communicate using events instead of direct dependencies.

Design Goals
------------
- Thread-safe
- Strong typing
- Easy to unit test
- No global singleton
- Dependency Injection friendly
- Exception isolation
- Wildcard subscriptions
- One-shot subscriptions
- Minimal external dependencies

Author:
    OpenCharge Project

License:
    MIT
"""

from __future__ import annotations

import logging
import threading
from collections import defaultdict
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Callable, DefaultDict
from uuid import UUID, uuid4

EventHandler = Callable[["Event"], None]


class EventType(Enum):
    """
    Standard event types used throughout OpenCharge.

    New events should be added here to maintain a central catalogue.
    """

    SYSTEM_STARTED = "system.started"
    SYSTEM_STOPPED = "system.stopped"

    VEHICLE_CONNECTED = "vehicle.connected"
    VEHICLE_DISCONNECTED = "vehicle.disconnected"

    RFID_PRESENTED = "rfid.presented"

    CHARGING_STARTED = "charging.started"
    CHARGING_STOPPED = "charging.stopped"

    SESSION_STARTED = "session.started"
    SESSION_FINISHED = "session.finished"

    FAULT_OCCURRED = "fault.occurred"
    FAULT_CLEARED = "fault.cleared"

    METER_UPDATED = "meter.updated"

    CONFIG_CHANGED = "config.changed"

    HEARTBEAT = "heartbeat"

    ANY = "*"


@dataclass(slots=True, frozen=True)
class Event:
    """
    Represents a single event published on the EventBus.

    Attributes
    ----------
    id:
        Unique identifier.

    type:
        Event type.

    payload:
        Arbitrary event data.

    timestamp:
        UTC timestamp.

    source:
        Name of publishing component.
    """

    type: EventType

    payload: dict[str, Any] = field(default_factory=dict)

    source: str = "Unknown"

    id: UUID = field(default_factory=uuid4)

    timestamp: datetime = field(
        default_factory=lambda: datetime.now(timezone.utc)
    )


class EventBus:
    """
    Thread-safe Publish/Subscribe Event Bus.

    Example
    -------

    >>> bus = EventBus()
    >>> bus.subscribe(EventType.SYSTEM_STARTED, handler)
    >>> bus.publish(Event(EventType.SYSTEM_STARTED))
    """

    def __init__(self, logger: logging.Logger | None = None) -> None:
        self._logger = logger or logging.getLogger(__name__)

        self._lock = threading.RLock()

        self._subscribers: DefaultDict[
            EventType,
            list[EventHandler]
        ] = defaultdict(list)

        self._one_time_subscribers: DefaultDict[
            EventType,
            list[EventHandler]
        ] = defaultdict(list)

    # ------------------------------------------------------------------
    # Subscription
    # ------------------------------------------------------------------

    def subscribe(
        self,
        event_type: EventType,
        handler: EventHandler,
    ) -> None:
        """
        Register a handler.

        Parameters
        ----------
        event_type:
            Event to subscribe to.

        handler:
            Callback function.
        """

        with self._lock:
            if handler not in self._subscribers[event_type]:
                self._subscribers[event_type].append(handler)

                self._logger.debug(
                    "Subscribed %s to %s",
                    handler.__name__,
                    event_type.value,
                )

    def subscribe_once(
        self,
        event_type: EventType,
        handler: EventHandler,
    ) -> None:
        """
        Register a one-shot event handler.
        """

        with self._lock:
            self._one_time_subscribers[event_type].append(handler)

    def unsubscribe(
        self,
        event_type: EventType,
        handler: EventHandler,
    ) -> None:
        """
        Remove a subscriber.
        """

        with self._lock:

            if handler in self._subscribers[event_type]:
                self._subscribers[event_type].remove(handler)

            if handler in self._one_time_subscribers[event_type]:
                self._one_time_subscribers[event_type].remove(handler)

    # ------------------------------------------------------------------
    # Publishing
    # ------------------------------------------------------------------

    def publish(self, event: Event) -> None:
        """
        Publish an event.

        Exceptions inside handlers are isolated so that one faulty
        subscriber cannot affect others.
        """

        handlers: list[EventHandler]

        with self._lock:

            handlers = (
                list(self._subscribers[event.type])
                + list(self._one_time_subscribers[event.type])
                + list(self._subscribers[EventType.ANY])
            )

            self._one_time_subscribers[event.type].clear()

        self._logger.debug(
            "Publishing event %s from %s",
            event.type.value,
            event.source,
        )

        for handler in handlers:

            try:
                handler(event)

            except Exception:

                self._logger.exception(
                    "Unhandled exception in event handler '%s'",
                    handler.__name__,
                )

    # ------------------------------------------------------------------
    # Utility
    # ------------------------------------------------------------------

    def clear(self) -> None:
        """
        Remove all subscribers.

        Primarily used by unit tests.
        """

        with self._lock:
            self._subscribers.clear()
            self._one_time_subscribers.clear()

    def subscriber_count(
        self,
        event_type: EventType | None = None,
    ) -> int:
        """
        Return subscriber count.

        Parameters
        ----------
        event_type:
            If supplied, count subscribers for one event.
            Otherwise count all subscribers.
        """

        with self._lock:

            if event_type:

                return (
                    len(self._subscribers[event_type])
                    + len(self._one_time_subscribers[event_type])
                )

            return sum(
                len(v)
                for v in self._subscribers.values()
            ) + sum(
                len(v)
                for v in self._one_time_subscribers.values()
            )

    def has_subscribers(
        self,
        event_type: EventType,
    ) -> bool:
        """
        Check whether an event has subscribers.
        """

        return self.subscriber_count(event_type) > 0