"""
Unit tests for opencharge.core.charger.

Covers the Charger aggregate root: state transitions with event
publishing, connector management, administrative control, availability
logic, and the summary snapshot.

Author:
    Ahmed Ghufran

License:
    Apache License 2.0
"""

from __future__ import annotations

import pytest

from opencharge.core.charger import Charger
from opencharge.core.connector import Connector
from opencharge.core.enums import ChargerState
from opencharge.core.event_bus import Event, EventBus, EventType
from opencharge.core.exceptions import InvalidStateTransitionError
from opencharge.core.state_machine import StateMachine


# =============================================================================
# Fixtures
# =============================================================================


@pytest.fixture()
def bus() -> EventBus:
    """Return a shared EventBus for event inspection."""
    return EventBus()


@pytest.fixture()
def charger(bus: EventBus) -> Charger:
    """Return a Charger with one connector and an injected EventBus."""
    return Charger(
        charger_id="OC-001",
        name="Test Charger",
        connectors=[Connector(connector_id=1)],
        event_bus=bus,
    )


@pytest.fixture()
def charger_available(charger: Charger) -> Charger:
    """Return a Charger advanced to AVAILABLE state."""
    charger.transition(ChargerState.BOOTING)
    charger.transition(ChargerState.INITIALIZING)
    charger.transition(ChargerState.AVAILABLE)
    return charger


# =============================================================================
# Construction
# =============================================================================


class TestConstruction:
    def test_starts_offline(self, charger: Charger) -> None:
        assert charger.state == ChargerState.OFFLINE

    def test_charger_id_set(self, charger: Charger) -> None:
        assert charger.charger_id == "OC-001"

    def test_name_set(self, charger: Charger) -> None:
        assert charger.name == "Test Charger"

    def test_connector_count(self, charger: Charger) -> None:
        assert charger.connector_count == 1

    def test_enabled_by_default(self, charger: Charger) -> None:
        assert charger.is_enabled is True

    def test_default_factory_creates_event_bus(self) -> None:
        c = Charger(
            charger_id="OC-002",
            name="Auto Bus",
            connectors=[Connector(connector_id=1)],
        )
        assert isinstance(c.event_bus, EventBus)

    def test_default_factory_creates_state_machine(self) -> None:
        c = Charger(
            charger_id="OC-003",
            name="Auto FSM",
            connectors=[Connector(connector_id=1)],
        )
        assert isinstance(c.state_machine, StateMachine)


# =============================================================================
# transition — FSM advancement
# =============================================================================


class TestTransition:
    def test_valid_transition_changes_state(self, charger: Charger) -> None:
        charger.transition(ChargerState.BOOTING)
        assert charger.state == ChargerState.BOOTING

    def test_invalid_transition_raises(self, charger: Charger) -> None:
        with pytest.raises(InvalidStateTransitionError):
            charger.transition(ChargerState.CHARGING)

    def test_invalid_transition_does_not_change_state(
        self, charger: Charger
    ) -> None:
        with pytest.raises(InvalidStateTransitionError):
            charger.transition(ChargerState.CHARGING)
        assert charger.state == ChargerState.OFFLINE

    def test_full_lifecycle_transitions(self, charger: Charger) -> None:
        sequence = [
            ChargerState.BOOTING,
            ChargerState.INITIALIZING,
            ChargerState.AVAILABLE,
            ChargerState.OCCUPIED,
            ChargerState.AUTHORIZING,
            ChargerState.AUTHORIZED,
            ChargerState.PREPARING,
            ChargerState.CHARGING,
            ChargerState.FINISHING,
            ChargerState.AVAILABLE,
        ]
        for state in sequence:
            charger.transition(state)
        assert charger.state == ChargerState.AVAILABLE


# =============================================================================
# transition — event publishing
# =============================================================================


class TestTransitionEvents:
    def test_state_changed_event_published(
        self, charger: Charger, bus: EventBus
    ) -> None:
        received: list[Event] = []
        bus.subscribe(EventType.STATE_CHANGED, received.append)
        charger.transition(ChargerState.BOOTING)
        assert len(received) == 1

    def test_event_type_is_state_changed(
        self, charger: Charger, bus: EventBus
    ) -> None:
        received: list[Event] = []
        bus.subscribe(EventType.STATE_CHANGED, received.append)
        charger.transition(ChargerState.BOOTING)
        assert received[0].type == EventType.STATE_CHANGED

    def test_event_payload_contains_charger_id(
        self, charger: Charger, bus: EventBus
    ) -> None:
        received: list[Event] = []
        bus.subscribe(EventType.STATE_CHANGED, received.append)
        charger.transition(ChargerState.BOOTING)
        assert received[0].payload["charger_id"] == "OC-001"

    def test_event_payload_contains_previous_state(
        self, charger: Charger, bus: EventBus
    ) -> None:
        received: list[Event] = []
        bus.subscribe(EventType.STATE_CHANGED, received.append)
        charger.transition(ChargerState.BOOTING)
        assert received[0].payload["previous_state"] == "OFFLINE"

    def test_event_payload_contains_current_state(
        self, charger: Charger, bus: EventBus
    ) -> None:
        received: list[Event] = []
        bus.subscribe(EventType.STATE_CHANGED, received.append)
        charger.transition(ChargerState.BOOTING)
        assert received[0].payload["current_state"] == "BOOTING"

    def test_event_source_contains_charger_id(
        self, charger: Charger, bus: EventBus
    ) -> None:
        received: list[Event] = []
        bus.subscribe(EventType.STATE_CHANGED, received.append)
        charger.transition(ChargerState.BOOTING)
        assert "OC-001" in received[0].source

    def test_no_event_published_on_invalid_transition(
        self, charger: Charger, bus: EventBus
    ) -> None:
        received: list[Event] = []
        bus.subscribe(EventType.STATE_CHANGED, received.append)
        with pytest.raises(InvalidStateTransitionError):
            charger.transition(ChargerState.CHARGING)
        assert received == []

    def test_multiple_transitions_publish_multiple_events(
        self, charger: Charger, bus: EventBus
    ) -> None:
        received: list[Event] = []
        bus.subscribe(EventType.STATE_CHANGED, received.append)
        charger.transition(ChargerState.BOOTING)
        charger.transition(ChargerState.INITIALIZING)
        charger.transition(ChargerState.AVAILABLE)
        assert len(received) == 3


# =============================================================================
# can_transition
# =============================================================================


class TestCanTransition:
    def test_valid_transition_returns_true(self, charger: Charger) -> None:
        assert charger.can_transition(ChargerState.BOOTING) is True

    def test_invalid_transition_returns_false(self, charger: Charger) -> None:
        assert charger.can_transition(ChargerState.CHARGING) is False


# =============================================================================
# Connector management
# =============================================================================


class TestConnectorManagement:
    def test_get_connector_returns_correct_connector(
        self, charger: Charger
    ) -> None:
        conn = charger.get_connector(1)
        assert conn.connector_id == 1

    def test_get_connector_raises_for_missing_id(
        self, charger: Charger
    ) -> None:
        with pytest.raises(ValueError, match="99"):
            charger.get_connector(99)

    def test_connector_count_multi(self) -> None:
        c = Charger(
            charger_id="OC-002",
            name="Dual",
            connectors=[Connector(connector_id=1), Connector(connector_id=2)],
        )
        assert c.connector_count == 2

    def test_get_connector_from_multi_charger(self) -> None:
        c = Charger(
            charger_id="OC-002",
            name="Dual",
            connectors=[Connector(connector_id=1), Connector(connector_id=2)],
        )
        assert c.get_connector(2).connector_id == 2


# =============================================================================
# is_available
# =============================================================================


class TestIsAvailable:
    def test_available_when_enabled_and_available_state(
        self, charger_available: Charger
    ) -> None:
        assert charger_available.is_available() is True

    def test_not_available_when_offline(self, charger: Charger) -> None:
        assert charger.is_available() is False

    def test_not_available_when_disabled_even_in_available_state(
        self, charger_available: Charger
    ) -> None:
        charger_available.disable()
        assert charger_available.is_available() is False

    def test_available_after_re_enable(
        self, charger_available: Charger
    ) -> None:
        charger_available.disable()
        charger_available.enable()
        assert charger_available.is_available() is True


# =============================================================================
# enable / disable
# =============================================================================


class TestEnableDisable:
    def test_disable_sets_enabled_false(self, charger: Charger) -> None:
        charger.disable()
        assert charger.is_enabled is False

    def test_enable_sets_enabled_true(self, charger: Charger) -> None:
        charger.disable()
        charger.enable()
        assert charger.is_enabled is True

    def test_disable_publishes_event(
        self, charger: Charger, bus: EventBus
    ) -> None:
        received: list[Event] = []
        bus.subscribe(EventType.CHARGER_DISABLED, received.append)
        charger.disable()
        assert len(received) == 1

    def test_enable_publishes_event(
        self, charger: Charger, bus: EventBus
    ) -> None:
        received: list[Event] = []
        bus.subscribe(EventType.CHARGER_ENABLED, received.append)
        charger.enable()
        assert len(received) == 1

    def test_disable_event_payload_contains_charger_id(
        self, charger: Charger, bus: EventBus
    ) -> None:
        received: list[Event] = []
        bus.subscribe(EventType.CHARGER_DISABLED, received.append)
        charger.disable()
        assert received[0].payload["charger_id"] == "OC-001"


# =============================================================================
# summary
# =============================================================================


class TestSummary:
    def test_summary_returns_dict(self, charger: Charger) -> None:
        assert isinstance(charger.summary(), dict)

    def test_summary_contains_charger_id(self, charger: Charger) -> None:
        assert charger.summary()["charger_id"] == "OC-001"

    def test_summary_contains_state(self, charger: Charger) -> None:
        assert charger.summary()["state"] == "OFFLINE"

    def test_summary_contains_connector_count(self, charger: Charger) -> None:
        assert charger.summary()["connector_count"] == 1

    def test_summary_state_updates_after_transition(
        self, charger: Charger
    ) -> None:
        charger.transition(ChargerState.BOOTING)
        assert charger.summary()["state"] == "BOOTING"

    def test_summary_enabled_field(self, charger: Charger) -> None:
        assert charger.summary()["enabled"] is True
        charger.disable()
        assert charger.summary()["enabled"] is False


# =============================================================================
# String representation
# =============================================================================


class TestStringRepresentation:
    def test_str_contains_charger_id(self, charger: Charger) -> None:
        assert "OC-001" in str(charger)

    def test_str_contains_state(self, charger: Charger) -> None:
        assert "OFFLINE" in str(charger)

    def test_str_contains_connector_count(self, charger: Charger) -> None:
        assert "connectors=1" in str(charger)
