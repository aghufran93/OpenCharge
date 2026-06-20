"""
OpenCharge Core — Domain Enumerations.

Global enumerations shared across the Desktop Simulator, OpenCharge Core,
IEC 61851 implementation, OCPP client, Raspberry Pi HMI, and STM32 firmware.

These enums form the common vocabulary of the entire platform.

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
    """
    Overall charger operating state.

    Follows the lifecycle defined in OC-SDS-001 §13:

        OFFLINE → BOOTING → INITIALIZING → AVAILABLE
            → OCCUPIED → AUTHORIZING → AUTHORIZED
            → PREPARING → CHARGING
            → SUSPENDED_EV / SUSPENDED_EVSE
            → FINISHING → AVAILABLE

    Any state may transition to FAULTED.
    """

    OFFLINE = auto()
    BOOTING = auto()
    INITIALIZING = auto()
    AVAILABLE = auto()
    OCCUPIED = auto()
    AUTHORIZING = auto()
    AUTHORIZED = auto()
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
    """Physical connector types supported by OpenCharge."""

    TYPE1 = auto()
    TYPE2_SOCKET = auto()
    TYPE2_TETHERED = auto()
    CCS1 = auto()
    CCS2 = auto()
    CHADEMO = auto()


class ConnectorStatus(Enum):
    """Logical status of a single charging connector."""

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
    IEC 61851-1 Control Pilot states.

    A — No vehicle connected         (12 V)
    B — Vehicle connected, not ready  (+9 V)
    C — Charging (without ventilation)(+6 V)
    D — Charging (with ventilation)   (+3 V)
    E — Power off / error             (0 V)
    F — Fault (EVSE cannot deliver)   (-12 V)
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
    """OCPP 1.6J / 2.0.1 connector status values for StatusNotification."""

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
    """Result of an authorization attempt (RFID, QR, OCPP remote)."""

    NONE = auto()
    ACCEPTED = auto()
    REJECTED = auto()
    EXPIRED = auto()
    BLOCKED = auto()


class AuthorizationMethod(Enum):
    """Method used for authorization."""

    NONE = auto()
    RFID = auto()
    QR_CODE = auto()
    LOCAL_WHITELIST = auto()
    OCPP_REMOTE = auto()
    PLUG_AND_CHARGE = auto()


# =============================================================================
# Charging Session
# =============================================================================


class SessionStatus(Enum):
    """
    Charging session lifecycle states.

    Aligned with OC-SDS-001 §14:

        IDLE → CREATED → AUTHORIZED → PREPARING
             → ACTIVE → SUSPENDED → STOPPING
             → COMPLETED | FAILED | CANCELLED
    """

    IDLE = auto()
    CREATED = auto()
    AUTHORIZED = auto()
    PREPARING = auto()
    ACTIVE = auto()
    SUSPENDED = auto()
    STOPPING = auto()
    COMPLETED = auto()
    FAILED = auto()
    CANCELLED = auto()


# =============================================================================
# Vehicle
# =============================================================================


class VehicleStatus(Enum):
    """Vehicle connection and charging readiness status."""

    DISCONNECTED = auto()
    CONNECTED = auto()
    READY = auto()
    CHARGING = auto()


# =============================================================================
# Contactor
# =============================================================================


class ContactorState(Enum):
    """Power contactor state."""

    OPEN = auto()
    CLOSED = auto()


# =============================================================================
# Connector Lock
# =============================================================================


class LockState(Enum):
    """Socket locking mechanism state."""

    UNLOCKED = auto()
    LOCKING = auto()
    LOCKED = auto()
    UNLOCKING = auto()
    ERROR = auto()


# =============================================================================
# Meter
# =============================================================================


class MeterUnit(Enum):
    """Electrical measurement units used by the Meter domain object."""

    WH = auto()
    KWH = auto()
    VOLT = auto()
    AMPERE = auto()
    WATT = auto()
    KILOWATT = auto()
    CELSIUS = auto()
    HERTZ = auto()


# =============================================================================
# Faults
# =============================================================================


class FaultCode(Enum):
    """
    Charger fault codes.

    Reported by the Fault Manager and mapped to OCPP ErrorCode where
    applicable.
    """

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


class FaultSeverity(Enum):
    """
    Fault severity classification per OC-SDS-001 §16.

    INFO     — Informational, no operational impact.
    WARNING  — Non-critical, degraded operation possible.
    ERROR    — Charger cannot continue normally.
    CRITICAL — Immediate shutdown required.
    """

    INFO = auto()
    WARNING = auto()
    ERROR = auto()
    CRITICAL = auto()


# =============================================================================
# Event Categories
# =============================================================================


class EventCategory(Enum):
    """
    High-level event category classification.

    Used for filtering and routing events within the platform.
    Not to be confused with EventType in event_bus.py, which defines
    the specific named events published on the EventBus.
    """

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
    """
    Logging severity levels.

    Aligned with Python's standard logging module values so that
    LogLevel.INFO == logging.INFO, enabling direct interoperability.
    """

    DEBUG = 10
    INFO = 20
    WARNING = 30
    ERROR = 40
    CRITICAL = 50
