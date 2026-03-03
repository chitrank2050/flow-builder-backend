"""
Logging Configuration Module.

This module configures Loguru to handle all application logging.
It intercepts standard library logs (logging module) and routes them through Loguru,
ensuring consistent formatting across all dependencies (like httpx, tenacity).

It also uses a custom sink to write to sys.stderr in a way that is compatible
with Rich progress bars (preventing visual corruption).
"""

import logging
import sys
from typing import Union

from loguru import logger

from .config import settings


class InterceptHandler(logging.Handler):
    """
    Redirect standard logging messages (stdlib) to Loguru.
    This ensures libraries like 'httpx' or 'tenacity' look beautiful too.
    """

    def emit(self, record: logging.LogRecord) -> None:
        # Get corresponding Loguru level if it exists
        try:
            level: Union[str, int] = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno

        # Find caller from where originated the logged message
        frame, depth = logging.currentframe(), 2
        while frame and frame.f_code.co_filename == logging.__file__:
            frame = frame.f_back
            depth += 1

        logger.opt(depth=depth, exception=record.exc_info).log(
            level, record.getMessage()
        )


def rich_compatible_sink(message: str) -> None:
    """
    Custom sink that writes to stderr.
    This is required for 'rich' to properly intercept and reprint logs
    above the active progress bar.
    """
    sys.stderr.write(message)
    sys.stderr.flush()


def setup_logger():
    """
    Configures the Loguru logger with project settings.
    """
    # Intercept Standard Library Logs
    logging.root.handlers = [InterceptHandler()]

    # Set the root logger level to the configured level to ensure interception works
    logging.root.setLevel(settings.LOG_LEVEL)

    # Reset Loguru Configuration
    logger.remove()

    # Add the Console Handler
    # Uses the 'rich_compatible_sink' to play nice with progress bars
    logger.add(
        sink=rich_compatible_sink,
        format=settings.LOG_FORMAT,
        level=settings.LOG_LEVEL,
        colorize=True,
        enqueue=True,  # Thread-safe logging
        backtrace=True,
        diagnose=True,
    )

    # Silence Noisy Libraries
    # We generally want to see errors, but not INFO/DEBUG from these unless configured
    noisy_modules = ["httpx", "httpcore", "asyncio", "urllib3"]
    for module_name in noisy_modules:
        logging.getLogger(module_name).setLevel(logging.WARNING)

    return logger


# Singleton Logger Instance
log = setup_logger()
