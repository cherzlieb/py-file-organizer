from PySide6.QtWidgets import QWidget, QHBoxLayout, QLabel, QLineEdit, QPushButton, QFileDialog
from PySide6.QtCore import Qt

class FolderEntryWidget(QWidget):
    """Widget for folder path entry with browse button."""
    def __init__(self, label_text: str, initial_value: str = ""):
        super().__init__()
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        self.label = QLabel(label_text)
        self.entry = QLineEdit(initial_value)
        self.browse_btn = QPushButton("Browse")
        
        # Connect browse button
        self.browse_btn.clicked.connect(self.browse_folder)

        layout.addWidget(self.label)
        layout.addWidget(self.entry)
        layout.addWidget(self.browse_btn)
    
    def browse_folder(self):
        """Open folder selection dialog."""
        folder = QFileDialog.getExistingDirectory(self, "Select Directory")
        if folder:
            self.entry.setText(folder)

class LogPathWidget(QWidget):
    """Widget for log file path settings."""
    def __init__(self):
        super().__init__()
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        self.label = QLabel("Log File Location:")
        self.entry = QLineEdit()
        self.browse_btn = QPushButton("Browse")
        
        # Connect browse button
        self.browse_btn.clicked.connect(self.browse_folder)

        layout.addWidget(self.label)
        layout.addWidget(self.entry)
        layout.addWidget(self.browse_btn)
    
    def browse_folder(self):
        """Open folder selection dialog."""
        folder = QFileDialog.getExistingDirectory(self, "Select Directory")
        if folder:
            self.entry.setText(folder)