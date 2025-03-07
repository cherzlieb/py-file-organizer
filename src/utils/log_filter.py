import logging
from typing import Optional

class ErrorOrDebugFilter(logging.Filter):
    """
    Filter für Logger: Lässt alle ERROR-Logs durch, aber andere Levels nur wenn Debug aktiviert ist.
    """
    def __init__(self, debug_mode: bool = False):
        super().__init__()
        self.debug_mode = debug_mode

    def filter(self, record):
        # ERROR (40) und kritischere Logs immer durchlassen
        if record.levelno >= 40:  # ERROR oder höher
            return True
        # Andere Logs nur durchlassen, wenn Debug-Modus aktiv ist
        return self.debug_mode
