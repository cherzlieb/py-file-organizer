import os
from typing import Dict, List, Optional

def get_destination_folder(file_extension: str, organized_folder: str, file_types: Dict[str, List[str]]) -> Optional[str]:
    """
    Determines the destination folder based on file extension.
    
    Parameters
    ----------
    file_extension : str
        The file extension to check
    organized_folder : str
        Base path for organized files
    file_types : Dict[str, List[str]]
        Dictionary mapping folder names to lists of file extensions
        
    Returns
    -------
    Optional[str]
        Path to destination folder or None if no match found
    """
    for folder_name, extensions in file_types.items():
        if file_extension.lower() in extensions:
            return os.path.join(organized_folder, folder_name)
    return None