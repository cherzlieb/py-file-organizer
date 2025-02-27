from dataclasses import dataclass
from typing import Dict, List
import logging

@dataclass
class Config:
    DEBUG: bool = False
    DATE_FORMAT: str = "%Y-%m-%d-"
    LOG_FORMAT: str = "%(asctime)s | %(message)s"
    LOG_LEVEL: int = logging.DEBUG
    LOG_FILE: str = "logs/file_organizer.log"
    DATE_FMT: str = "%Y-%m-%d %H:%M:%S"  # Neues Datumsformat ohne Millisekunden

@dataclass
class OrganizerConfig:
    source_folder: str
    organized_folder: str
    unorganized_folder: str
    file_types: Dict[str, List[str]]
    logger: logging.Logger
    use_creation_date: bool = False
    force_date: bool = False
    date_folders: bool = False  # New setting