"""
OpenCharge Core Package.

Contains all hardware-independent, protocol-independent, and GUI-independent
business logic for the OpenCharge platform.

This package must never import from:
    - PySide6 / Qt
    - pyserial / hardware drivers
    - ocpp (protocol library)
    - Any platform-specific module

All other packages depend on Core — Core depends on nothing above it.

Modules
-------
charger          — Charger aggregate root (EVSE)
connector        — Connector domain object
state_machine    — Finite state machine for charger lifecycle
event_bus        — Publish/subscribe event bus
enums            — Platform-wide enumeration types
exceptions       — Exception hierarchy
configuration    — Configuration manager and schema
logger           — Logging infrastructure
version          — Package version constants
"""

from .version import NAME, VERSION

__version__ = VERSION
__all__ = ["NAME", "VERSION"]
