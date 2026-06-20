"""
OpenCharge
==========

File:
    connector.py

Description:
    Represents a physical EV charging connector.

A Connector encapsulates the logical state of one EV charging outlet,
including the socket, locking mechanism, IEC 61851 state, contactor
interface, and availability.

The Connector does not directly control hardware. Hardware interaction
is performed through the Hardware Abstraction Layer (HAL).

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


@dataclass
class Connector:
    """
    Represents one EV charging connector.
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

    metadata: dict = field(default_factory=dict)

    # ------------------------------------------------------------------
    # Plug
    # ------------------------------------------------------------------

    def plug_in(self) -> None:
        """
        Vehicle cable connected.
        """
        self.plugged = True
        self.status = ConnectorStatus.PLUG_CONNECTED
        self.iec_state = IEC61851State.B

    def unplug(self) -> None:
        """
        Vehicle cable disconnected.
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
        """
        Lock connector.
        """
        self.lock_state = LockState.LOCKED

    def unlock(self) -> None:
        """
        Unlock connector.
        """
        self.lock_state = LockState.UNLOCKED

    # ------------------------------------------------------------------
    # Contactor
    # ------------------------------------------------------------------

    def close_contactor(self) -> None:
        """
        Energize power output.
        """
        self.contactor_state = ContactorState.CLOSED

    def open_contactor(self) -> None:
        """
        Remove power output.
        """
        self.contactor_state = ContactorState.OPEN

    # ------------------------------------------------------------------
    # Charging
    # ------------------------------------------------------------------

    def start_charging(self) -> None:
        """
        Begin charging session.
        """

        if not self.plugged:
            raise RuntimeError("Cannot start charging: no vehicle connected.")

        self.lock()

        self.close_contactor()

        self.status = ConnectorStatus.CHARGING

        self.iec_state = IEC61851State.C

    def stop_charging(self) -> None:
        """
        Stop charging session.
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
    # Fault
    # ------------------------------------------------------------------

    def fault(self) -> None:
        """
        Put connector into fault state.
        """

        self.status = ConnectorStatus.FAULTED

        self.open_contactor()

    def clear_fault(self) -> None:
        """
        Recover from fault.
        """

        if self.plugged:
            self.status = ConnectorStatus.PLUG_CONNECTED
        else:
            self.status = ConnectorStatus.AVAILABLE

    # ------------------------------------------------------------------
    # Properties
    # ------------------------------------------------------------------

    @property
    def is_available(self) -> bool:
        return self.status == ConnectorStatus.AVAILABLE

    @property
    def is_plugged(self) -> bool:
        return self.plugged

    @property
    def is_locked(self) -> bool:
        return self.lock_state == LockState.LOCKED

    @property
    def is_charging(self) -> bool:
        return self.status == ConnectorStatus.CHARGING

    # ------------------------------------------------------------------
    # Representation
    # ------------------------------------------------------------------

    def __str__(self) -> str:
        return (
            f"Connector("
            f"id={self.connector_id}, "
            f"status={self.status.name}, "
            f"iec={self.iec_state.name}, "
            f"lock={self.lock_state.name}, "
            f"contactor={self.contactor_state.name})"
        )