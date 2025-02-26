import os
from datetime import datetime

def get_file_date(file_path: str, use_creation_date: bool = False) -> datetime:
    """Gets creation or modification date of file."""
    timestamp = os.path.getctime(file_path) if use_creation_date else os.path.getmtime(file_path)
    return datetime.fromtimestamp(timestamp)

def format_date_prefix(date: datetime) -> str:
    """Formats date as YYYY-MM-DD-."""
    return date.strftime("%Y-%m-%d-")