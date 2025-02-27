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

        # Create checkbox container
        checkbox_container = QWidget()
        checkbox_layout = QHBoxLayout(checkbox_container)
        checkbox_layout.setContentsMargins(0, 0, 0, 0)

        # Create checkboxes
        self.debug_cb = QCheckBox("Debug Mode")
        self.creation_date_cb = QCheckBox("Use Creation Date")
        self.force_date_cb = QCheckBox("Force Date")
        self.date_folders_cb = QCheckBox("Add Date to Folders")

        # Add checkboxes to horizontal layout
        checkbox_layout.addWidget(self.debug_cb)
        checkbox_layout.addWidget(self.creation_date_cb)
        checkbox_layout.addWidget(self.force_date_cb)
        checkbox_layout.addWidget(self.date_folders_cb)

        # Set checkbox states
        self.debug_cb.setChecked(self.current_values['DEBUG'].lower() == 'true')
        self.creation_date_cb.setChecked(self.current_values['USE_CREATION_DATE'].lower() == 'true')
        self.force_date_cb.setChecked(self.current_values['FORCE_DATE'].lower() == 'true')
        self.date_folders_cb.setChecked(self.current_values.get('DATE_FOLDERS', 'False').lower() == 'true')

        # Add checkbox container to main layout
        main_layout.addWidget(checkbox_container)

        # Create and add log container (after checkbox container)
        self.log_container = QWidget()
        log_layout = QHBoxLayout(self.log_container)
        log_layout.setContentsMargins(0, 0, 0, 0)

        log_label = QLabel("Log File Location:")
        self.log_path_entry = QLineEdit()
        log_browse_btn = QPushButton("Browse")
        
        log_layout.addWidget(log_label)
        log_layout.addWidget(self.log_path_entry)
        log_layout.addWidget(log_browse_btn)
        
        # Hide log path widgets initially
        self.log_container.setVisible(False)
        
        # Connect debug checkbox to show/hide log path widgets
        self.debug_cb.stateChanged.connect(self.toggle_log_path)
        log_browse_btn.clicked.connect(self.browse_log_folder)
        
        # Add widgets to main layout
        main_layout.addWidget(self.log_container)  # Add log path widgets after debug checkbox

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

    def toggle_log_path(self, state):
        """Show or hide log path widgets based on debug checkbox state."""
        self.log_container.setVisible(state == Qt.CheckState.Checked.value)

    def browse_log_folder(self):
        """Open folder selection dialog for log file location."""
        folder = QFileDialog.getExistingDirectory(self, "Select Log Directory")
        if folder:
            self.log_path_entry.setText(folder)

    def save_config(self):
        """
        Save the current values of the folder entries and checkboxes to the .env file and close the dialog.
        """        
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
        """
        Start the file organization process.

        This method is called when the user clicks the "Start" button. It sets up
        logging if the debug checkbox is enabled, and then starts the organization
        process using the provided configuration.

        If the source folder does not exist, a warning message is shown and the
        process is canceled.

        If any errors occur during the organization process, a critical error
        message is shown with the error details.
        """
        try:
            # Setup logging if debug is enabled
            if self.debug_cb.isChecked():
                log_folder = self.log_path_entry.text()
                if not log_folder:
                    QMessageBox.warning(self, "Warning", "Please select a log file location")
                    return
                    
                log_file = os.path.join(log_folder, 'file_organizer.log')
                os.makedirs(os.path.dirname(log_file), exist_ok=True)
                
                # Configure logging
                file_handler = logging.FileHandler(log_file, encoding='utf-8')
                console_handler = logging.StreamHandler(sys.stdout)
                
                self.logger.handlers = []
                self.logger.addHandler(file_handler)
                self.logger.addHandler(console_handler)
                self.logger.setLevel(logging.DEBUG)
            else:
                self.logger.handlers = []
                self.logger.addHandler(logging.NullHandler())
                self.logger.setLevel(logging.WARNING)

            config = OrganizerConfig(
                source_folder=self.folder_entries['SOURCE_FOLDER'].text(),
                organized_folder=self.folder_entries['ORGANIZED_FOLDER'].text(),
                unorganized_folder=self.folder_entries['UNORGANIZED_FOLDER'].text(),
                file_types=FILE_TYPES,
                logger=self.logger,
                use_creation_date=self.creation_date_cb.isChecked(),
                force_date=self.force_date_cb.isChecked(),
                date_folders=self.date_folders_cb.isChecked()
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