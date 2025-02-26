import os
import logging
from utils.file_utils import organize_files
from utils.file_types import FILE_TYPES

# Setup logging with more detailed output
logging.basicConfig(
    level=logging.DEBUG,
    format='%(message)s'  # Simplified format for cleaner output
)
logger = logging.getLogger(__name__)

# Change Downloads folder path to your specific location
DOWNLOADS_FOLDER = "E:/Downloads"
ORGANIZED_FOLDER = os.path.join(DOWNLOADS_FOLDER, "Organized")

# Add debug output to verify paths
print(f"Downloads folder path: {DOWNLOADS_FOLDER}")
print(f"Organized folder path: {ORGANIZED_FOLDER}")

# Check if Downloads folder exists and list contents
if os.path.exists(DOWNLOADS_FOLDER):
    print("\nFiles in Downloads folder:")
    for file in os.listdir(DOWNLOADS_FOLDER):
        print(f"- {file}")
else:
    print(f"Warning: Downloads folder not found at {DOWNLOADS_FOLDER}")


if __name__ == "__main__":
    organize_files(download_folder=DOWNLOADS_FOLDER, organized_folder=ORGANIZED_FOLDER, file_types=FILE_TYPES, logger=logger)
