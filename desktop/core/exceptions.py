"""
Core exception hierarchy for OpenCharge.
"""


class OpenChargeError(Exception):
    """Base exception for all OpenCharge errors."""


class ConfigurationError(OpenChargeError):
    """Raised when configuration is invalid."""


class InvalidStateTransition(OpenChargeError):
    """Raised when an invalid state transition is attempted."""


class EventBusError(OpenChargeError):
    """Raised for EventBus related errors."""


class HardwareError(OpenChargeError):
    """Raised for hardware abstraction errors."""