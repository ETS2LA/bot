import utils.variables as variables

from rich.highlighter import NullHighlighter, RegexHighlighter
from rich.logging import RichHandler
from rich.console import Console
import inspect
import logging
import os
import re

class level_names:
    '''Shortened level names for logging'''
    debug = 'DBG'
    info = 'INF'
    warning = 'WRN'
    error = 'ERR'
    critical = 'CRT'

    def level(self, level_name):
        '''Returns the shortened level name for the given level name'''
        return getattr(self, level_name.lower())

class FileFormatter(logging.Formatter):
    '''Logging formatter class for file output'''
    def __init__(self):
        super().__init__(datefmt="%m-%d-%y %H:%M:%S")

    def format(self, record):
        timestamp = self.formatTime(record, self.datefmt) # Timestamp
        level_name = f"[{level_names().level(record.levelname)}]" # Three character level name
        message = re.sub(r'\[.*?\]', '', record.getMessage()) # Remove rich markup

        # Get filename and line number
        filename = os.path.basename(getattr(record, 'custom_filename', record.filename))
        lineno = getattr(record, 'custom_lineno', record.lineno)

        return f"{timestamp} {level_name} ({filename}:{lineno}) {message}" # Return formatted message

def setup_global_logging():
    console = Console()
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    rich_handler = RichHandler(markup=True, show_path=False, console=console)
    logger.addHandler(rich_handler)

    if os.path.exists(variables.LOG_FILE):
        os.remove(variables.LOG_FILE)
    file_handler = logging.FileHandler(variables.LOG_FILE)
    file_handler.setFormatter(FileFormatter())
    logger.addHandler(file_handler)

    logger.info("Logger initialized")
    return logger