#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ─────────────────────────────────────────────────────────────────────────────
# Module Documentation
# ─────────────────────────────────────────────────────────────────────────────

"""
Module Overview
───────────────
Purpose
    Establish a structured, color-coded logging framework that makes 
    console messages semantically distinct and immediately interpretable 
    for data processing and debugging workflows.

Context
    Complex pipelines often generate unstructured, hard-to-read logs. 
    This module addresses that problem by providing developer-friendly 
    logging methods with clear semantics, aligned labels, and Rich formatting.

Semantics
    Provides dynamically created semantic log methods, including:
    read, write, meta, stage, step, substep, info, config, metric, result,
    warning, alert, error, check, debug.

Note
    The logger methods are generated dynamically, making it easy to add, 
    remove, or modify log semantics without altering the core class.

Usage
─────
    # Import and instantiate
    from rich_logger import RichLogger
    logger = RichLogger("project_name")

    # Use semantic log methods
    logger.read("Loading dataset")
    logger.metric("MAE=3.21 RMSE=4.09")
    logger.error("Failed to write output file")
    logger.debug("Developer check details")

Dependencies
────────────
- rich >= 13.0
- Python standard logging

Limitations
───────────
- Tested with Python 3.13.
- Designed for console output; file logging requires additional handlers.
- Rich formatting may not render properly in non-compatible terminals.
- Traceback cannot be toggled.
"""

__author__  = "Aidan Calderhead"
__created__ = "2025-10-14"
__license__ = "MIT"

# ─────────────────────────────────────────────────────────────────────────────
# Imports
# ─────────────────────────────────────────────────────────────────────────────

import logging
from rich.logging import RichHandler
from rich.console import Console

# ─────────────────────────────────────────────────────────────────────────────
# Logger Class
# ─────────────────────────────────────────────────────────────────────────────

class RichLogger:
    """
    Extends Python’s `logging` with dynamically attached, semantically distinct
    log methods (e.g., `.process()`, `.warn()`, `.metric()`) defined by 
    `LOG_CATEGORIES`. Each category specifies a label, color, and logging level
    for consistent, readable console output.
    """

    # ─────────────────────────────────
    # Core Logging Categories
    # ─────────────────────────────────
    LOG_CATEGORIES = {
        # I/O Management
        "read": {
            "label": "READ", 
            "color": "magenta",
            "level": logging.INFO
        },
        "write": {
            "label": "WRITE", 
            "color": "magenta", 
            "level": logging.INFO
        },
        "meta": {
            "label": "METADATA", 
            "color": "magenta", 
            "level": logging.INFO
        },

        # Processing Checkpoints
        "stage": {
            "label": "STAGE", 
            "color": "blue", 
            "level": logging.INFO
        },
        "step": {
            "label": "STEP", 
            "color": "blue", 
            "level": logging.INFO
        },
        "substep": {
            "label": "SUB", 
            "color": "blue", 
            "level": logging.INFO
        },
        "info": {
            "label": "STATUS", 
            "color": "blue", 
            "level": logging.INFO
        },

        # Processing Figures
        "config": {
            "label": "CONFIG", 
            "color": "cyan", 
            "level": logging.INFO
        },
        "metric": {
            "label": "METRIC", 
            "color": "cyan", 
            "level": logging.INFO
        },
        "result": {
            "label": "RESULT", 
            "color": "cyan", 
            "level": logging.INFO
        },

        # Warnings and Errors
        "warning": {
            "label": "WARNING", 
            "color": "yellow", 
            "level": logging.WARNING
        },
        "alert": {
            "label": "ALERT", 
            "color": "red", 
            "level": logging.ERROR
        },
        "error": {
            "label": "ERROR", 
            "color": "red", 
            "level": logging.ERROR
        },

        # Code Development
        "check":  {
            "label": "CHECK", 
            "color": "green", 
            "level": logging.DEBUG
        },
        "debug":  {
            "label": "DEBUG", 
            "color": "green", 
            "level": logging.DEBUG
        },
    }

    # ─────────────────────────────────
    # Initialization
    # ─────────────────────────────────
    def __init__(self, name: str):
        """
        Initializes the custom Rich-enhanced logger.

        Creates a Rich console for styled output and configures a standard
        Python logger with a RichHandler to display timestamps, paths, and 
        colorized text. If no handlers exist, one is added to prevent duplicate
        log output. Finally, dynamically attaches category-specific log methods
        via `_attach_log_methods()`.
        """
        self.console = Console()
        self.logger  = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)

        # Add RichHandler if no handlers exist
        if not self.logger.handlers:
            handler = RichHandler(
                console    = self.console,
                show_time  = True,     # Display timestamps
                show_level = False,    # Hide default logging levels
                show_path  = True,     # Show file path and line number
                markup     = True,
                rich_tracebacks = True
            )
            handler.setLevel(logging.NOTSET)  # Pass all messages through
            self.logger.addHandler(handler)
            self.logger.propagate = False     # Avoid duplicate messages

        # Dynamically attach logging methods
        self._attach_log_methods()

    # ─────────────────────────────────
    # Core Logging Method
    # ─────────────────────────────────
    def log(self, message, label, level = logging.DEBUG, color = "white"):
        """
        Logs a message with a color-formatted label using Rich markup.

        Applies color styling to the label, aligns it for readability, and 
        passes the formatted message to the underlying logger at logging level
        that will catch all messages without filtering. Include the traceback
        to the most recent call when `verbose()` is called.
        """
        rich_label = f"[{color}]{label:<8}[/]"

        self.logger.log(
            level,
            f"{rich_label} {message}",
            exc_info = label.upper() in {"DEBUG"}
        )

    # ─────────────────────────────────
    # Dynamic Method Attachment
    # ─────────────────────────────────
    def _attach_log_methods(self):
        """
        Dynamically creates and binds instance methods for each log category.

        For every entry in LOG_CATEGORIES, this function defines a new method
        on the instance (e.g., `self.info()`, `self.error()`, etc.) that logs 
        messages with the corresponding label, color, and log level specified 
        in that category.
        """
        for method_name, properties in self.LOG_CATEGORIES.items():
            def log_method(self, message, props = properties):
                self.log(
                    message, 
                    props["label"], 
                    color = props["color"], 
                    level = props["level"]
                )
            
            setattr(
                self, 
                method_name, 
                log_method.__get__(self, self.__class__)
            )
