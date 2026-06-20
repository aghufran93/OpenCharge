"""
Unit tests for opencharge.core.state_machine.

Covers the complete transition table from OC-SDS-001 §13, all invalid
transition rejections, convenience predicates, and the reset operation.

Author:
    Ahmed Ghufran

License:
    Apache License 2.0
"""

import pytest

from opencharge.core.enums import ChargerState
from opencharge.core.exceptions import InvalidStateTransitionError
from opencharge.core.state_machine import StateMachine


# =============================================================================
# Fixtures
# =============================================================================


@pytest.fixture()
def fsm() -> StateMachine:
    """Return a fresh StateMachine starting in OFFLINE."""
    return StateMachine()


@pytest.fixture()
def fsm_available(fsm: StateMachine) -> StateMachine:
    """Return a StateMachine advanced to AVAILABLE."""
    fsm.transition_to(ChargerState.BOOTING)
    fsm.transition_to(ChargerState.INITIALIZING)
    fsm.transition_to(ChargerState.AVAILABLE)
    return fsm


@pytest.fixture()
def fsm_charging(fsm_available: StateMachine) -> StateMachine:
    """Return a StateMachine advanced to CHARGING via the full auth path."""
    fsm_available.transition_to(ChargerState.OCCUPIED)
    fsm_available.transition_to(ChargerState.AUTHORIZING)
    fsm_available.transition_to(ChargerState.AUTHORIZED)
    fsm_available.transition_to(ChargerState.PREPARING)
    fsm_available.transition_to(ChargerState.CHARGING)
    return fsm_available


# =============================================================================
# Initial state
# =============================================================================


class TestInitialState:
    def test_starts_offline(self, fsm: StateMachine) -> None:
        assert fsm.current_state == ChargerState.OFFLINE

    def test_state_attribute_matches_property(self, fsm: StateMachine) -> None:
        assert fsm.state == fsm.current_state


# =============================================================================
# Happy path — full charging lifecycle per OC-SDS-001 §13
# =============================================================================


class TestFullChargingLifecycle:
    def test_boot_sequence(self, fsm: StateMachine) -> None:
        fsm.transition_to(ChargerState.BOOTING)
        assert fsm.current_state == ChargerState.BOOTING

        fsm.transition_to(ChargerState.INITIALIZING)
        assert fsm.current_state == ChargerState.INITIALIZING

        fsm.transition_to(ChargerState.AVAILABLE)
        assert fsm.current_state == ChargerState.AVAILABLE

    def test_vehicle_connects(self, fsm_available: StateMachine) -> None:
        fsm_available.transition_to(ChargerState.OCCUPIED)
        assert fsm_available.current_state == ChargerState.OCCUPIED

    def test_authorization_flow(self, fsm_available: StateMachine) -> None:
        fsm_available.transition_to(ChargerState.OCCUPIED)
        fsm_available.transition_to(ChargerState.AUTHORIZING)
        assert fsm_available.current_state == ChargerState.AUTHORIZING

        fsm_available.transition_to(ChargerState.AUTHORIZED)
        assert fsm_available.current_state == ChargerState.AUTHORIZED

    def test_preparing_to_charging(self, fsm_available: StateMachine) -> None:
        fsm_available.transition_to(ChargerState.OCCUPIED)
        fsm_available.transition_to(ChargerState.AUTHORIZING)
        fsm_available.transition_to(ChargerState.AUTHORIZED)
        fsm_available.transition_to(ChargerState.PREPARING)
        fsm_available.transition_to(ChargerState.CHARGING)
        assert fsm_available.current_state == ChargerState.CHARGING

    def test_charging_to_finishing_to_available(
        self, fsm_charging: StateMachine
    ) -> None:
        fsm_charging.transition_to(ChargerState.FINISHING)
        fsm_charging.transition_to(ChargerState.AVAILABLE)
        assert fsm_charging.current_state == ChargerState.AVAILABLE


# =============================================================================
# Authorization rejection path
# =============================================================================


class TestAuthorizationRejection:
    def test_rejected_auth_returns_to_occupied(
        self, fsm_available: StateMachine
    ) -> None:
        """When credentials are rejected the vehicle is still connected → OCCUPIED."""
        fsm_available.transition_to(ChargerState.OCCUPIED)
        fsm_available.transition_to(ChargerState.AUTHORIZING)
        fsm_available.transition_to(ChargerState.OCCUPIED)
        assert fsm_available.current_state == ChargerState.OCCUPIED

    def test_vehicle_unplugs_during_auth(self, fsm_available: StateMachine) -> None:
        """Vehicle unplugs while auth is in progress → AVAILABLE."""
        fsm_available.transition_to(ChargerState.OCCUPIED)
        fsm_available.transition_to(ChargerState.AUTHORIZING)
        fsm_available.transition_to(ChargerState.AVAILABLE)
        assert fsm_available.current_state == ChargerState.AVAILABLE

    def test_vehicle_unplugs_after_auth(self, fsm_available: StateMachine) -> None:
        """Vehicle unplugs after authorization but before contactor closes → AVAILABLE."""
        fsm_available.transition_to(ChargerState.OCCUPIED)
        fsm_available.transition_to(ChargerState.AUTHORIZING)
        fsm_available.transition_to(ChargerState.AUTHORIZED)
        fsm_available.transition_to(ChargerState.AVAILABLE)
        assert fsm_available.current_state == ChargerState.AVAILABLE


# =============================================================================
# Suspension paths
# =============================================================================


class TestSuspension:
    def test_charging_to_suspended_ev(self, fsm_charging: StateMachine) -> None:
        fsm_charging.transition_to(ChargerState.SUSPENDED_EV)
        assert fsm_charging.current_state == ChargerState.SUSPENDED_EV

    def test_charging_to_suspended_evse(self, fsm_charging: StateMachine) -> None:
        fsm_charging.transition_to(ChargerState.SUSPENDED_EVSE)
        assert fsm_charging.current_state == ChargerState.SUSPENDED_EVSE

    def test_suspended_ev_resumes(self, fsm_charging: StateMachine) -> None:
        fsm_charging.transition_to(ChargerState.SUSPENDED_EV)
        fsm_charging.transition_to(ChargerState.CHARGING)
        assert fsm_charging.current_state == ChargerState.CHARGING

    def test_suspended_evse_resumes(self, fsm_charging: StateMachine) -> None:
        fsm_charging.transition_to(ChargerState.SUSPENDED_EVSE)
        fsm_charging.transition_to(ChargerState.CHARGING)
        assert fsm_charging.current_state == ChargerState.CHARGING

    def test_suspended_ev_to_finishing(self, fsm_charging: StateMachine) -> None:
        fsm_charging.transition_to(ChargerState.SUSPENDED_EV)
        fsm_charging.transition_to(ChargerState.FINISHING)
        assert fsm_charging.current_state == ChargerState.FINISHING

    def test_suspended_evse_to_finishing(self, fsm_charging: StateMachine) -> None:
        fsm_charging.transition_to(ChargerState.SUSPENDED_EVSE)
        fsm_charging.transition_to(ChargerState.FINISHING)
        assert fsm_charging.current_state == ChargerState.FINISHING


# =============================================================================
# Fault paths
# =============================================================================


class TestFaultPaths:
    @pytest.mark.parametrize(
        "start_state,setup",
        [
            (ChargerState.BOOTING, lambda f: f.transition_to(ChargerState.BOOTING)),
            (
                ChargerState.INITIALIZING,
                lambda f: [
                    f.transition_to(ChargerState.BOOTING),
                    f.transition_to(ChargerState.INITIALIZING),
                ],
            ),
            (
                ChargerState.AVAILABLE,
                lambda f: [
                    f.transition_to(ChargerState.BOOTING),
                    f.transition_to(ChargerState.INITIALIZING),
                    f.transition_to(ChargerState.AVAILABLE),
                ],
            ),
        ],
    )
    def test_fault_from_multiple_states(
        self, fsm: StateMachine, start_state: ChargerState, setup: object
    ) -> None:
        setup(fsm)
        fsm.transition_to(ChargerState.FAULTED)
        assert fsm.current_state == ChargerState.FAULTED

    def test_fault_recovery_to_initializing(self, fsm_available: StateMachine) -> None:
        fsm_available.transition_to(ChargerState.FAULTED)
        fsm_available.transition_to(ChargerState.INITIALIZING)
        assert fsm_available.current_state == ChargerState.INITIALIZING

    def test_fault_recovery_to_offline(self, fsm_available: StateMachine) -> None:
        fsm_available.transition_to(ChargerState.FAULTED)
        fsm_available.transition_to(ChargerState.OFFLINE)
        assert fsm_available.current_state == ChargerState.OFFLINE

    def test_fault_from_charging(self, fsm_charging: StateMachine) -> None:
        fsm_charging.transition_to(ChargerState.FAULTED)
        assert fsm_charging.current_state == ChargerState.FAULTED


# =============================================================================
# Unavailable path
# =============================================================================


class TestUnavailablePath:
    def test_available_to_unavailable(self, fsm_available: StateMachine) -> None:
        fsm_available.transition_to(ChargerState.UNAVAILABLE)
        assert fsm_available.current_state == ChargerState.UNAVAILABLE

    def test_unavailable_returns_to_available(
        self, fsm_available: StateMachine
    ) -> None:
        fsm_available.transition_to(ChargerState.UNAVAILABLE)
        fsm_available.transition_to(ChargerState.AVAILABLE)
        assert fsm_available.current_state == ChargerState.AVAILABLE


# =============================================================================
# Invalid transitions
# =============================================================================


class TestInvalidTransitions:
    def test_offline_to_charging_is_invalid(self, fsm: StateMachine) -> None:
        with pytest.raises(InvalidStateTransitionError):
            fsm.transition_to(ChargerState.CHARGING)

    def test_offline_to_available_is_invalid(self, fsm: StateMachine) -> None:
        with pytest.raises(InvalidStateTransitionError):
            fsm.transition_to(ChargerState.AVAILABLE)

    def test_available_to_charging_skips_auth(
        self, fsm_available: StateMachine
    ) -> None:
        """Jumping directly to CHARGING without authorization must be rejected."""
        with pytest.raises(InvalidStateTransitionError):
            fsm_available.transition_to(ChargerState.CHARGING)

    def test_available_to_preparing_without_occupied(
        self, fsm_available: StateMachine
    ) -> None:
        with pytest.raises(InvalidStateTransitionError):
            fsm_available.transition_to(ChargerState.PREPARING)

    def test_occupied_to_charging_skips_auth(
        self, fsm_available: StateMachine
    ) -> None:
        """OCCUPIED must not transition to CHARGING — must go through AUTHORIZING."""
        fsm_available.transition_to(ChargerState.OCCUPIED)
        with pytest.raises(InvalidStateTransitionError):
            fsm_available.transition_to(ChargerState.CHARGING)

    def test_occupied_to_preparing_skips_auth(
        self, fsm_available: StateMachine
    ) -> None:
        """OCCUPIED → PREPARING is not valid — must authenticate first."""
        fsm_available.transition_to(ChargerState.OCCUPIED)
        with pytest.raises(InvalidStateTransitionError):
            fsm_available.transition_to(ChargerState.PREPARING)

    def test_charging_to_available_direct(self, fsm_charging: StateMachine) -> None:
        """Must go through FINISHING, not jump to AVAILABLE."""
        with pytest.raises(InvalidStateTransitionError):
            fsm_charging.transition_to(ChargerState.AVAILABLE)

    def test_error_message_includes_state_names(self, fsm: StateMachine) -> None:
        with pytest.raises(InvalidStateTransitionError, match="OFFLINE"):
            fsm.transition_to(ChargerState.CHARGING)


# =============================================================================
# can_transition
# =============================================================================


class TestCanTransition:
    def test_valid_transition_returns_true(self, fsm: StateMachine) -> None:
        assert fsm.can_transition(ChargerState.BOOTING) is True

    def test_invalid_transition_returns_false(self, fsm: StateMachine) -> None:
        assert fsm.can_transition(ChargerState.CHARGING) is False

    def test_does_not_change_state(self, fsm: StateMachine) -> None:
        fsm.can_transition(ChargerState.BOOTING)
        assert fsm.current_state == ChargerState.OFFLINE


# =============================================================================
# Predicates
# =============================================================================


class TestPredicates:
    def test_is_available_true(self, fsm_available: StateMachine) -> None:
        assert fsm_available.is_available() is True

    def test_is_available_false_when_offline(self, fsm: StateMachine) -> None:
        assert fsm.is_available() is False

    def test_is_charging_true(self, fsm_charging: StateMachine) -> None:
        assert fsm_charging.is_charging() is True

    def test_is_charging_false_when_available(
        self, fsm_available: StateMachine
    ) -> None:
        assert fsm_available.is_charging() is False

    def test_is_faulted_true(self, fsm_available: StateMachine) -> None:
        fsm_available.transition_to(ChargerState.FAULTED)
        assert fsm_available.is_faulted() is True

    def test_is_faulted_false_when_available(
        self, fsm_available: StateMachine
    ) -> None:
        assert fsm_available.is_faulted() is False

    def test_is_occupied_true_in_authorizing(
        self, fsm_available: StateMachine
    ) -> None:
        fsm_available.transition_to(ChargerState.OCCUPIED)
        fsm_available.transition_to(ChargerState.AUTHORIZING)
        assert fsm_available.is_occupied() is True

    def test_is_occupied_true_in_charging(self, fsm_charging: StateMachine) -> None:
        assert fsm_charging.is_occupied() is True

    def test_is_occupied_false_when_available(
        self, fsm_available: StateMachine
    ) -> None:
        assert fsm_available.is_occupied() is False


# =============================================================================
# reset
# =============================================================================


class TestReset:
    def test_reset_from_charging(self, fsm_charging: StateMachine) -> None:
        fsm_charging.reset()
        assert fsm_charging.current_state == ChargerState.OFFLINE

    def test_reset_from_available(self, fsm_available: StateMachine) -> None:
        fsm_available.reset()
        assert fsm_available.current_state == ChargerState.OFFLINE

    def test_reset_allows_normal_boot_after(self, fsm_charging: StateMachine) -> None:
        fsm_charging.reset()
        fsm_charging.transition_to(ChargerState.BOOTING)
        assert fsm_charging.current_state == ChargerState.BOOTING


# =============================================================================
# String representation
# =============================================================================


class TestStringRepresentation:
    def test_str_returns_state_name(self, fsm: StateMachine) -> None:
        assert str(fsm) == "OFFLINE"

    def test_str_updates_after_transition(self, fsm: StateMachine) -> None:
        fsm.transition_to(ChargerState.BOOTING)
        assert str(fsm) == "BOOTING"
