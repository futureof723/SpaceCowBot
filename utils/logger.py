import logging
import colorlog

# Configure logging with color
log_formatter = colorlog.ColoredFormatter(
    "%(log_color)s%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    reset=True,
    log_colors={
        'DEBUG': 'cyan',
        'INFO': 'green',
        'WARNING': 'yellow',
        'ERROR': 'red',
        'CRITICAL': 'bold_red',
    }
)

# Create and configure the logger
logger = colorlog.getLogger("studybot")
handler = logging.StreamHandler()
handler.setFormatter(log_formatter)
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)
