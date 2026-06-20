"""
OpenCharge Core — Finite State Machine.

Controls the charger lifecycle and enforces all state transition rules.
The StateMachine is the single gatekeeper for charger state — no
component may bypass it to set state directly.

Transition table per OC-SDS-001 §13.

Author:
    Ahmed Ghufran

License:
    Apache License 2.0
"""

from __future__ import annotations

from dataclasses import dataclass, field

from .enums import ChargerState
from .exceptions import InvalidStateTransitionError


@dataclass
class StateMachine:
    """
    OpenCharge Finite State Machine (FSM).

    Validates every state transition against the approved rule table
    from OC-SDS-001 §13. Invalid transitions raise
    InvalidStateTransitionError rather than silently corrupting state.

    Example
    -------
    >>> fsm = StateMachine()
    >>> fsm.transition_to(ChargerState.BOOTING)
    >>> fsm.transition_to(ChargerState.INITIALIZING)
    >>> fsm.transition_to(ChargerState.AVAILABLE)
    >>> fsm.current_state
    ChargerState.AVAILABLE
    """

    state: ChargerState = field(default=ChargerState.OFFLINE)

    # Populated in __post_init__ — not part of the public constructor.
    _transitions: dict[ChargerState, set[ChargerState]] = field(
        default_factory=dict, init=False, repr=False
    )

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
            # Vehicle connected — waiting for user to present credentials.
            ChargerState.OCCUPIED: {
                ChargerState.AUTHORIZING,
                ChargerState.AVAILABLE,   # vehicle unplugged before auth
                ChargerState.FAULTED,
            },
            # Authorization in progress (RFID, QR, OCPP remote).
            ChargerState.AUTHORIZING: {
                ChargerState.AUTHORIZED,  # credentials accepted
                ChargerState.OCCUPIED,    # credentials rejected — retry
                ChargerState.AVAILABLE,   # vehicle unplugged during auth
                ChargerState.FAULTED,
            },
            # Credentials accepted — preparing to energize connector.
            ChargerState.AUTHORIZED: {
                ChargerState.PREPARING,
                ChargerState.AVAILABLE,   # vehicle unplugged before contactor closes
                ChargerState.FAULTED,
            },
            # Contactor closing sequence in progress.
            ChargerState.PREPARING: {
                ChargerState.CHARGING,
                ChargerState.FAULTED,
            },
            # Energy transfer active.
            ChargerState.CHARGING: {
                ChargerState.SUSPENDED_EV,
                ChargerState.SUSPENDED_EVSE,
                ChargerState.FINISHING,
                ChargerState.FAULTED,
            },
            # EV has paused charging (e.g. battery management, timer).
            ChargerState.SUSPENDED_EV: {
                ChargerState.CHARGING,
                ChargerState.FINISHING,
                ChargerState.FAULTED,
            },
            # EVSE has paused charging (e.g. load balancing, OCPP command).
            ChargerState.SUSPENDED_EVSE: {
                ChargerState.CHARGING,
                ChargerState.FINISHING,
                ChargerState.FAULTED,
            },
            # Charging ending — contactor opening, session closing.
            ChargerState.FINISHING: {
                ChargerState.AVAILABLE,
                ChargerState.FAULTED,
            },
            # Administratively disabled.
            ChargerState.UNAVAILABLE: {
                ChargerState.AVAILABLE,
            },
            # Recovery paths from fault state.
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
        """Return the current charger state."""
        return self.state

    # -------------------------------------------------------------------------
    # Public API
    # -------------------------------------------------------------------------

    def can_transition(self, next_state: ChargerState) -> bool:
        """
        Return True if transitioning to next_state is permitted.

        Parameters
        ----------
        next_state:
            The requested target state.
        """
        return next_state in self._transitions.get(self.state, set())

    def transition_to(self, next_state: ChargerState) -> None:
        """
        Transition to next_state if permitted by the rule table.

        Parameters
        ----------
        next_state:
            The requested target state.

        Raises
        ------
        InvalidStateTransitionError
            If the transition is not in the approved rule table.
        """
        if not self.can_transition(next_state):
            raise InvalidStateTransitionError(
                f"Invalid transition: {self.state.name} → {next_state.name}"
            )
        self.state = next_state

    # -------------------------------------------------------------------------
    # Convenience predicates
    # -------------------------------------------------------------------------

    def is_available(self) -> bool:
        """Return True if the charger is ready to accept a vehicle."""
        return self.state == ChargerState.AVAILABLE

    def is_charging(self) -> bool:
        """Return True if energy transfer is active."""
        return self.state == ChargerState.CHARGING

    def is_faulted(self) -> bool:
        """Return True if the charger is in a fault state."""
        return self.state == ChargerState.FAULTED

    def is_occupied(self) -> bool:
        """Return True if a vehicle is connected."""
        return self.state in {
            ChargerState.OCCUPIED,
            ChargerState.AUTHORIZING,
            ChargerState.AUTHORIZED,
            ChargerState.PREPARING,
            ChargerState.CHARGING,
            ChargerState.SUSPENDED_EV,
            ChargerState.SUSPENDED_EVSE,
            ChargerState.FINISHING,
        }

    def reset(self) -> None:
        """Force-reset the FSM to OFFLINE without transition validation.

        Only to be used during controlled system shutdown or factory reset.
        """
        self.state = ChargerState.OFFLINE

    def __str__(self) -> str:
        return self.state.name
