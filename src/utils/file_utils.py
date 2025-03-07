import os
import shutil
import logging
from datetime import datetime
from typing import Dict, List, Tuple, Optional
from .file_operations import move_file
from .date_utils import get_file_date, format_date_prefix
from .path_utils import get_destination_folder
from .filename_utils import FilenameProcessor
from core.config import OrganizerConfig


class FileOrganizerError(Exception):
    """Base exception for file organizer errors."""
    pass


class SourceFolderNotFoundError(FileOrganizerError):
    """Raised when source folder does not exist."""
    pass


def clean_filename(filename: str) -> str:
    """
    Replaces spaces and underscores with hyphens in a given filename.

    Parameters
    ----------
    filename : str
        The filename to clean.

    Returns
    -------
    str
        The filename with spaces and underscores replaced with hyphens.
    """
    return filename.replace(' ', '-').replace('_', '-')


def is_valid_date_prefix(filename: str) -> Tuple[bool, Optional[datetime]]:
    """
    Check if filename starts with a valid date prefix (YYYY-MM-DD-).

    Parameters
    ----------
    filename : str
        The filename to check

    Returns
    -------
    tuple
        (bool, datetime or None) - (is valid, parsed date if valid)
    """
    try:
        date_part = filename[:10]
        date_obj = datetime.strptime(date_part, "%Y-%m-%d")
        return filename[10] == '-', date_obj
    except (ValueError, IndexError):
        return False, None


def organize_files_by_type(config: OrganizerConfig) -> None:
    """Main organization function with high-level logic."""
    if not os.path.exists(config.source_folder):
        raise SourceFolderNotFoundError(
            f"Source folder not found: {config.source_folder}")

    try:
        results = process_directory(config)
        log_results(config.logger, results)
    except Exception as e:
        config.logger.error(f"Error during organization: {e}")
        raise FileOrganizerError(f"File organization failed: {e}")


def process_directory(config: OrganizerConfig) -> Tuple[int, int]:
    """Processes all files in directory."""
    files_moved = 0
    folders_moved = 0

    for item_name in os.listdir(config.source_folder):
        if should_skip_item(item_name, config):
            continue

        item_path = os.path.join(config.source_folder, item_name)

        if os.path.isfile(item_path):
            files_moved += process_file(item_path, item_name, config)
        elif os.path.isdir(item_path):
            folders_moved += process_folder(item_path, item_name, config)

    return files_moved, folders_moved


def process_file(item_path: str, item_name: str, config: OrganizerConfig) -> int:
    """Process a single file."""
    try:
        # Get file date
        file_date = get_file_date(item_path, config.use_creation_date)

        # Check if filename already has a valid date prefix
        has_valid_date, existing_date = FilenameProcessor.parse_date_prefix(
            item_name)

        if has_valid_date and not config.force_date:
            # Keep original name if date is valid and force_date is False
            new_filename = item_name
        else:
            # Create new filename with date prefix
            new_filename = FilenameProcessor.create_dated_filename(
                item_name, file_date)

        # Get file extension and determine destination
        file_extension = os.path.splitext(item_name)[1].lower()
        destination_folder = get_destination_folder(
            file_extension, config.organized_folder, config.file_types)

        if destination_folder:
            if not os.path.exists(destination_folder):
                os.makedirs(destination_folder)

            destination_path = os.path.join(destination_folder, new_filename)
            config.logger.info(
                f"Moving file: {item_name} -> {destination_folder} as {new_filename}")

            if move_file(item_path, destination_path, config.logger):
                return 1  # Successfully moved

        return 0  # Not moved (no matching destination folder)

    except Exception as e:
        config.logger.error(f"Error processing file {item_name}: {str(e)}")
        return 0  # Error case


def process_folder(item_path: str, item_name: str, config: OrganizerConfig) -> int:
    """Process a single folder."""
    try:
        if config.date_folders:
            # Get folder date and create new name with date prefix
            folder_date = get_file_date(item_path, config.use_creation_date)
            new_foldername = FilenameProcessor.create_dated_filename(
                item_name, folder_date)
            destination_path = os.path.join(
                config.unorganized_folder, new_foldername)
        else:
            # Use original folder name
            destination_path = os.path.join(
                config.unorganized_folder, item_name)

        config.logger.info(
            f"Moving folder: {item_name} -> {config.unorganized_folder}")

        if move_file(item_path, destination_path, config.logger):
            return 1  # Successfully moved
        return 0  # Not moved

    except Exception as e:
        config.logger.error(f"Error processing folder {item_name}: {str(e)}")
        return 0  # Error case


def should_skip_item(item_name: str, config: OrganizerConfig) -> bool:
    """
    Determines if an item should be skipped during processing.

    Parameters
    ----------
    item_name : str
        Name of the file or folder to check
    config : OrganizerConfig
        Configuration object containing paths

    Returns
    -------
    bool
        True if item should be skipped, False otherwise
    """
    # Skip the organized and unorganized folders
    organized_base = os.path.basename(config.organized_folder)
    unorganized_base = os.path.basename(config.unorganized_folder)

    return item_name in [organized_base, unorganized_base]


def log_results(logger: logging.Logger, results: Tuple[int, int]) -> None:
    """
    Logs the results of the file organization.

    Parameters
    ----------
    logger : logging.Logger
        Logger instance to use
    results : Tuple[int, int]
        Tuple containing (files_moved, folders_moved)
    """
    files_moved, folders_moved = results
    logger.info("Organization complete!")
    logger.info(f"Files moved: {files_moved}")
    logger.info(f"Folders moved: {folders_moved}")
