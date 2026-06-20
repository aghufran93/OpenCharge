"""
OpenCharge Core — Logging Infrastructure.

Provides a consistent logging setup for the entire OpenCharge platform.
All modules obtain their logger through the standard
`logging.getLogger(__name__)` pattern. This module centralises
formatter and handler configuration so that callers never need to
configure logging directly.

Usage
-----
Call `configure_logging()` once at application startup:

    from opencharge.core.logger import configure_logging
    configure_logging(level=logging.DEBUG)

All subsequent `logging.getLogger(__name__)` calls in any opencharge
module will inherit the configured handlers automatically.

Author:
    Ahmed Ghufran

License:
    Apache License 2.0
"""

from __future__ import annotations

import logging
import sys
from typing import IO


OPENCHARGE_LOGGER = "opencharge"

_DEFAULT_FORMAT = (
    "%(asctime)s.%(msecs)03d  "
    "%(levelname)-8s  "
    "%(name)-40s  "
    "%(message)s"
)
_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"


def configure_logging(
    level: int = logging.INFO,
    fmt: str = _DEFAULT_FORMAT,
    datefmt: str = _DATE_FORMAT,
    stream: IO[str] = sys.stdout,
    propagate: bool = False,
) -> logging.Logger:
    """
    Configure and return the root OpenCharge logger.

    Idempotent — calling this function multiple times will not add
    duplicate handlers.

    Parameters
    ----------
    level:
        Logging level (e.g. logging.DEBUG, logging.INFO).
    fmt:
        Log record format string.
    datefmt:
        Date format string.
    stream:
        Output stream (defaults to stdout).
    propagate:
        Whether to propagate records to the root Python logger.

    Returns
    -------
    logging.Logger
        The configured opencharge package logger.
    """
    logger = logging.getLogger(OPENCHARGE_LOGGER)

    # Guard against double-init, but only count our own StreamHandlers —
    # not pytest's LogCaptureHandler or other injected handlers.
    if any(type(h) is logging.StreamHandler for h in logger.handlers):
        return logger

    handler = logging.StreamHandler(stream)
    handler.setFormatter(logging.Formatter(fmt=fmt, datefmt=datefmt))
    logger.addHandler(handler)
    logger.setLevel(level)
    logger.propagate = propagate

    return logger


def get_logger(name: str) -> logging.Logger:
    """
    Return a child logger under the opencharge namespace.

    Parameters
    ----------
    name:
        Sub-logger name, typically the calling module's __name__.

    Returns
    -------
    logging.Logger
        A logger named 'opencharge.<name>'.
    """
    return logging.getLogger(f"{OPENCHARGE_LOGGER}.{name}")
