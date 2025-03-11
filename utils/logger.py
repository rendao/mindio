import logging
from os import getenv
from rich.logging import RichHandler

LOGGER_NAME = "mindio"
LOG_LEVEL = getenv("LOG_LEVEL", "INFO")

# Define common log formats
LOG_FORMAT = {
    "DEBUG": "%(asctime)s [%(levelname)s] [%(name)s] %(message)s",
    "INFO": "%(asctime)s [%(levelname)s] %(message)s",
    "WARNING": "%(asctime)s [%(levelname)s] %(message)s",
    "ERROR": "%(asctime)s [%(levelname)s] [%(name)s] %(message)s",
    "CRITICAL": "%(asctime)s [%(levelname)s] [%(name)s] %(message)s"
}

# Create a global logger instance
_logger = logging.getLogger(LOGGER_NAME)

# Configure the logger once at module level
def setup_logger():
    """Configure the logger with handlers"""
    # Set log level
    _logger.setLevel(logging.getLevelName(LOG_LEVEL))
    
    # Clear any existing handlers to avoid duplicates
    if _logger.handlers:
        _logger.handlers = []
    
    # Set log format
    formatter = logging.Formatter(LOG_FORMAT[LOG_LEVEL])
    
    # File handler
    file_handler = logging.FileHandler("mindio.log")
    file_handler.setFormatter(formatter)
    
    # Console handler with Rich formatting
    console_handler = RichHandler()
    console_handler.setFormatter(formatter)
    
    # Add handlers
    _logger.addHandler(file_handler)
    _logger.addHandler(console_handler)

# Initialize the logger
setup_logger()

def log(level: str, message: str):
    """Log a message at the specified level"""
    level_upper = level.upper()
    if level_upper == "DEBUG":
        _logger.debug(message)
    elif level_upper == "INFO":
        _logger.info(message)
    elif level_upper == "WARNING":
        _logger.warning(message)
    elif level_upper == "ERROR":
        _logger.error(message)
    elif level_upper == "CRITICAL":
        _logger.critical(message)
    else:
        _logger.info(message)  # Default to INFO level

# For backwards compatibility
def logger(level: str, message: str):
    """Legacy function for logging (for backward compatibility)"""
    log(level, message)
