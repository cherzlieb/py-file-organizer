import re
from datetime import datetime
from typing import Tuple, Optional

class FilenameProcessor:
    """Handles all filename-related operations following best practices."""
    
    DATE_FORMAT = "%Y-%m-%d"
    DATE_SEPARATOR = "-"
    INVALID_CHARS_PATTERN = r'[<>:"/\\|?*]'
    
    @staticmethod
    def sanitize_filename(filename: str) -> str:
        """
        Sanitizes a filename by removing/replacing invalid characters.
        
        Parameters
        ----------
        filename : str
            Original filename
            
        Returns
        -------
        str
            Sanitized filename
        """
        # Remove invalid characters
        clean_name = re.sub(FilenameProcessor.INVALID_CHARS_PATTERN, '', filename)
        # Replace spaces and underscores with hyphens
        clean_name = clean_name.replace(' ', '-').replace('_', '-')
        # Remove multiple consecutive hyphens
        clean_name = re.sub(r'-+', '-', clean_name)
        # Remove leading/trailing hyphens
        clean_name = clean_name.strip('-')
        return clean_name

    @staticmethod
    def parse_date_prefix(filename: str) -> Tuple[bool, Optional[datetime]]:
        """
        Checks if filename starts with a valid date prefix.
        
        Parameters
        ----------
        filename : str
            Filename to check
            
        Returns
        -------
        Tuple[bool, Optional[datetime]]
            (has_valid_date, datetime_object if valid)
        """
        try:
            date_part = filename[:10]
            date_obj = datetime.strptime(date_part, FilenameProcessor.DATE_FORMAT)
            has_separator = filename[10] == FilenameProcessor.DATE_SEPARATOR
            return has_separator, date_obj
        except (ValueError, IndexError):
            return False, None

    @staticmethod
    def create_dated_filename(original_filename: str, file_date: datetime) -> str:
        """
        Creates a filename with date prefix.
        
        Parameters
        ----------
        original_filename : str
            Original filename
        file_date : datetime
            Date to use as prefix
            
        Returns
        -------
        str
            New filename with date prefix
        """
        date_prefix = file_date.strftime(f"{FilenameProcessor.DATE_FORMAT}-")
        clean_name = FilenameProcessor.sanitize_filename(original_filename)
        
        # Remove existing date prefix if present
        has_date, _ = FilenameProcessor.parse_date_prefix(clean_name)
        if has_date:
            clean_name = clean_name[11:]
            
        return f"{date_prefix}{clean_name}"