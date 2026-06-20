"""
OpenCharge Core — Event Bus.

A production-grade publish/subscribe event bus used throughout the
OpenCharge Core.

The EventBus provides loose coupling between modules by allowing
components to communicate through events rather than direct object
references.

Design Goals:
    - Thread-safe (RLock around all mutable state)
    - Strongly typed (EventType enum, typed Event dataclass)
    - Exception-isolated (one faulty handler never breaks others)
    - Dependency-injection friendly (no global singleton)
    - Wildcard subscriptions (EventType.ANY catches everything)
    - One-shot subscriptions (subscribe_once)
    - Minimal external dependencies (stdlib only)

Author:
    Ahmed Ghufran

License:
    Apache License 2.0
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
    Named events published on the OpenCharge EventBus.

    String values are used deliberately so that event names are
    human-readable in logs and serialized records.

    New events must be registered here to maintain a central catalogue
    and prevent naming collisions.
    """

    # System lifecycle
    SYSTEM_STARTED = "system.started"
    SYSTEM_STOPPED = "system.stopped"
    SYSTEM_FAULT = "system.fault"

    # Charger state
    STATE_CHANGED = "charger.state_changed"
    CHARGER_ENABLED = "charger.enabled"
    CHARGER_DISABLED = "charger.disabled"

    # Vehicle
    VEHICLE_CONNECTED = "vehicle.connected"
    VEHICLE_DISCONNECTED = "vehicle.disconnected"

    # Authorization
    RFID_PRESENTED = "rfid.presented"
    AUTHORIZATION_ACCEPTED = "authorization.accepted"
    AUTHORIZATION_REJECTED = "authorization.rejected"

    # Charging session
    SESSION_CREATED = "session.created"
    SESSION_STARTED = "session.started"
    SESSION_SUSPENDED = "session.suspended"
    SESSION_RESUMED = "session.resumed"
    SESSION_FINISHED = "session.finished"
    SESSION_FAILED = "session.failed"

    # Legacy aliases — kept for compatibility during transition
    CHARGING_STARTED = "charging.started"
    CHARGING_STOPPED = "charging.stopped"

    # Meter
    METER_UPDATED = "meter.updated"

    # Fault
    FAULT_OCCURRED = "fault.occurred"
    FAULT_CLEARED = "fault.cleared"

    # Configuration
    CONFIG_CHANGED = "config.changed"

    # OCPP
    OCPP_CONNECTED = "ocpp.connected"
    OCPP_DISCONNECTED = "ocpp.disconnected"
    HEARTBEAT = "ocpp.heartbeat"

    # Wildcard — receives every published event
    ANY = "*"


@dataclass(slots=True, frozen=True)
class Event:
    """
    Immutable event published on the EventBus.

    Attributes
    ----------
    type:
        Specific event type from the EventType catalogue.
    payload:
        Arbitrary event data. Must be JSON-serializable where possible.
    source:
        Name of the publishing component (e.g. "Charger:OC-001").
    id:
        Globally unique event identifier.
    timestamp:
        UTC timestamp of event creation.
    """

    type: EventType
    payload: dict[str, Any] = field(default_factory=dict)
    source: str = "unknown"
    id: UUID = field(default_factory=uuid4)
    timestamp: datetime = field(
        default_factory=lambda: datetime.now(timezone.utc)
    )


class EventBus:
    """
    Thread-safe Publish/Subscribe Event Bus.

    Usage
    -----
    >>> bus = EventBus()
    >>> bus.subscribe(EventType.STATE_CHANGED, my_handler)
    >>> bus.publish(Event(type=EventType.STATE_CHANGED, source="Charger"))
    """

    def __init__(self, logger: logging.Logger | None = None) -> None:
        self._logger = logger or logging.getLogger(__name__)
        self._lock = threading.RLock()
        self._subscribers: DefaultDict[EventType, list[EventHandler]] = defaultdict(list)
        self._one_time_subscribers: DefaultDict[EventType, list[EventHandler]] = defaultdict(list)

    # ------------------------------------------------------------------
    # Subscription
    # ------------------------------------------------------------------

    def subscribe(self, event_type: EventType, handler: EventHandler) -> None:
        """
        Register a persistent event handler.

        The same handler will not be registered twice for the same event.

        Parameters
        ----------
        event_type:
            Event to subscribe to. Use EventType.ANY to receive all events.
        handler:
            Callable accepting a single Event argument.
        """
        with self._lock:
            if handler not in self._subscribers[event_type]:
                self._subscribers[event_type].append(handler)
                self._logger.debug(
                    "Subscribed '%s' to '%s'",
                    handler.__name__,
                    event_type.value,
                )

    def subscribe_once(self, event_type: EventType, handler: EventHandler) -> None:
        """
        Register a one-shot event handler.

        The handler is removed after the first matching event is dispatched.
        """
        with self._lock:
            self._one_time_subscribers[event_type].append(handler)

    def unsubscribe(self, event_type: EventType, handler: EventHandler) -> None:
        """Remove a handler from both persistent and one-shot registries."""
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
        Publish an event to all registered subscribers.

        Exceptions raised inside handlers are caught and logged so that
        one faulty subscriber never prevents others from receiving the event.

        Parameters
        ----------
        event:
            The event to dispatch.
        """
        with self._lock:
            handlers: list[EventHandler] = (
                list(self._subscribers[event.type])
                + list(self._one_time_subscribers[event.type])
                + list(self._subscribers[EventType.ANY])
            )
            self._one_time_subscribers[event.type].clear()

        self._logger.debug(
            "Publishing '%s' from '%s'",
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
        """Remove all subscribers. Primarily used in unit tests."""
        with self._lock:
            self._subscribers.clear()
            self._one_time_subscribers.clear()

    def subscriber_count(self, event_type: EventType | None = None) -> int:
        """
        Return the number of registered handlers.

        Parameters
        ----------
        event_type:
            If provided, count handlers for that specific event only.
            Otherwise return the total across all event types.
        """
        with self._lock:
            if event_type is not None:
                return (
                    len(self._subscribers[event_type])
                    + len(self._one_time_subscribers[event_type])
                )
            return sum(len(v) for v in self._subscribers.values()) + sum(
                len(v) for v in self._one_time_subscribers.values()
            )

    def has_subscribers(self, event_type: EventType) -> bool:
        """Return True if the given event type has at least one subscriber."""
        return self.subscriber_count(event_type) > 0
