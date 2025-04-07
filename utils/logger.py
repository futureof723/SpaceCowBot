"""
🔧 logger.py

This module sets up a colorized logger using the `colorlog` library for enhanced
readability in terminal outputs. The logger is used throughout the application
to provide consistent, formatted logging at different severity levels.

Log format example:
[INFO] 2025-04-07 12:00:00 - Message content

Color coding:
- DEBUG: cyan
- INFO: green
- WARNING: yellow
- ERROR: red
- CRITICAL: bold red

Usage:
    from utils.logger import logger
    logger.info("This is an info message.")
"""

import logging
import colorlog

# 🖌 Configure the log message format with color and timestamp
log_formatter = colorlog.ColoredFormatter(
    "%(log_color)s%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    reset=True,
    log_colors={
        'DEBUG': 'cyan',         # Cyan for debug messages
        'INFO': 'green',         # Green for general info
        'WARNING': 'yellow',     # Yellow for warnings
        'ERROR': 'red',          # Red for errors
        'CRITICAL': 'bold_red',  # Bold red for critical issues
    }
)

# 🧱 Create the logger instance used throughout the project
logger = colorlog.getLogger("studybot")

# 📦 Create a handler to stream logs to stdout (e.g., terminal or server logs)
handler = logging.StreamHandler()

# 🎨 Attach the colorized formatter to the handler
handler.setFormatter(log_formatter)

# 🔌 Attach the handler to the logger
logger.addHandler(handler)

# 🔊 Set default logging level (DEBUG captures everything)
logger.setLevel(logging.DEBUG)
