"""
OpenCharge
==========

File:
    enums.py

Description:
    Global enumerations used throughout the OpenCharge platform.

These enums define the common language shared by the Desktop Simulator,
OpenCharge Core, IEC 61851 implementation, OCPP client, Raspberry Pi HMI,
and STM32 firmware.

Author:
    Ahmed Ghufran

License:
    Apache License 2.0
"""

from enum import Enum, IntEnum, auto


# =============================================================================
# Charger
# =============================================================================


class ChargerState(Enum):
    """Overall charger operating state."""

    OFFLINE = auto()
    BOOTING = auto()
    INITIALIZING = auto()
    AVAILABLE = auto()
    OCCUPIED = auto()
    PREPARING = auto()
    CHARGING = auto()
    SUSPENDED_EV = auto()
    SUSPENDED_EVSE = auto()
    FINISHING = auto()
    FAULTED = auto()
    UNAVAILABLE = auto()


# =============================================================================
# Connector
# =============================================================================


class ConnectorType(Enum):
    """Physical connector types."""

    TYPE1 = auto()
    TYPE2_SOCKET = auto()
    TYPE2_TETHERED = auto()
    CCS1 = auto()
    CCS2 = auto()
    CHADEMO = auto()


class ConnectorStatus(Enum):
    """Current connector status."""

    AVAILABLE = auto()
    PLUG_CONNECTED = auto()
    LOCKED = auto()
    CHARGING = auto()
    SUSPENDED = auto()
    FAULTED = auto()


# =============================================================================
# IEC 61851
# =============================================================================


class IEC61851State(Enum):
    """
    IEC 61851 Control Pilot States.

    A : No vehicle connected
    B : Vehicle connected
    C : Charging
    D : Charging with ventilation
    E : Error
    F : Fault
    """

    A = auto()
    B = auto()
    C = auto()
    D = auto()
    E = auto()
    F = auto()


# =============================================================================
# OCPP
# =============================================================================


class OCPPStatus(Enum):
    """OCPP 1.6J / 2.0.1 connector status."""

    AVAILABLE = auto()
    PREPARING = auto()
    CHARGING = auto()
    SUSPENDED_EV = auto()
    SUSPENDED_EVSE = auto()
    FINISHING = auto()
    RESERVED = auto()
    UNAVAILABLE = auto()
    FAULTED = auto()


# =============================================================================
# Authorization
# =============================================================================


class AuthorizationStatus(Enum):
    """Authorization result."""

    NONE = auto()
    ACCEPTED = auto()
    REJECTED = auto()
    EXPIRED = auto()
    BLOCKED = auto()


# =============================================================================
# Charging Session
# =============================================================================


class SessionStatus(Enum):
    """Charging session lifecycle."""

    IDLE = auto()
    STARTING = auto()
    ACTIVE = auto()
    PAUSED = auto()
    STOPPING = auto()
    FINISHED = auto()
    FAILED = auto()


# =============================================================================
# Vehicle
# =============================================================================


class VehicleStatus(Enum):
    """Vehicle connection status."""

    DISCONNECTED = auto()
    CONNECTED = auto()
    READY = auto()
    CHARGING = auto()


# =============================================================================
# Contactor
# =============================================================================


class ContactorState(Enum):
    """Power contactor."""

    OPEN = auto()
    CLOSED = auto()


# =============================================================================
# Connector Lock
# =============================================================================


class LockState(Enum):
    """Socket locking mechanism."""

    UNLOCKED = auto()
    LOCKING = auto()
    LOCKED = auto()
    UNLOCKING = auto()
    ERROR = auto()


# =============================================================================
# Meter
# =============================================================================


class MeterUnit(Enum):
    """Energy meter units."""

    WH = auto()
    KWH = auto()
    VOLT = auto()
    AMPERE = auto()
    WATT = auto()
    KILOWATT = auto()


# =============================================================================
# Faults
# =============================================================================


class FaultCode(Enum):
    """General charger fault codes."""

    NONE = auto()
    EMERGENCY_STOP = auto()
    OVER_VOLTAGE = auto()
    UNDER_VOLTAGE = auto()
    OVER_CURRENT = auto()
    UNDER_CURRENT = auto()
    OVER_TEMPERATURE = auto()
    CONTACTOR_FAILURE = auto()
    LOCK_FAILURE = auto()
    METER_FAILURE = auto()
    COMMUNICATION_FAILURE = auto()
    RCD_TRIPPED = auto()
    CONTROL_PILOT_FAULT = auto()
    PROXIMITY_FAULT = auto()
    INTERNAL_ERROR = auto()


# =============================================================================
# Events
# =============================================================================


class EventType(Enum):
    """System event types."""

    SYSTEM = auto()
    USER = auto()
    CHARGING = auto()
    FAULT = auto()
    WARNING = auto()
    INFORMATION = auto()
    DEBUG = auto()


# =============================================================================
# Log Levels
# =============================================================================


class LogLevel(IntEnum):
    """Logging levels."""

    DEBUG = 10
    INFO = 20
    WARNING = 30
    ERROR = 40
    CRITICAL = 50