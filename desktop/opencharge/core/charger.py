"""
OpenCharge Core — Charger Aggregate Root.

The Charger is the central domain object of the OpenCharge platform.
It is the DDD Aggregate Root responsible for coordinating all charging
operations — owning connectors, driving the state machine, owning the
event bus, and delegating to future services (authorization, sessions,
smart charging, load balancing).

Business logic only — no hardware access, no GUI dependencies,
no protocol dependencies.

Author:
    Ahmed Ghufran

License:
    Apache License 2.0
"""

from __future__ import annotations

from dataclasses import dataclass, field

from .connector import Connector
from .enums import ChargerState
from .event_bus import Event, EventBus, EventType
from .exceptions import InvalidStateTransitionError
from .state_machine import StateMachine


@dataclass
class Charger:
    """
    Represents one complete EV charging station (EVSE).

    The Charger owns the StateMachine, one or more Connectors, and the
    EventBus. All significant state changes are published as events so
    that the GUI, OCPP client, logger, and other observers can react
    without being directly coupled to the Charger.

    Attributes
    ----------
    charger_id:
        Unique charger identifier (maps to OCPP ChargePointId).
    name:
        Human-readable charger name.
    connectors:
        List of physical charging connectors managed by this charger.
    state_machine:
        Finite state machine controlling the charger lifecycle.
    event_bus:
        Publish/subscribe bus for all charger events. Injectable for
        testing — defaults to a new instance if not provided.
    firmware_version:
        Current firmware version string.
    serial_number:
        Hardware serial number.
    manufacturer:
        Charger manufacturer name.
    model:
        Charger model identifier.
    """

    charger_id: str
    name: str
    connectors: list[Connector]
    state_machine: StateMachine = field(default_factory=StateMachine)
    event_bus: EventBus = field(default_factory=EventBus)

    # These defaults will eventually be replaced by ConfigurationManager
    # values per OC-SDS-001 §5 (Configuration First principle).
    firmware_version: str = "0.2.0"
    serial_number: str = ""
    manufacturer: str = "OpenCharge"
    model: str = "OC-AC-001"

    _enabled: bool = field(default=True, init=False, repr=False)

    # -----------------------------------------------------------------
    # Properties
    # -----------------------------------------------------------------

    @property
    def state(self) -> ChargerState:
        """Current charger state from the FSM."""
        return self.state_machine.current_state

    @property
    def connector_count(self) -> int:
        """Number of connectors owned by this charger."""
        return len(self.connectors)

    @property
    def is_enabled(self) -> bool:
        """True if the charger has not been administratively disabled."""
        return self._enabled

    # -----------------------------------------------------------------
    # State machine
    # -----------------------------------------------------------------

    def transition(self, next_state: ChargerState) -> None:
        """
        Request a charger state transition.

        Delegates validation to the StateMachine and publishes a
        STATE_CHANGED event on success.

        Parameters
        ----------
        next_state:
            The requested target state.

        Raises
        ------
        InvalidStateTransitionError
            If the requested transition is not permitted.
        """
        previous_state = self.state
        self.state_machine.transition_to(next_state)  # raises on invalid
        self.event_bus.publish(
            Event(
                type=EventType.STATE_CHANGED,
                source=f"Charger:{self.charger_id}",
                payload={
                    "charger_id": self.charger_id,
                    "previous_state": previous_state.name,
                    "current_state": next_state.name,
                },
            )
        )

    def can_transition(self, next_state: ChargerState) -> bool:
        """Return True if the requested transition is currently valid."""
        return self.state_machine.can_transition(next_state)

    # -----------------------------------------------------------------
    # Connector management
    # -----------------------------------------------------------------

    def get_connector(self, connector_id: int) -> Connector:
        """
        Return the connector with the given ID.

        Parameters
        ----------
        connector_id:
            OCPP-style connector ID (1-based).

        Raises
        ------
        ValueError
            If no connector with connector_id exists.
        """
        for connector in self.connectors:
            if connector.connector_id == connector_id:
                return connector
        raise ValueError(
            f"Charger '{self.charger_id}': "
            f"connector {connector_id} does not exist."
        )

    # -----------------------------------------------------------------
    # Availability
    # -----------------------------------------------------------------

    def is_available(self) -> bool:
        """
        Return True if the charger can accept a new charging session.

        Both the administrative enable flag and FSM state must be
        satisfied simultaneously.
        """
        return self._enabled and self.state == ChargerState.AVAILABLE

    # -----------------------------------------------------------------
    # Administrative control
    # -----------------------------------------------------------------

    def enable(self) -> None:
        """
        Administratively enable the charger.

        Publishes a CHARGER_ENABLED event.
        """
        self._enabled = True
        self.event_bus.publish(
            Event(
                type=EventType.CHARGER_ENABLED,
                source=f"Charger:{self.charger_id}",
                payload={"charger_id": self.charger_id},
            )
        )

    def disable(self) -> None:
        """
        Administratively disable the charger.

        Publishes a CHARGER_DISABLED event. Does not affect an active
        charging session — the session must be stopped by the caller.
        """
        self._enabled = False
        self.event_bus.publish(
            Event(
                type=EventType.CHARGER_DISABLED,
                source=f"Charger:{self.charger_id}",
                payload={"charger_id": self.charger_id},
            )
        )

    # -----------------------------------------------------------------
    # Information
    # -----------------------------------------------------------------

    def summary(self) -> dict[str, object]:
        """
        Return a dictionary snapshot of the charger's current status.

        Suitable for logging, GUI rendering, and OCPP BootNotification.
        """
        return {
            "charger_id": self.charger_id,
            "name": self.name,
            "manufacturer": self.manufacturer,
            "model": self.model,
            "serial_number": self.serial_number,
            "firmware_version": self.firmware_version,
            "state": self.state.name,
            "enabled": self._enabled,
            "connector_count": self.connector_count,
        }

    # -----------------------------------------------------------------
    # Representation
    # -----------------------------------------------------------------

    def __str__(self) -> str:
        return (
            f"Charger("
            f"id='{self.charger_id}', "
            f"name='{self.name}', "
            f"state={self.state.name}, "
            f"connectors={self.connector_count})"
        )
