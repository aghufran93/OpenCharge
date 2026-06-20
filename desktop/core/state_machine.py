"""
Generic finite state machine implementation.
"""

"""
OpenCharge
==========

File:
    state_machine.py

Description:
    Finite State Machine (FSM) for the OpenCharge platform.

The FSM is responsible for controlling the charger lifecycle and validating
all state transitions. It provides a single source of truth for charger
behaviour and is shared across the Desktop Simulator, IEC 61851,
OCPP implementation, Raspberry Pi HMI, and STM32 firmware.

Author:
    Ahmed Ghufran

License:
    Apache License 2.0
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Set

from .enums import ChargerState


# =============================================================================
# Exceptions
# =============================================================================


class InvalidStateTransitionError(Exception):
    """Raised when an invalid state transition is requested."""


# =============================================================================
# State Machine
# =============================================================================


@dataclass
class StateMachine:
    """
    OpenCharge Finite State Machine.

    Example
    -------
    >>> fsm = StateMachine()
    >>> fsm.transition_to(ChargerState.INITIALIZING)
    >>> fsm.transition_to(ChargerState.AVAILABLE)
    >>> print(fsm.state)
    ChargerState.AVAILABLE
    """

    state: ChargerState = ChargerState.OFFLINE

    # Allowed transitions
    _transitions: Dict[ChargerState, Set[ChargerState]] = None

    def __post_init__(self) -> None:
        self._transitions = {

            ChargerState.OFFLINE: {
                ChargerState.BOOTING,
            },

            ChargerState.BOOTING: {
                ChargerState.INITIALIZING,
                ChargerState.FAULTED,
            },

            ChargerState.INITIALIZING: {
                ChargerState.AVAILABLE,
                ChargerState.FAULTED,
            },

            ChargerState.AVAILABLE: {
                ChargerState.OCCUPIED,
                ChargerState.UNAVAILABLE,
                ChargerState.FAULTED,
            },

            ChargerState.OCCUPIED: {
                ChargerState.PREPARING,
                ChargerState.AVAILABLE,
                ChargerState.FAULTED,
            },

            ChargerState.PREPARING: {
                ChargerState.CHARGING,
                ChargerState.FAULTED,
            },

            ChargerState.CHARGING: {
                ChargerState.SUSPENDED_EV,
                ChargerState.SUSPENDED_EVSE,
                ChargerState.FINISHING,
                ChargerState.FAULTED,
            },

            ChargerState.SUSPENDED_EV: {
                ChargerState.CHARGING,
                ChargerState.FINISHING,
                ChargerState.FAULTED,
            },

            ChargerState.SUSPENDED_EVSE: {
                ChargerState.CHARGING,
                ChargerState.FINISHING,
                ChargerState.FAULTED,
            },

            ChargerState.FINISHING: {
                ChargerState.AVAILABLE,
                ChargerState.FAULTED,
            },

            ChargerState.UNAVAILABLE: {
                ChargerState.AVAILABLE,
            },

            ChargerState.FAULTED: {
                ChargerState.INITIALIZING,
                ChargerState.OFFLINE,
            },
        }

    # -------------------------------------------------------------------------
    # Properties
    # -------------------------------------------------------------------------

    @property
    def current_state(self) -> ChargerState:
        """Return current charger state."""
        return self.state

    # -------------------------------------------------------------------------
    # Public API
    # -------------------------------------------------------------------------

    def can_transition(self, next_state: ChargerState) -> bool:
        """
        Check if transition is allowed.

        Parameters
        ----------
        next_state:
            Requested charger state.

        Returns
        -------
        bool
            True if transition is valid.
        """
        return next_state in self._transitions.get(self.state, set())

    def transition_to(self, next_state: ChargerState) -> None:
        """
        Change charger state.

        Raises
        ------
        InvalidStateTransitionError
            If transition is not permitted.
        """
        if not self.can_transition(next_state):
            raise InvalidStateTransitionError(
                f"Invalid transition: "
                f"{self.state.name} -> {next_state.name}"
            )

        self.state = next_state

    # -------------------------------------------------------------------------
    # Helper Methods
    # -------------------------------------------------------------------------

    def reset(self) -> None:
        """Reset charger to OFFLINE state."""
        self.state = ChargerState.OFFLINE

    def is_available(self) -> bool:
        """Return True if charger is available."""
        return self.state == ChargerState.AVAILABLE

    def is_charging(self) -> bool:
        """Return True if charging is active."""
        return self.state == ChargerState.CHARGING

    def is_faulted(self) -> bool:
        """Return True if charger is faulted."""
        return self.state == ChargerState.FAULTED

    def __str__(self) -> str:
        return self.state.name