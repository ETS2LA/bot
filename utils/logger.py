import utils.variables as variables
import logging
import os

def setup_logger():
    # Custom logger setup
    logger = logging.getLogger(variables.LOGGER_NAME)
    logger.setLevel(logging.INFO)

    # Console handler
    console_handler = logging.StreamHandler()
    logger.addHandler(console_handler)

    # File handler
    open(variables.LOG_FILE, 'w').close() # Clear the log file
    file_handler = logging.FileHandler(variables.LOG_FILE)
    logger.addHandler(file_handler)

    # Redirect the discordpy logger to the custom logger
    discord_logger = logging.getLogger('discord')
    discord_logger.setLevel(logging.INFO)
    discord_logger.handlers = []
    discord_logger.propagate = True
    logging.root.setLevel(logging.INFO)
    logging.root.addHandler(console_handler)
    logging.root.addHandler(file_handler)

    logger.info("Logger initialized")
    return logger