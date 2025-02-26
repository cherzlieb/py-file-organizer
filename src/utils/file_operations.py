import os
import shutil
import logging
from typing import Optional

def move_file(source_path: str, destination_path: str, logger: logging.Logger) -> bool:
    """Moves a single file to destination."""
    try:
        if not os.path.exists(os.path.dirname(destination_path)):
            os.makedirs(os.path.dirname(destination_path))
            logger.info(f"Created destination folder: {os.path.dirname(destination_path)}")
        
        shutil.move(source_path, destination_path)
        return True
    except Exception as e:
        logger.error(f"Error moving file {source_path}: {str(e)}")
        return False