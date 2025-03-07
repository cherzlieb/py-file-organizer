import logging
import os
import sys
from .log_filter import ErrorOrDebugFilter

# Global debug mode for the entire application
_debug_mode = False

def configure_logging(debug_mode=False):
    """Konfiguriert das zentrale Logging für die gesamte Anwendung."""
    global _debug_mode
    _debug_mode = debug_mode

    # Create default logs folder
    log_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "logs")
    log_file = os.path.join(log_dir, 'file_organizer.log')
    os.makedirs(log_dir, exist_ok=True)

    # Configure root logger
    root_logger = logging.getLogger()

    # Remove all existing handlers
    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)

    # Set log level (always DEBUG, but the filter decides)
    root_logger.setLevel(logging.DEBUG)

    # Add file handler with filter
    file_handler = logging.FileHandler(log_file, encoding='utf-8')
    file_handler.setFormatter(logging.Formatter('%(asctime)s | %(levelname)s | %(message)s'))
    file_handler.addFilter(ErrorOrDebugFilter(debug_mode))
    root_logger.addHandler(file_handler)

    # Console handler for debug mode only
    if debug_mode:
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(logging.Formatter('%(asctime)s | %(levelname)s | %(message)s'))
        console_handler.addFilter(ErrorOrDebugFilter(debug_mode))
        root_logger.addHandler(console_handler)

    # Info for debugging
    if debug_mode:
        logging.debug("Logging konfiguriert: Debug-Modus AKTIV")
    else:
        logging.debug("Logging konfiguriert: Nur ERROR-Level")

def update_debug_mode(debug_mode):
    """Aktualisiere den Debug-Modus für alle Logger."""
    global _debug_mode
    _debug_mode = debug_mode

    # Update filter for all existing handlers
    root_logger = logging.getLogger()
    for handler in root_logger.handlers:
        # Remove all existing filters
        for f in handler.filters[:]:
            if isinstance(f, ErrorOrDebugFilter):
                handler.removeFilter(f)
        # Add new filter
        handler.addFilter(ErrorOrDebugFilter(debug_mode))

    # Info for debugging
    if debug_mode:
        logging.debug("Logging aktualisiert: Debug-Modus AKTIV")
    else:
        logging.debug("Logging aktualisiert: Nur ERROR-Level")

def get_logger(name):
    """Gibt einen Logger zurück, der korrekt konfiguriert ist."""
    return logging.getLogger(name)
