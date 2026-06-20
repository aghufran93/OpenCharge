"""
OpenCharge Charger aggregate root.
"""

"""
OpenCharge
==========

File:
    charger.py

Description:
    Represents an EV Charger (EVSE).

The Charger is the central object within the OpenCharge Core.
It coordinates the state machine, connectors, charging sessions,
metering, authorization, and future protocol integrations.

The Charger contains business logic only.
It does not directly interact with GPIO, UART, or hardware drivers.

Author:
    Ahmed Ghufran

License:
    Apache License 2.0
"""

from __future__ import annotations

from dataclasses import dataclass, field

from .connector import Connector
from .enums import ChargerState
from .state_machine import StateMachine


@dataclass
class Charger:
    """
    Represents a complete EV charger (EVSE).

    A charger owns one or more connectors and a finite state machine.
    """

    charger_id: str

    name: str

    connectors: list[Connector]

    state_machine: StateMachine = field(default_factory=StateMachine)

    firmware_version: str = "0.1.0"

    serial_number: str = ""

    manufacturer: str = "OpenCharge"

    model: str = "OC-AC-001"

    available: bool = True

    # -----------------------------------------------------------------
    # Properties
    # -----------------------------------------------------------------

    @property
    def state(self) -> ChargerState:
        """Current charger state."""
        return self.state_machine.current_state

    @property
    def connector_count(self) -> int:
        """Number of connectors."""
        return len(self.connectors)

    # -----------------------------------------------------------------
    # State Machine
    # -----------------------------------------------------------------

    def transition(self, next_state: ChargerState) -> None:
        """
        Request a charger state transition.
        """
        self.state_machine.transition_to(next_state)

    # -----------------------------------------------------------------
    # Connector Management
    # -----------------------------------------------------------------

    def get_connector(self, connector_id: int) -> Connector:
        """
        Return connector by ID.

        Raises
        ------
        ValueError
            If connector does not exist.
        """

        for connector in self.connectors:

            if connector.connector_id == connector_id:
                return connector

        raise ValueError(f"Connector {connector_id} not found.")

    # -----------------------------------------------------------------
    # Status
    # -----------------------------------------------------------------

    def is_available(self) -> bool:
        """
        Return True if charger can accept a new session.
        """
        return (
            self.available
            and self.state == ChargerState.AVAILABLE
        )

    # -----------------------------------------------------------------
    # Control
    # -----------------------------------------------------------------

    def enable(self) -> None:
        """Enable charger."""
        self.available = True

    def disable(self) -> None:
        """Disable charger."""
        self.available = False

    # -----------------------------------------------------------------
    # Information
    # -----------------------------------------------------------------

    def summary(self) -> dict:
        """
        Return charger summary.
        """

        return {
            "charger_id": self.charger_id,
            "name": self.name,
            "manufacturer": self.manufacturer,
            "model": self.model,
            "serial_number": self.serial_number,
            "firmware": self.firmware_version,
            "state": self.state.name,
            "available": self.available,
            "connectors": self.connector_count,
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