"""
OpenCharge Core — Connector Domain Object.

Represents one physical EV charging outlet.

A Connector encapsulates the logical state of a single charging socket,
including the lock mechanism, IEC 61851 pilot state, and contactor.

The Connector does not communicate with hardware directly. All physical
control is delegated to the Hardware Abstraction Layer (HAL).

One Charger owns one or more Connectors.
One Connector may hold at most one active ChargingSession.

Author:
    Ahmed Ghufran

License:
    Apache License 2.0
"""

from __future__ import annotations

from dataclasses import dataclass, field

from .enums import (
    ConnectorStatus,
    ConnectorType,
    ContactorState,
    IEC61851State,
    LockState,
)
from .exceptions import SessionAlreadyActiveError


@dataclass
class Connector:
    """
    Represents one EV charging connector (socket or tethered cable).

    Attributes
    ----------
    connector_id:
        Unique identifier within the parent Charger (1-based per OCPP).
    connector_type:
        Physical socket type (Type 2, CCS2, etc.).
    status:
        Current logical connector status.
    iec_state:
        IEC 61851-1 Control Pilot state.
    lock_state:
        Locking mechanism state.
    contactor_state:
        Power contactor state.
    plugged:
        True when a vehicle cable is physically detected.
    max_current:
        Rated maximum charging current in amperes.
    rated_voltage:
        Rated voltage in volts.
    metadata:
        Optional key/value store for connector-specific extension data.
    """

    connector_id: int
    connector_type: ConnectorType = ConnectorType.TYPE2_SOCKET
    status: ConnectorStatus = ConnectorStatus.AVAILABLE
    iec_state: IEC61851State = IEC61851State.A
    lock_state: LockState = LockState.UNLOCKED
    contactor_state: ContactorState = ContactorState.OPEN
    plugged: bool = False
    max_current: float = 32.0
    rated_voltage: float = 230.0
    metadata: dict[str, object] = field(default_factory=dict)

    # ------------------------------------------------------------------
    # Cable management
    # ------------------------------------------------------------------

    def plug_in(self) -> None:
        """
        Record a vehicle cable insertion event.

        Sets IEC 61851 CP state to B (vehicle connected, not ready).
        """
        if self.plugged:
            return
        self.plugged = True
        self.status = ConnectorStatus.PLUG_CONNECTED
        self.iec_state = IEC61851State.B

    def unplug(self) -> None:
        """
        Record a vehicle cable removal event.

        Resets all connector state to idle. The HAL must ensure the
        contactor is open and the lock is released before calling this.
        """
        self.plugged = False
        self.status = ConnectorStatus.AVAILABLE
        self.lock_state = LockState.UNLOCKED
        self.contactor_state = ContactorState.OPEN
        self.iec_state = IEC61851State.A

    # ------------------------------------------------------------------
    # Lock
    # ------------------------------------------------------------------

    def lock(self) -> None:
        """Lock the connector — prevents cable removal during charging."""
        self.lock_state = LockState.LOCKED

    def unlock(self) -> None:
        """Unlock the connector."""
        self.lock_state = LockState.UNLOCKED

    # ------------------------------------------------------------------
    # Contactor
    # ------------------------------------------------------------------

    def close_contactor(self) -> None:
        """Close the power contactor — energizes the connector output."""
        self.contactor_state = ContactorState.CLOSED

    def open_contactor(self) -> None:
        """Open the power contactor — removes power from the connector."""
        self.contactor_state = ContactorState.OPEN

    # ------------------------------------------------------------------
    # Charging
    # ------------------------------------------------------------------

    def start_charging(self) -> None:
        """
        Begin a charging session on this connector.

        Locks the connector, closes the contactor, and advances the
        IEC 61851 CP state to C (charging without ventilation).

        Raises
        ------
        RuntimeError
            If no vehicle cable is detected.
        SessionAlreadyActiveError
            If the connector is already in a charging state.
        """
        if not self.plugged:
            raise RuntimeError(
                f"Connector {self.connector_id}: "
                "cannot start charging — no vehicle connected."
            )
        if self.status == ConnectorStatus.CHARGING:
            raise SessionAlreadyActiveError(
                f"Connector {self.connector_id}: charging already active."
            )

        self.lock()
        self.close_contactor()
        self.status = ConnectorStatus.CHARGING
        self.iec_state = IEC61851State.C

    def stop_charging(self) -> None:
        """
        Stop an active charging session on this connector.

        Opens the contactor, unlocks the connector, and returns the
        IEC 61851 CP state to the appropriate idle state.
        """
        self.open_contactor()
        self.unlock()

        if self.plugged:
            self.status = ConnectorStatus.PLUG_CONNECTED
            self.iec_state = IEC61851State.B
        else:
            self.status = ConnectorStatus.AVAILABLE
            self.iec_state = IEC61851State.A

    # ------------------------------------------------------------------
    # Fault management
    # ------------------------------------------------------------------

    def fault(self) -> None:
        """
        Place the connector into fault state.

        The contactor is opened immediately as a safety measure.
        The lock is NOT released — the cable remains captured until a
        service technician clears the fault (per IEC 61851 safety rules).
        """
        self.open_contactor()
        self.status = ConnectorStatus.FAULTED

    def clear_fault(self) -> None:
        """
        Recover the connector from fault state.

        Returns status to PLUG_CONNECTED or AVAILABLE depending on
        whether a vehicle cable is still detected.
        """
        if self.plugged:
            self.status = ConnectorStatus.PLUG_CONNECTED
        else:
            self.status = ConnectorStatus.AVAILABLE

    # ------------------------------------------------------------------
    # Convenience properties
    # ------------------------------------------------------------------

    @property
    def is_available(self) -> bool:
        """True if the connector is ready to accept a vehicle."""
        return self.status == ConnectorStatus.AVAILABLE

    @property
    def is_plugged(self) -> bool:
        """True if a vehicle cable is physically detected."""
        return self.plugged

    @property
    def is_locked(self) -> bool:
        """True if the connector lock is engaged."""
        return self.lock_state == LockState.LOCKED

    @property
    def is_charging(self) -> bool:
        """True if energy transfer is active on this connector."""
        return self.status == ConnectorStatus.CHARGING

    @property
    def is_faulted(self) -> bool:
        """True if the connector is in a fault state."""
        return self.status == ConnectorStatus.FAULTED

    @property
    def max_power_kw(self) -> float:
        """Rated maximum power in kilowatts (single-phase)."""
        return (self.max_current * self.rated_voltage) / 1000.0

    # ------------------------------------------------------------------
    # Representation
    # ------------------------------------------------------------------

    def __str__(self) -> str:
        return (
            f"Connector("
            f"id={self.connector_id}, "
            f"type={self.connector_type.name}, "
            f"status={self.status.name}, "
            f"iec={self.iec_state.name}, "
            f"lock={self.lock_state.name}, "
            f"contactor={self.contactor_state.name})"
        )
