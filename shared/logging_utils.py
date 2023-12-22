"""
Module for logging utilities.

This module contains functions for setting up and configuring loggers,
facilitating consistent logging practices across the application.
"""

import logging
import os
import sys

def get_logger(name):
    """
    Create a configured logger.

    Args:
        name (str): Name of the logger.
        level: Logging level, e.g., logging.INFO, logging.DEBUG.

    Returns:
        logging.Logger: Configured logger instance.
    """
    # Read log level from environment variable or default to INFO
    log_level_name = os.getenv('LOG_LEVEL', 'INFO').upper()
    level = getattr(logging, log_level_name, logging.INFO)

    logger = logging.getLogger(name)
    logger.setLevel(level)

    # Define different Formatter formats based on verbosity required
    verbose_format = (
        'time=%(asctime)s level=%(levelname)s app=%(name)s '
        'file=%(pathname)s:%(lineno)d method=%(funcName)s '
        'proc_id=%(process)d thread_id=%(thread)d msg="%(message)s"'
    )
    default_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    # simple_format = '%(levelname)s - %(message)s'

    # Select formatter based on the log level
    if level <= logging.DEBUG:
        # Create the more detailed formatter for DEBUG level
        formatter = logging.Formatter(verbose_format)
    else:
        # Create the simpler formatter for higher levels like INFO
        formatter = logging.Formatter(default_format)

    # Create console handler and set level
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(level)

    # Add formatter to console_handler
    console_handler.setFormatter(formatter)

    # Add console_handler to logger
    if not logger.handlers:
        logger.addHandler(console_handler)

    return logger
