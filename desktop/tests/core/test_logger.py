"""
Unit tests for opencharge.core.logger.

Verifies that configure_logging is idempotent, returns the correct
logger, and that get_logger produces child loggers in the opencharge
namespace.

Author:
    Ahmed Ghufran

License:
    Apache License 2.0
"""

from __future__ import annotations

import logging

import pytest

from opencharge.core.logger import (
    OPENCHARGE_LOGGER,
    configure_logging,
    get_logger,
)


def _our_stream_handlers(logger: logging.Logger) -> list[logging.StreamHandler]:
    """Return only the StreamHandlers added by configure_logging (not pytest's)."""
    return [h for h in logger.handlers if type(h) is logging.StreamHandler]


# =============================================================================
# Fixtures
# =============================================================================


@pytest.fixture(autouse=True)
def reset_logger() -> None:
    """Remove our StreamHandlers from the opencharge logger before each test."""
    logger = logging.getLogger(OPENCHARGE_LOGGER)
    for h in list(logger.handlers):
        if type(h) is logging.StreamHandler:
            logger.removeHandler(h)
    yield
    for h in list(logger.handlers):
        if type(h) is logging.StreamHandler:
            logger.removeHandler(h)


# =============================================================================
# configure_logging
# =============================================================================


class TestConfigureLogging:
    def test_returns_logger(self) -> None:
        logger = configure_logging()
        assert isinstance(logger, logging.Logger)

    def test_logger_name_is_opencharge(self) -> None:
        logger = configure_logging()
        assert logger.name == OPENCHARGE_LOGGER

    def test_logger_has_one_handler_after_first_call(self) -> None:
        configure_logging()
        logger = logging.getLogger(OPENCHARGE_LOGGER)
        assert len(_our_stream_handlers(logger)) == 1

    def test_idempotent_does_not_add_duplicate_handlers(self) -> None:
        configure_logging()
        configure_logging()
        logger = logging.getLogger(OPENCHARGE_LOGGER)
        assert len(_our_stream_handlers(logger)) == 1

    def test_log_level_applied(self) -> None:
        configure_logging(level=logging.DEBUG)
        logger = logging.getLogger(OPENCHARGE_LOGGER)
        assert logger.level == logging.DEBUG

    def test_default_level_is_info(self) -> None:
        configure_logging()
        logger = logging.getLogger(OPENCHARGE_LOGGER)
        assert logger.level == logging.INFO

    def test_propagation_disabled_by_default(self) -> None:
        logger = configure_logging()
        assert logger.propagate is False

    def test_handler_is_stream_handler(self) -> None:
        configure_logging()
        logger = logging.getLogger(OPENCHARGE_LOGGER)
        assert len(_our_stream_handlers(logger)) >= 1


# =============================================================================
# get_logger
# =============================================================================


class TestGetLogger:
    def test_returns_logger(self) -> None:
        logger = get_logger("test_module")
        assert isinstance(logger, logging.Logger)

    def test_logger_name_is_namespaced(self) -> None:
        logger = get_logger("state_machine")
        assert logger.name == f"{OPENCHARGE_LOGGER}.state_machine"

    def test_different_names_produce_different_loggers(self) -> None:
        l1 = get_logger("module_a")
        l2 = get_logger("module_b")
        assert l1 is not l2
        assert l1.name != l2.name

    def test_same_name_returns_same_logger(self) -> None:
        l1 = get_logger("same_module")
        l2 = get_logger("same_module")
        assert l1 is l2

    def test_child_logger_inherits_from_opencharge(self) -> None:
        """Child loggers must inherit from the opencharge root logger."""
        child = get_logger("charger")
        assert child.name.startswith(OPENCHARGE_LOGGER)


# =============================================================================
# OPENCHARGE_LOGGER constant
# =============================================================================


class TestConstant:
    def test_logger_constant_value(self) -> None:
        assert OPENCHARGE_LOGGER == "opencharge"
