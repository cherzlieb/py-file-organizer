from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                              QHBoxLayout, QLabel, QLineEdit, QPushButton,
                              QCheckBox, QFileDialog, QMessageBox)
from PySide6.QtCore import Qt
import sys
import os
import logging
from dotenv import load_dotenv, set_key
from utils.file_utils import organize_files_by_type
from utils.file_types import FILE_TYPES
from config import OrganizerConfig

class FileOrganizerGUI(QMainWindow):
    def __init__(self, logger):
        """Initialize the GUI with logger from main."""
        super().__init__()
        self.logger = logger
        self.setWindowTitle("File Organizer Configuration")
        self.setMinimumWidth(600)

        # Create central widget and main layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)

        # Load current values
        load_dotenv()
        self.current_values = {
            'SOURCE_FOLDER': os.getenv('SOURCE_FOLDER', ''),
            'ORGANIZED_FOLDER': os.getenv('ORGANIZED_FOLDER', ''),
            'UNORGANIZED_FOLDER': os.getenv('UNORGANIZED_FOLDER', ''),
            'DEBUG': os.getenv('DEBUG', 'False'),
            'USE_CREATION_DATE': os.getenv('USE_CREATION_DATE', 'False'),
            'FORCE_DATE': os.getenv('FORCE_DATE', 'False')
        }

        # Create folder entries
        self.folder_entries = {}
        for key, label in [
            ('SOURCE_FOLDER', 'Source Folder:'),
            ('ORGANIZED_FOLDER', 'Organized Folder:'),
            ('UNORGANIZED_FOLDER', 'Unorganized Folder:')
        ]:
            self.create_folder_entry(main_layout, label, key)

        # Create checkboxes
        self.debug_cb = QCheckBox("Debug Mode")
        self.creation_date_cb = QCheckBox("Use Creation Date")
        self.force_date_cb = QCheckBox("Force Date")
        self.date_folders_cb = QCheckBox("Add Date to Folders")  # New checkbox

        # Set checkbox states
        self.debug_cb.setChecked(self.current_values['DEBUG'].lower() == 'true')
        self.creation_date_cb.setChecked(self.current_values['USE_CREATION_DATE'].lower() == 'true')
        self.force_date_cb.setChecked(self.current_values['FORCE_DATE'].lower() == 'true')
        self.date_folders_cb.setChecked(self.current_values.get('DATE_FOLDERS', 'False').lower() == 'true')  # New setting

        # Add checkboxes to layout
        main_layout.addWidget(self.debug_cb)
        main_layout.addWidget(self.creation_date_cb)
        main_layout.addWidget(self.force_date_cb)
        main_layout.addWidget(self.date_folders_cb)  # Add new checkbox

        # Create button container
        button_container = QWidget()
        button_layout = QHBoxLayout(button_container)
        
        # Create save and start buttons
        save_button = QPushButton("Save Configuration")
        start_button = QPushButton("Start Sorting")
        save_button.clicked.connect(self.save_config)
        start_button.clicked.connect(self.start_sorting)
        
        button_layout.addWidget(save_button)
        button_layout.addWidget(start_button)
        main_layout.addWidget(button_container)

        # Add some spacing
        main_layout.addStretch()

    def create_folder_entry(self, layout, label_text, key):
        """Create a folder entry row."""
        container = QWidget()
        hbox = QHBoxLayout(container)
        hbox.setContentsMargins(0, 0, 0, 0)

        label = QLabel(label_text)
        entry = QLineEdit(self.current_values[key])
        browse_btn = QPushButton("Browse")

        hbox.addWidget(label)
        hbox.addWidget(entry)
        hbox.addWidget(browse_btn)

        self.folder_entries[key] = entry
        browse_btn.clicked.connect(lambda: self.browse_folder(entry))

        layout.addWidget(container)

    def browse_folder(self, entry_widget):
        """Open folder selection dialog."""
        folder = QFileDialog.getExistingDirectory(self, "Select Directory")
        if folder:
            entry_widget.setText(folder)

    def save_config(self):
        """Save configuration to .env file."""
        env_path = os.path.join(os.path.dirname(__file__), '..', '.env')
        
        config = {
            'SOURCE_FOLDER': self.folder_entries['SOURCE_FOLDER'].text(),
            'ORGANIZED_FOLDER': self.folder_entries['ORGANIZED_FOLDER'].text(),
            'UNORGANIZED_FOLDER': self.folder_entries['UNORGANIZED_FOLDER'].text(),
            'DEBUG': str(self.debug_cb.isChecked()),
            'USE_CREATION_DATE': str(self.creation_date_cb.isChecked()),
            'FORCE_DATE': str(self.force_date_cb.isChecked()),
            'DATE_FOLDERS': str(self.date_folders_cb.isChecked()),  # Save new setting
            'LOG_FILE': "logs/file_organizer.log"
        }
        
        for key, value in config.items():
            set_key(env_path, key, value)
        
        self.close()

    def start_sorting(self):
        """Start the file organization process."""
        try:
            config = OrganizerConfig(
                source_folder=self.folder_entries['SOURCE_FOLDER'].text(),
                organized_folder=self.folder_entries['ORGANIZED_FOLDER'].text(),
                unorganized_folder=self.folder_entries['UNORGANIZED_FOLDER'].text(),
                file_types=FILE_TYPES,
                logger=self.logger,
                use_creation_date=self.creation_date_cb.isChecked(),
                force_date=self.force_date_cb.isChecked(),
                date_folders=self.date_folders_cb.isChecked()  # Pass new setting
            )

            # Check if source folder exists
            if not os.path.exists(config.source_folder):
                QMessageBox.warning(self, "Error", f"Source folder not found: {config.source_folder}")
                return

            # Start organization process
            organize_files_by_type(config)
            
            QMessageBox.information(self, "Success", "File organization completed successfully!")
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error during file organization: {str(e)}")

def main():
    """
    Entry point of the GUI application.

    Creates a QApplication instance with the command line arguments,
    initializes the main window (FileOrganizerGUI), shows it, and starts
    the main event loop with exec().
    """
    app = QApplication(sys.argv)
    logger = logging.getLogger(__name__)
    window = FileOrganizerGUI(logger)
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()