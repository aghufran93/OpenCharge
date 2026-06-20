"""
Unit tests for opencharge.core.connector.

Covers the full connector lifecycle: cable insertion/removal, lock
management, contactor control, charging start/stop, fault handling,
computed properties, and edge cases.

Author:
    Ahmed Ghufran

License:
    Apache License 2.0
"""

import pytest

from opencharge.core.connector import Connector
from opencharge.core.enums import (
    ConnectorStatus,
    ConnectorType,
    ContactorState,
    IEC61851State,
    LockState,
)
from opencharge.core.exceptions import SessionAlreadyActiveError


# =============================================================================
# Fixtures
# =============================================================================


@pytest.fixture()
def connector() -> Connector:
    """Return a fresh, unoccupied connector with default settings."""
    return Connector(connector_id=1)


@pytest.fixture()
def plugged_connector(connector: Connector) -> Connector:
    """Return a connector with a vehicle cable detected."""
    connector.plug_in()
    return connector


@pytest.fixture()
def charging_connector(plugged_connector: Connector) -> Connector:
    """Return a connector actively charging."""
    plugged_connector.start_charging()
    return plugged_connector


# =============================================================================
# Default state
# =============================================================================


class TestDefaultState:
    def test_status_is_available(self, connector: Connector) -> None:
        assert connector.status == ConnectorStatus.AVAILABLE

    def test_iec_state_is_a(self, connector: Connector) -> None:
        assert connector.iec_state == IEC61851State.A

    def test_lock_is_unlocked(self, connector: Connector) -> None:
        assert connector.lock_state == LockState.UNLOCKED

    def test_contactor_is_open(self, connector: Connector) -> None:
        assert connector.contactor_state == ContactorState.OPEN

    def test_plugged_is_false(self, connector: Connector) -> None:
        assert connector.plugged is False

    def test_default_max_current(self, connector: Connector) -> None:
        assert connector.max_current == 32.0

    def test_default_rated_voltage(self, connector: Connector) -> None:
        assert connector.rated_voltage == 230.0

    def test_default_connector_type(self, connector: Connector) -> None:
        assert connector.connector_type == ConnectorType.TYPE2_SOCKET


# =============================================================================
# plug_in / unplug
# =============================================================================


class TestPlugInUnplug:
    def test_plug_in_sets_plugged(self, connector: Connector) -> None:
        connector.plug_in()
        assert connector.plugged is True

    def test_plug_in_sets_status(self, connector: Connector) -> None:
        connector.plug_in()
        assert connector.status == ConnectorStatus.PLUG_CONNECTED

    def test_plug_in_sets_iec_state_b(self, connector: Connector) -> None:
        connector.plug_in()
        assert connector.iec_state == IEC61851State.B

    def test_plug_in_is_idempotent(self, connector: Connector) -> None:
        """Calling plug_in twice must not raise or corrupt state."""
        connector.plug_in()
        connector.plug_in()
        assert connector.plugged is True
        assert connector.status == ConnectorStatus.PLUG_CONNECTED

    def test_unplug_clears_plugged(self, plugged_connector: Connector) -> None:
        plugged_connector.unplug()
        assert plugged_connector.plugged is False

    def test_unplug_restores_available(self, plugged_connector: Connector) -> None:
        plugged_connector.unplug()
        assert plugged_connector.status == ConnectorStatus.AVAILABLE

    def test_unplug_opens_contactor(self, charging_connector: Connector) -> None:
        charging_connector.unplug()
        assert charging_connector.contactor_state == ContactorState.OPEN

    def test_unplug_unlocks_connector(self, charging_connector: Connector) -> None:
        charging_connector.unplug()
        assert charging_connector.lock_state == LockState.UNLOCKED

    def test_unplug_restores_iec_state_a(self, plugged_connector: Connector) -> None:
        plugged_connector.unplug()
        assert plugged_connector.iec_state == IEC61851State.A


# =============================================================================
# Lock / Unlock
# =============================================================================


class TestLockUnlock:
    def test_lock_sets_locked(self, connector: Connector) -> None:
        connector.lock()
        assert connector.lock_state == LockState.LOCKED

    def test_unlock_sets_unlocked(self, connector: Connector) -> None:
        connector.lock()
        connector.unlock()
        assert connector.lock_state == LockState.UNLOCKED


# =============================================================================
# Contactor
# =============================================================================


class TestContactor:
    def test_close_contactor(self, connector: Connector) -> None:
        connector.close_contactor()
        assert connector.contactor_state == ContactorState.CLOSED

    def test_open_contactor(self, connector: Connector) -> None:
        connector.close_contactor()
        connector.open_contactor()
        assert connector.contactor_state == ContactorState.OPEN


# =============================================================================
# start_charging
# =============================================================================


class TestStartCharging:
    def test_locks_connector(self, plugged_connector: Connector) -> None:
        plugged_connector.start_charging()
        assert plugged_connector.lock_state == LockState.LOCKED

    def test_closes_contactor(self, plugged_connector: Connector) -> None:
        plugged_connector.start_charging()
        assert plugged_connector.contactor_state == ContactorState.CLOSED

    def test_sets_charging_status(self, plugged_connector: Connector) -> None:
        plugged_connector.start_charging()
        assert plugged_connector.status == ConnectorStatus.CHARGING

    def test_sets_iec_state_c(self, plugged_connector: Connector) -> None:
        plugged_connector.start_charging()
        assert plugged_connector.iec_state == IEC61851State.C

    def test_raises_when_not_plugged(self, connector: Connector) -> None:
        with pytest.raises(RuntimeError, match="no vehicle connected"):
            connector.start_charging()

    def test_raises_when_already_charging(
        self, charging_connector: Connector
    ) -> None:
        with pytest.raises(SessionAlreadyActiveError):
            charging_connector.start_charging()


# =============================================================================
# stop_charging
# =============================================================================


class TestStopCharging:
    def test_opens_contactor(self, charging_connector: Connector) -> None:
        charging_connector.stop_charging()
        assert charging_connector.contactor_state == ContactorState.OPEN

    def test_unlocks_connector(self, charging_connector: Connector) -> None:
        charging_connector.stop_charging()
        assert charging_connector.lock_state == LockState.UNLOCKED

    def test_status_plug_connected_when_vehicle_still_present(
        self, charging_connector: Connector
    ) -> None:
        charging_connector.stop_charging()
        assert charging_connector.status == ConnectorStatus.PLUG_CONNECTED

    def test_iec_state_b_when_vehicle_still_present(
        self, charging_connector: Connector
    ) -> None:
        charging_connector.stop_charging()
        assert charging_connector.iec_state == IEC61851State.B

    def test_status_available_when_vehicle_gone(
        self, charging_connector: Connector
    ) -> None:
        charging_connector.plugged = False
        charging_connector.stop_charging()
        assert charging_connector.status == ConnectorStatus.AVAILABLE

    def test_iec_state_a_when_vehicle_gone(
        self, charging_connector: Connector
    ) -> None:
        charging_connector.plugged = False
        charging_connector.stop_charging()
        assert charging_connector.iec_state == IEC61851State.A


# =============================================================================
# Fault
# =============================================================================


class TestFault:
    def test_fault_sets_faulted_status(
        self, charging_connector: Connector
    ) -> None:
        charging_connector.fault()
        assert charging_connector.status == ConnectorStatus.FAULTED

    def test_fault_opens_contactor(self, charging_connector: Connector) -> None:
        charging_connector.fault()
        assert charging_connector.contactor_state == ContactorState.OPEN

    def test_fault_does_not_unlock(self, charging_connector: Connector) -> None:
        """Per IEC 61851 safety: cable must remain locked until technician clears fault."""
        charging_connector.fault()
        assert charging_connector.lock_state == LockState.LOCKED

    def test_clear_fault_with_vehicle_present(
        self, charging_connector: Connector
    ) -> None:
        charging_connector.fault()
        charging_connector.clear_fault()
        assert charging_connector.status == ConnectorStatus.PLUG_CONNECTED

    def test_clear_fault_without_vehicle(self, connector: Connector) -> None:
        connector.fault()
        connector.clear_fault()
        assert connector.status == ConnectorStatus.AVAILABLE


# =============================================================================
# Computed properties
# =============================================================================


class TestProperties:
    def test_is_available_true_when_idle(self, connector: Connector) -> None:
        assert connector.is_available is True

    def test_is_available_false_when_charging(
        self, charging_connector: Connector
    ) -> None:
        assert charging_connector.is_available is False

    def test_is_plugged_true_after_plug_in(
        self, plugged_connector: Connector
    ) -> None:
        assert plugged_connector.is_plugged is True

    def test_is_plugged_false_initially(self, connector: Connector) -> None:
        assert connector.is_plugged is False

    def test_is_locked_after_lock(self, connector: Connector) -> None:
        connector.lock()
        assert connector.is_locked is True

    def test_is_locked_false_initially(self, connector: Connector) -> None:
        assert connector.is_locked is False

    def test_is_charging_true_during_session(
        self, charging_connector: Connector
    ) -> None:
        assert charging_connector.is_charging is True

    def test_is_charging_false_when_idle(self, connector: Connector) -> None:
        assert connector.is_charging is False

    def test_is_faulted_true_after_fault(self, connector: Connector) -> None:
        connector.fault()
        assert connector.is_faulted is True

    def test_is_faulted_false_when_idle(self, connector: Connector) -> None:
        assert connector.is_faulted is False

    def test_max_power_kw_calculation(self, connector: Connector) -> None:
        expected = (32.0 * 230.0) / 1000.0
        assert connector.max_power_kw == pytest.approx(expected)

    def test_max_power_kw_with_custom_current(self) -> None:
        c = Connector(connector_id=1, max_current=16.0, rated_voltage=230.0)
        assert c.max_power_kw == pytest.approx(3.68)


# =============================================================================
# String representation
# =============================================================================


class TestStringRepresentation:
    def test_str_contains_connector_id(self, connector: Connector) -> None:
        assert "id=1" in str(connector)

    def test_str_contains_status(self, connector: Connector) -> None:
        assert "AVAILABLE" in str(connector)

    def test_str_contains_iec_state(self, connector: Connector) -> None:
        assert "iec=A" in str(connector)
