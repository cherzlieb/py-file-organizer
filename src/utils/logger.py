import logging
import os
import sys
from .log_filter import ErrorOrDebugFilter

# Globaler Debug-Modus für die gesamte Anwendung
_debug_mode = False

def configure_logging(debug_mode=False):
    """Konfiguriert das zentrale Logging für die gesamte Anwendung."""
    global _debug_mode
    _debug_mode = debug_mode

    # Standardmäßigen Logs-Ordner erstellen
    log_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "logs")
    log_file = os.path.join(log_dir, 'file_organizer.log')
    os.makedirs(log_dir, exist_ok=True)

    # Root Logger konfigurieren
    root_logger = logging.getLogger()

    # Alle bestehenden Handler entfernen
    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)

    # Log-Level setzen (immer DEBUG, aber der Filter entscheidet)
    root_logger.setLevel(logging.DEBUG)

    # Datei-Handler mit Filter hinzufügen
    file_handler = logging.FileHandler(log_file, encoding='utf-8')
    file_handler.setFormatter(logging.Formatter('%(asctime)s | %(levelname)s | %(message)s'))
    file_handler.addFilter(ErrorOrDebugFilter(debug_mode))
    root_logger.addHandler(file_handler)

    # Console-Handler nur für Debug-Modus
    if debug_mode:
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(logging.Formatter('%(asctime)s | %(levelname)s | %(message)s'))
        console_handler.addFilter(ErrorOrDebugFilter(debug_mode))
        root_logger.addHandler(console_handler)

    # Info für Debugging
    if debug_mode:
        logging.debug("Logging konfiguriert: Debug-Modus AKTIV")
    else:
        logging.debug("Logging konfiguriert: Nur ERROR-Level")

def update_debug_mode(debug_mode):
    """Aktualisiere den Debug-Modus für alle Logger."""
    global _debug_mode
    _debug_mode = debug_mode

    # Filter für alle bestehenden Handler aktualisieren
    root_logger = logging.getLogger()
    for handler in root_logger.handlers:
        # Alle bestehenden Filter entfernen
        for f in handler.filters[:]:
            if isinstance(f, ErrorOrDebugFilter):
                handler.removeFilter(f)
        # Neuen Filter hinzufügen
        handler.addFilter(ErrorOrDebugFilter(debug_mode))

    # Info für Debugging
    if debug_mode:
        logging.debug("Logging aktualisiert: Debug-Modus AKTIV")
    else:
        logging.debug("Logging aktualisiert: Nur ERROR-Level")

def get_logger(name):
    """Gibt einen Logger zurück, der korrekt konfiguriert ist."""
    return logging.getLogger(name)
