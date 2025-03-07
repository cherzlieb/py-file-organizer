import os
import sqlite3
import logging
from typing import Dict, List, Any, Optional
from pathlib import Path
from utils.logger import get_logger

class DatabaseManager:
    """Manages database operations for configuration and file types."""

    DB_FILE = "fileorganizer.db"

    def __init__(self, db_path: Optional[str] = None):
        """Initialize database connection."""
        # Use specified path or default to app directory
        if db_path:
            self.db_path = db_path
        else:
            # Store in user's home directory or app directory
            app_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
            self.db_path = os.path.join(app_dir, self.DB_FILE)

        self.conn = None
        self.logger = get_logger(__name__)

    def connect(self) -> None:
        """Connect to the database."""
        try:
            self.conn = sqlite3.connect(self.db_path)
            self.conn.row_factory = sqlite3.Row
        except sqlite3.Error as e:
            self.logger.error(f"Database connection error: {e}")
            raise

    def close(self) -> None:
        """Close the database connection."""
        if self.conn:
            self.conn.close()
            self.conn = None

    def initialize_database(self) -> None:
        """Create database tables if they don't exist."""
        try:
            self.connect()
            cursor = self.conn.cursor()

            # Create config table
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS config (
                key TEXT PRIMARY KEY,
                value TEXT
            )
            ''')

            # Create file_types table
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS file_types (
                folder_name TEXT NOT NULL,
                extension TEXT NOT NULL,
                PRIMARY KEY (folder_name, extension)
            )
            ''')

            self.conn.commit()
            self.logger.debug("Database initialized successfully")
        except sqlite3.Error as e:
            self.logger.error(f"Database initialization error: {e}")
            raise
        finally:
            self.close()

    def populate_default_config(self, default_config: Dict[str, str]) -> None:
        """Populate the config table with default values if empty."""
        try:
            self.connect()
            cursor = self.conn.cursor()

            # Check if config table is empty
            cursor.execute("SELECT COUNT(*) FROM config")
            count = cursor.fetchone()[0]

            if count == 0:
                for key, value in default_config.items():
                    cursor.execute(
                        "INSERT INTO config (key, value) VALUES (?, ?)",
                        (key, value)
                    )
                self.conn.commit()
                self.logger.debug("Default configuration populated")
        except sqlite3.Error as e:
            self.logger.error(f"Error populating default config: {e}")
            raise
        finally:
            self.close()

    def populate_default_file_types(self, file_types: Dict[str, List[str]]) -> None:
        """Populate the file_types table with default values if empty."""
        try:
            self.connect()
            cursor = self.conn.cursor()

            # Check if file_types table is empty
            cursor.execute("SELECT COUNT(*) FROM file_types")
            count = cursor.fetchone()[0]

            if count == 0:
                for folder_name, extensions in file_types.items():
                    for ext in extensions:
                        cursor.execute(
                            "INSERT INTO file_types (folder_name, extension) VALUES (?, ?)",
                            (folder_name, ext)
                        )
                self.conn.commit()
                self.logger.debug("Default file types populated")
        except sqlite3.Error as e:
            self.logger.error(f"Error populating default file types: {e}")
            raise
        finally:
            self.close()

    def get_config(self) -> Dict[str, str]:
        """Get all configuration values."""
        try:
            self.connect()
            cursor = self.conn.cursor()
            cursor.execute("SELECT key, value FROM config")
            config = {row['key']: row['value'] for row in cursor.fetchall()}
            return config
        except sqlite3.Error as e:
            self.logger.error(f"Error retrieving configuration: {e}")
            return {}
        finally:
            self.close()

    def update_config(self, config: Dict[str, str]) -> None:
        """Update configuration values."""
        try:
            self.connect()
            cursor = self.conn.cursor()
            for key, value in config.items():
                cursor.execute(
                    "INSERT OR REPLACE INTO config (key, value) VALUES (?, ?)",
                    (key, str(value))
                )
            self.conn.commit()
            self.logger.debug("Configuration updated")
        except sqlite3.Error as e:
            self.logger.error(f"Error updating configuration: {e}")
            raise
        finally:
            self.close()

    def get_file_types(self) -> Dict[str, List[str]]:
        """Get all file types."""
        try:
            self.connect()
            cursor = self.conn.cursor()
            cursor.execute("SELECT folder_name, extension FROM file_types ORDER BY folder_name")

            file_types = {}
            for row in cursor.fetchall():
                folder_name = row['folder_name']
                extension = row['extension']
                if folder_name not in file_types:
                    file_types[folder_name] = []
                file_types[folder_name].append(extension)

            return file_types
        except sqlite3.Error as e:
            self.logger.error(f"Error retrieving file types: {e}")
            return {}
        finally:
            self.close()

    def add_file_type(self, folder_name: str, extension: str) -> bool:
        """Add a new file type."""
        try:
            self.connect()
            cursor = self.conn.cursor()
            cursor.execute(
                "INSERT OR IGNORE INTO file_types (folder_name, extension) VALUES (?, ?)",
                (folder_name, extension)
            )
            self.conn.commit()
            return cursor.rowcount > 0
        except sqlite3.Error as e:
            self.logger.error(f"Error adding file type: {e}")
            return False
        finally:
            self.close()

    def remove_file_type(self, folder_name: str, extension: str) -> bool:
        """Remove a file type."""
        try:
            self.connect()
            cursor = self.conn.cursor()
            cursor.execute(
                "DELETE FROM file_types WHERE folder_name = ? AND extension = ?",
                (folder_name, extension)
            )
            self.conn.commit()
            return cursor.rowcount > 0
        except sqlite3.Error as e:
            self.logger.error(f"Error removing file type: {e}")
            return False
        finally:
            self.close()

    def rename_folder(self, old_name: str, new_name: str) -> bool:
        """Rename a folder and all its associated file types."""
        if old_name == new_name:
            return True

        try:
            self.connect()
            cursor = self.conn.cursor()
            cursor.execute(
                "UPDATE file_types SET folder_name = ? WHERE folder_name = ?",
                (new_name, old_name)
            )
            self.conn.commit()
            return cursor.rowcount > 0
        except sqlite3.Error as e:
            self.logger.error(f"Error renaming folder: {e}")
            return False
        finally:
            self.close()

    def delete_folder(self, folder_name: str) -> bool:
        """Delete a folder and all its associated file types."""
        try:
            self.connect()
            cursor = self.conn.cursor()
            cursor.execute(
                "DELETE FROM file_types WHERE folder_name = ?",
                (folder_name,)
            )
            self.conn.commit()
            return cursor.rowcount > 0
        except sqlite3.Error as e:
            self.logger.error(f"Error deleting folder: {e}")
            return False
        finally:
            self.close()

    def create_folder(self, folder_name: str) -> bool:
        """Create a new folder (placeholder entry with a dummy extension that will be removed)."""
        try:
            self.connect()
            # No action needed as folders are implicit through file_types entries
            # Return True to indicate success
            return True
        except sqlite3.Error as e:
            self.logger.error(f"Error creating folder: {e}")
            return False
        finally:
            self.close()

    def get_folder_count(self, folder_name: str) -> int:
        """Get the number of extensions in a folder."""
        try:
            self.connect()
            cursor = self.conn.cursor()
            cursor.execute(
                "SELECT COUNT(*) FROM file_types WHERE folder_name = ?",
                (folder_name,)
            )
            return cursor.fetchone()[0]
        except sqlite3.Error as e:
            self.logger.error(f"Error counting folder extensions: {e}")
            return 0
        finally:
            self.close()
