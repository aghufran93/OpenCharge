"""
Unit tests for opencharge.core.configuration.

Verifies that all configuration sections exist with sensible defaults,
the schema matches OC-SDS-001 §20, and the ConfigurationManager
returns the correct values.

Author:
    Ahmed Ghufran

License:
    Apache License 2.0
"""

import pytest

from opencharge.core.configuration import (
    ChargerConfig,
    ConfigurationManager,
    ConnectorConfig,
    DynamicLoadBalancingConfig,
    ElectricalConfig,
    LoggingConfig,
    NetworkConfig,
    OCPPConfig,
    OpenChargeConfig,
    SecurityConfig,
    SmartChargingConfig,
    UserInterfaceConfig,
)


# =============================================================================
# Individual section defaults
# =============================================================================


class TestChargerConfig:
    def test_default_charger_id(self) -> None:
        assert ChargerConfig().charger_id == "OC-001"

    def test_default_manufacturer(self) -> None:
        assert ChargerConfig().manufacturer == "OpenCharge"

    def test_custom_values(self) -> None:
        cfg = ChargerConfig(charger_id="ABC-123", name="My Charger")
        assert cfg.charger_id == "ABC-123"
        assert cfg.name == "My Charger"


class TestConnectorConfig:
    def test_default_connector_count(self) -> None:
        assert ConnectorConfig().connector_count == 1

    def test_default_max_current(self) -> None:
        assert ConnectorConfig().max_current == 32.0

    def test_default_voltage(self) -> None:
        assert ConnectorConfig().rated_voltage == 230.0

    def test_lock_enabled_by_default(self) -> None:
        assert ConnectorConfig().lock_enabled is True


class TestElectricalConfig:
    def test_default_rated_current(self) -> None:
        assert ElectricalConfig().rated_current == 32.0

    def test_rcd_enabled_by_default(self) -> None:
        assert ElectricalConfig().rcd_enabled is True

    def test_contactor_delay_positive(self) -> None:
        assert ElectricalConfig().contactor_delay_ms > 0

    def test_max_power_kw_sensible(self) -> None:
        cfg = ElectricalConfig()
        assert 0 < cfg.max_power_kw <= 22.0


class TestSmartChargingConfig:
    def test_disabled_by_default(self) -> None:
        assert SmartChargingConfig().enabled is False

    def test_min_current_not_below_iec_minimum(self) -> None:
        """IEC 61851 minimum advertised current is 6 A."""
        assert SmartChargingConfig().min_current >= 6.0

    def test_default_current_not_exceed_max(self) -> None:
        cfg = SmartChargingConfig()
        assert cfg.default_current <= cfg.max_current


class TestDynamicLoadBalancingConfig:
    def test_disabled_by_default(self) -> None:
        assert DynamicLoadBalancingConfig().enabled is False

    def test_site_capacity_positive(self) -> None:
        assert DynamicLoadBalancingConfig().site_max_current > 0

    def test_priority_positive(self) -> None:
        assert DynamicLoadBalancingConfig().priority >= 1


class TestOCPPConfig:
    def test_server_url_empty_by_default(self) -> None:
        assert OCPPConfig().server_url == ""

    def test_heartbeat_interval_positive(self) -> None:
        assert OCPPConfig().heartbeat_interval_s > 0

    def test_authorization_cache_enabled_by_default(self) -> None:
        assert OCPPConfig().authorization_cache_enabled is True


class TestNetworkConfig:
    def test_dhcp_enabled_by_default(self) -> None:
        assert NetworkConfig().dhcp_enabled is True

    def test_ntp_server_set(self) -> None:
        assert NetworkConfig().ntp_server != ""


class TestSecurityConfig:
    def test_tls_disabled_by_default(self) -> None:
        assert SecurityConfig().tls_enabled is False


class TestUserInterfaceConfig:
    def test_default_language_english(self) -> None:
        assert UserInterfaceConfig().language == "en"

    def test_brightness_in_valid_range(self) -> None:
        assert 0 <= UserInterfaceConfig().brightness <= 100


class TestLoggingConfig:
    def test_default_log_level(self) -> None:
        assert LoggingConfig().log_level == "INFO"

    def test_debug_disabled_by_default(self) -> None:
        assert LoggingConfig().debug_mode is False


# =============================================================================
# OpenChargeConfig — root aggregate
# =============================================================================


class TestOpenChargeConfig:
    def test_all_sections_present(self) -> None:
        cfg = OpenChargeConfig()
        assert isinstance(cfg.charger, ChargerConfig)
        assert isinstance(cfg.connector, ConnectorConfig)
        assert isinstance(cfg.electrical, ElectricalConfig)
        assert isinstance(cfg.smart_charging, SmartChargingConfig)
        assert isinstance(cfg.load_balancing, DynamicLoadBalancingConfig)
        assert isinstance(cfg.ocpp, OCPPConfig)
        assert isinstance(cfg.network, NetworkConfig)
        assert isinstance(cfg.security, SecurityConfig)
        assert isinstance(cfg.ui, UserInterfaceConfig)
        assert isinstance(cfg.logging, LoggingConfig)

    def test_sections_are_independent_instances(self) -> None:
        """Each OpenChargeConfig must have its own independent section instances."""
        cfg1 = OpenChargeConfig()
        cfg2 = OpenChargeConfig()
        cfg1.charger.charger_id = "MODIFIED"
        assert cfg2.charger.charger_id != "MODIFIED"


# =============================================================================
# ConfigurationManager
# =============================================================================


class TestConfigurationManager:
    def test_returns_opencharge_config(self) -> None:
        mgr = ConfigurationManager()
        assert isinstance(mgr.config, OpenChargeConfig)

    def test_default_charger_id(self) -> None:
        mgr = ConfigurationManager()
        assert mgr.config.charger.charger_id == "OC-001"

    def test_load_defaults_resets_to_defaults(self) -> None:
        mgr = ConfigurationManager()
        mgr.config.charger.charger_id = "CHANGED"
        mgr.load_defaults()
        assert mgr.config.charger.charger_id == "OC-001"

    def test_load_defaults_replaces_config_instance(self) -> None:
        mgr = ConfigurationManager()
        original = mgr.config
        mgr.load_defaults()
        assert mgr.config is not original
