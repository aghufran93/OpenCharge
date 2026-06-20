"""
OpenCharge Core — Configuration Manager.

The Configuration Manager is the single source of truth for all
configurable parameters within the OpenCharge platform.

No component may read configuration directly from files, hardware,
environment variables, or databases. All configuration access must
pass through this manager.

Design per OC-SDS-001 §11.13 and §20.

Status:
    STUB — full implementation planned for v0.2.0-alpha.
    The dataclass structures below define the approved configuration
    schema. Persistence, validation, versioning, and change notification
    are not yet implemented.

Author:
    Ahmed Ghufran

License:
    Apache License 2.0
"""

from __future__ import annotations

from dataclasses import dataclass, field


# =============================================================================
# Configuration sections — per OC-SDS-001 §20
# =============================================================================


@dataclass
class ChargerConfig:
    """Identity and metadata for the physical charger unit."""

    charger_id: str = "OC-001"
    name: str = "OpenCharge Station"
    manufacturer: str = "OpenCharge"
    model: str = "OC-AC-001"
    serial_number: str = ""
    firmware_version: str = "0.2.0"


@dataclass
class ConnectorConfig:
    """Per-connector electrical and hardware settings."""

    connector_count: int = 1
    max_current: float = 32.0
    rated_voltage: float = 230.0
    lock_enabled: bool = True


@dataclass
class ElectricalConfig:
    """Site electrical parameters."""

    rated_voltage: float = 230.0
    rated_current: float = 32.0
    max_power_kw: float = 7.4
    grid_frequency: float = 50.0
    rcd_enabled: bool = True
    contactor_delay_ms: int = 500


@dataclass
class SmartChargingConfig:
    """Smart charging engine parameters."""

    enabled: bool = False
    default_current: float = 32.0
    max_current: float = 32.0
    min_current: float = 6.0


@dataclass
class DynamicLoadBalancingConfig:
    """Dynamic Load Balancing (DLB) parameters."""

    enabled: bool = False
    site_max_current: float = 160.0
    site_max_power_kw: float = 36.8
    priority: int = 1
    phase_balancing_enabled: bool = False


@dataclass
class OCPPConfig:
    """OCPP client connection parameters."""

    server_url: str = ""
    charge_point_id: str = "OC-001"
    heartbeat_interval_s: int = 60
    meter_value_interval_s: int = 60
    authorization_cache_enabled: bool = True
    offline_authorization_enabled: bool = True


@dataclass
class NetworkConfig:
    """Network interface parameters."""

    dhcp_enabled: bool = True
    static_ip: str = ""
    subnet_mask: str = ""
    gateway: str = ""
    dns_primary: str = ""
    dns_secondary: str = ""
    ntp_server: str = "pool.ntp.org"


@dataclass
class SecurityConfig:
    """Security and access control parameters."""

    tls_enabled: bool = False
    ca_certificate_path: str = ""
    client_certificate_path: str = ""
    client_key_path: str = ""
    admin_password: str = ""


@dataclass
class UserInterfaceConfig:
    """Display and user interface parameters."""

    language: str = "en"
    theme: str = "default"
    brightness: int = 100
    screen_timeout_s: int = 60
    qr_display_enabled: bool = True


@dataclass
class LoggingConfig:
    """Logging parameters."""

    log_level: str = "INFO"
    debug_mode: bool = False
    remote_logging_enabled: bool = False
    log_retention_days: int = 30


# =============================================================================
# Root configuration container
# =============================================================================


@dataclass
class OpenChargeConfig:
    """
    Root configuration object for the OpenCharge platform.

    Aggregates all configuration sections. The ConfigurationManager
    will load, validate, persist, and provide change notifications
    for this object.
    """

    charger: ChargerConfig = field(default_factory=ChargerConfig)
    connector: ConnectorConfig = field(default_factory=ConnectorConfig)
    electrical: ElectricalConfig = field(default_factory=ElectricalConfig)
    smart_charging: SmartChargingConfig = field(default_factory=SmartChargingConfig)
    load_balancing: DynamicLoadBalancingConfig = field(default_factory=DynamicLoadBalancingConfig)
    ocpp: OCPPConfig = field(default_factory=OCPPConfig)
    network: NetworkConfig = field(default_factory=NetworkConfig)
    security: SecurityConfig = field(default_factory=SecurityConfig)
    ui: UserInterfaceConfig = field(default_factory=UserInterfaceConfig)
    logging: LoggingConfig = field(default_factory=LoggingConfig)


# =============================================================================
# Configuration Manager (stub)
# =============================================================================


class ConfigurationManager:
    """
    Manages loading, validation, persistence, and change notification
    for OpenCharge configuration.

    All components must obtain configuration exclusively through this
    class — never from files or environment variables directly.

    Status:
        STUB — implementation planned for v0.2.0-alpha.
        Currently returns default values only.
    """

    def __init__(self) -> None:
        self._config: OpenChargeConfig = OpenChargeConfig()

    @property
    def config(self) -> OpenChargeConfig:
        """Return the current configuration snapshot."""
        return self._config

    def load_defaults(self) -> None:
        """Reset all configuration to factory default values."""
        self._config = OpenChargeConfig()

    # TODO (v0.2.0-alpha):
    #   - load_from_file(path: str) -> None
    #   - save_to_file(path: str) -> None
    #   - validate() -> list[str]  (returns list of validation errors)
    #   - subscribe_to_changes(section: str, handler: Callable) -> None
    #   - factory_reset() -> None
    #   - export_json() -> str
    #   - import_json(data: str) -> None
