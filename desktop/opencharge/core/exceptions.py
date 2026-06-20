"""
OpenCharge Core — Exception Hierarchy.

All OpenCharge exceptions inherit from OpenChargeError, allowing
callers to catch the entire family with a single except clause while
still handling specific conditions individually.

Author:
    Ahmed Ghufran

License:
    Apache License 2.0
"""


class OpenChargeError(Exception):
    """Base exception for all OpenCharge errors."""


# =============================================================================
# Configuration
# =============================================================================


class ConfigurationError(OpenChargeError):
    """Raised when configuration is missing, invalid, or cannot be loaded."""


# =============================================================================
# State Machine
# =============================================================================


class InvalidStateTransitionError(OpenChargeError):
    """
    Raised when a state transition that violates the FSM rule table
    is requested.

    Example
    -------
    OFFLINE → CHARGING is not a valid transition and raises this error.
    """


# =============================================================================
# Event Bus
# =============================================================================


class EventBusError(OpenChargeError):
    """Raised for EventBus-related errors."""


# =============================================================================
# Hardware Abstraction
# =============================================================================


class HardwareError(OpenChargeError):
    """Raised when the Hardware Abstraction Layer encounters an error."""


class ContactorError(HardwareError):
    """Raised when the contactor fails to open or close."""


class LockError(HardwareError):
    """Raised when the connector lock fails to operate."""


# =============================================================================
# Authorization
# =============================================================================


class AuthorizationError(OpenChargeError):
    """Raised when authorization cannot be processed."""


# =============================================================================
# Session
# =============================================================================


class SessionError(OpenChargeError):
    """Raised for illegal charging session operations."""


class SessionAlreadyActiveError(SessionError):
    """Raised when a new session is started while one is already active."""


# =============================================================================
# Fault
# =============================================================================


class FaultError(OpenChargeError):
    """Raised when a critical charger fault occurs that requires handling."""
