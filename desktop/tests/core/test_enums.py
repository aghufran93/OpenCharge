"""
Unit tests for opencharge.core.enums.

Verifies that every enumeration contains the values required by
OC-SDS-001 and that no naming collisions exist between enum classes.

Author:
    Ahmed Ghufran

License:
    Apache License 2.0
"""

import pytest

from opencharge.core.enums import (
    AuthorizationMethod,
    AuthorizationStatus,
    ChargerState,
    ConnectorStatus,
    ConnectorType,
    ContactorState,
    EventCategory,
    FaultCode,
    FaultSeverity,
    IEC61851State,
    LockState,
    LogLevel,
    MeterUnit,
    OCPPStatus,
    SessionStatus,
    VehicleStatus,
)
from opencharge.core.event_bus import EventType


# =============================================================================
# ChargerState
# =============================================================================


class TestChargerState:
    """ChargerState covers all lifecycle states defined in OC-SDS-001 §13."""

    def test_all_required_states_present(self) -> None:
        required = {
            "OFFLINE",
            "BOOTING",
            "INITIALIZING",
            "AVAILABLE",
            "OCCUPIED",
            "AUTHORIZING",
            "AUTHORIZED",
            "PREPARING",
            "CHARGING",
            "SUSPENDED_EV",
            "SUSPENDED_EVSE",
            "FINISHING",
            "FAULTED",
            "UNAVAILABLE",
        }
        actual = {s.name for s in ChargerState}
        assert required == actual

    def test_authorizing_state_exists(self) -> None:
        assert ChargerState.AUTHORIZING is not None

    def test_authorized_state_exists(self) -> None:
        assert ChargerState.AUTHORIZED is not None

    def test_states_are_unique(self) -> None:
        values = [s.value for s in ChargerState]
        assert len(values) == len(set(values))

    def test_states_are_comparable_by_identity(self) -> None:
        assert ChargerState.AVAILABLE is ChargerState.AVAILABLE
        assert ChargerState.CHARGING is not ChargerState.AVAILABLE


# =============================================================================
# SessionStatus
# =============================================================================


class TestSessionStatus:
    """SessionStatus must match the session lifecycle defined in OC-SDS-001 §14."""

    def test_all_sds_states_present(self) -> None:
        required = {
            "IDLE",
            "CREATED",
            "AUTHORIZED",
            "PREPARING",
            "ACTIVE",
            "SUSPENDED",
            "STOPPING",
            "COMPLETED",
            "FAILED",
            "CANCELLED",
        }
        actual = {s.name for s in SessionStatus}
        assert required == actual

    def test_created_state_present(self) -> None:
        assert SessionStatus.CREATED is not None

    def test_completed_replaces_finished(self) -> None:
        """SDS §14 uses COMPLETED, not FINISHED."""
        assert hasattr(SessionStatus, "COMPLETED")
        assert not hasattr(SessionStatus, "FINISHED")

    def test_suspended_replaces_paused(self) -> None:
        """SDS §14 uses SUSPENDED, not PAUSED."""
        assert hasattr(SessionStatus, "SUSPENDED")
        assert not hasattr(SessionStatus, "PAUSED")

    def test_cancelled_state_present(self) -> None:
        assert SessionStatus.CANCELLED is not None


# =============================================================================
# EventCategory vs EventType — no collision
# =============================================================================


class TestEventCategoryNoCollision:
    """EventCategory (enums.py) and EventType (event_bus.py) must be separate types."""

    def test_event_category_is_not_event_type(self) -> None:
        assert EventCategory is not EventType

    def test_event_category_has_expected_members(self) -> None:
        expected = {"SYSTEM", "USER", "CHARGING", "FAULT", "WARNING", "INFORMATION", "DEBUG"}
        assert {m.name for m in EventCategory} == expected

    def test_event_type_has_string_values(self) -> None:
        for member in EventType:
            if member is not EventType.ANY:
                assert isinstance(member.value, str)
                assert "." in member.value, (
                    f"{member.name} value '{member.value}' should be namespaced (e.g. 'system.started')"
                )

    def test_event_category_has_auto_int_values(self) -> None:
        for member in EventCategory:
            assert isinstance(member.value, int)


# =============================================================================
# IEC61851State
# =============================================================================


class TestIEC61851State:
    """IEC 61851-1 defines six CP states: A through F."""

    def test_six_states(self) -> None:
        assert len(list(IEC61851State)) == 6

    def test_state_names(self) -> None:
        assert {s.name for s in IEC61851State} == {"A", "B", "C", "D", "E", "F"}


# =============================================================================
# OCPPStatus
# =============================================================================


class TestOCPPStatus:
    """OCPP 1.6J / 2.0.1 connector status values."""

    def test_all_ocpp_statuses_present(self) -> None:
        required = {
            "AVAILABLE",
            "PREPARING",
            "CHARGING",
            "SUSPENDED_EV",
            "SUSPENDED_EVSE",
            "FINISHING",
            "RESERVED",
            "UNAVAILABLE",
            "FAULTED",
        }
        assert {s.name for s in OCPPStatus} == required


# =============================================================================
# FaultSeverity
# =============================================================================


class TestFaultSeverity:
    """FaultSeverity must match OC-SDS-001 §16."""

    def test_four_levels(self) -> None:
        assert {s.name for s in FaultSeverity} == {"INFO", "WARNING", "ERROR", "CRITICAL"}


# =============================================================================
# LogLevel
# =============================================================================


class TestLogLevel:
    """LogLevel must be interoperable with Python's standard logging module."""

    def test_values_match_stdlib(self) -> None:
        import logging

        assert LogLevel.DEBUG == logging.DEBUG
        assert LogLevel.INFO == logging.INFO
        assert LogLevel.WARNING == logging.WARNING
        assert LogLevel.ERROR == logging.ERROR
        assert LogLevel.CRITICAL == logging.CRITICAL

    def test_log_level_is_int(self) -> None:
        assert isinstance(LogLevel.DEBUG, int)


# =============================================================================
# LockState
# =============================================================================


class TestLockState:
    """Connector lock mechanism states."""

    def test_all_states(self) -> None:
        assert {s.name for s in LockState} == {
            "UNLOCKED",
            "LOCKING",
            "LOCKED",
            "UNLOCKING",
            "ERROR",
        }


# =============================================================================
# ContactorState
# =============================================================================


class TestContactorState:
    def test_two_states(self) -> None:
        assert {s.name for s in ContactorState} == {"OPEN", "CLOSED"}


# =============================================================================
# MeterUnit
# =============================================================================


class TestMeterUnit:
    def test_has_temperature_and_frequency(self) -> None:
        """MeterUnit must include CELSIUS and HERTZ for full sensor coverage."""
        assert MeterUnit.CELSIUS is not None
        assert MeterUnit.HERTZ is not None


# =============================================================================
# AuthorizationStatus
# =============================================================================


class TestAuthorizationStatus:
    def test_all_statuses(self) -> None:
        assert {s.name for s in AuthorizationStatus} == {
            "NONE",
            "ACCEPTED",
            "REJECTED",
            "EXPIRED",
            "BLOCKED",
        }


# =============================================================================
# AuthorizationMethod
# =============================================================================


class TestAuthorizationMethod:
    def test_plug_and_charge_included(self) -> None:
        """PLUG_AND_CHARGE is required for future ISO 15118 support per SDS §3."""
        assert AuthorizationMethod.PLUG_AND_CHARGE is not None

    def test_all_methods(self) -> None:
        assert {m.name for m in AuthorizationMethod} == {
            "NONE",
            "RFID",
            "QR_CODE",
            "LOCAL_WHITELIST",
            "OCPP_REMOTE",
            "PLUG_AND_CHARGE",
        }
