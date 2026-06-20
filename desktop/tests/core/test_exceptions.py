"""
Unit tests for opencharge.core.exceptions.

Verifies the exception hierarchy, correct base class inheritance, and
that exception messages propagate correctly through the hierarchy.

Author:
    Ahmed Ghufran

License:
    Apache License 2.0
"""

import pytest

from opencharge.core.exceptions import (
    AuthorizationError,
    ConfigurationError,
    ContactorError,
    EventBusError,
    FaultError,
    HardwareError,
    InvalidStateTransitionError,
    LockError,
    OpenChargeError,
    SessionAlreadyActiveError,
    SessionError,
)


# =============================================================================
# Base class
# =============================================================================


class TestOpenChargeError:
    def test_is_exception(self) -> None:
        assert issubclass(OpenChargeError, Exception)

    def test_can_be_raised_and_caught(self) -> None:
        with pytest.raises(OpenChargeError):
            raise OpenChargeError("test")

    def test_message_preserved(self) -> None:
        msg = "something went wrong"
        exc = OpenChargeError(msg)
        assert str(exc) == msg


# =============================================================================
# Direct children of OpenChargeError
# =============================================================================


class TestConfigurationError:
    def test_inherits_from_opencharge_error(self) -> None:
        assert issubclass(ConfigurationError, OpenChargeError)

    def test_caught_as_opencharge_error(self) -> None:
        with pytest.raises(OpenChargeError):
            raise ConfigurationError("bad config")


class TestInvalidStateTransitionError:
    def test_inherits_from_opencharge_error(self) -> None:
        assert issubclass(InvalidStateTransitionError, OpenChargeError)

    def test_message_contains_states(self) -> None:
        exc = InvalidStateTransitionError("Invalid transition: OFFLINE → CHARGING")
        assert "OFFLINE" in str(exc)
        assert "CHARGING" in str(exc)

    def test_caught_as_opencharge_error(self) -> None:
        with pytest.raises(OpenChargeError):
            raise InvalidStateTransitionError("bad transition")

    def test_not_named_invalid_state_transition(self) -> None:
        """The old name without 'Error' suffix must not exist."""
        import opencharge.core.exceptions as exc_module
        assert not hasattr(exc_module, "InvalidStateTransition"), (
            "InvalidStateTransition (old name) must have been removed; "
            "use InvalidStateTransitionError instead."
        )


class TestEventBusError:
    def test_inherits_from_opencharge_error(self) -> None:
        assert issubclass(EventBusError, OpenChargeError)


class TestAuthorizationError:
    def test_inherits_from_opencharge_error(self) -> None:
        assert issubclass(AuthorizationError, OpenChargeError)


class TestFaultError:
    def test_inherits_from_opencharge_error(self) -> None:
        assert issubclass(FaultError, OpenChargeError)


# =============================================================================
# HardwareError branch
# =============================================================================


class TestHardwareError:
    def test_inherits_from_opencharge_error(self) -> None:
        assert issubclass(HardwareError, OpenChargeError)


class TestContactorError:
    def test_inherits_from_hardware_error(self) -> None:
        assert issubclass(ContactorError, HardwareError)

    def test_caught_as_opencharge_error(self) -> None:
        with pytest.raises(OpenChargeError):
            raise ContactorError("contactor stuck")

    def test_caught_as_hardware_error(self) -> None:
        with pytest.raises(HardwareError):
            raise ContactorError("contactor stuck")


class TestLockError:
    def test_inherits_from_hardware_error(self) -> None:
        assert issubclass(LockError, HardwareError)

    def test_caught_as_opencharge_error(self) -> None:
        with pytest.raises(OpenChargeError):
            raise LockError("lock jammed")


# =============================================================================
# SessionError branch
# =============================================================================


class TestSessionError:
    def test_inherits_from_opencharge_error(self) -> None:
        assert issubclass(SessionError, OpenChargeError)


class TestSessionAlreadyActiveError:
    def test_inherits_from_session_error(self) -> None:
        assert issubclass(SessionAlreadyActiveError, SessionError)

    def test_caught_as_opencharge_error(self) -> None:
        with pytest.raises(OpenChargeError):
            raise SessionAlreadyActiveError("already active")

    def test_caught_as_session_error(self) -> None:
        with pytest.raises(SessionError):
            raise SessionAlreadyActiveError("already active")


# =============================================================================
# Cross-hierarchy — catch-all works
# =============================================================================


class TestCatchAll:
    """A single 'except OpenChargeError' must catch any platform exception."""

    @pytest.mark.parametrize(
        "exc_class",
        [
            ConfigurationError,
            InvalidStateTransitionError,
            EventBusError,
            HardwareError,
            ContactorError,
            LockError,
            AuthorizationError,
            SessionError,
            SessionAlreadyActiveError,
            FaultError,
        ],
    )
    def test_caught_as_opencharge_error(self, exc_class: type) -> None:
        with pytest.raises(OpenChargeError):
            raise exc_class("test")
