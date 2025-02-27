from PySide6.QtWidgets import QWidget, QHBoxLayout, QLabel, QLineEdit, QPushButton, QFileDialog
from PySide6.QtCore import Qt

class FolderEntryWidget(QWidget):
    """Widget for folder path entry with browse button."""
    def __init__(self, label_text: str, initial_value: str = ""):
        super().__init__()
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(10)  # Abstand zwischen den Elementen

        # Create widgets with fixed sizes
        self.label = QLabel(label_text)
        self.label.setFixedWidth(150)
        self.label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        
        self.entry = QLineEdit(initial_value)
        self.entry.setFixedWidth(400)  # Feste statt Minimum-Breite
        
        self.browse_btn = QPushButton("Browse")
        self.browse_btn.setFixedWidth(80)
        
        # Connect browse button
        self.browse_btn.clicked.connect(self.browse_folder)

        # Add widgets to layout
        layout.addWidget(self.label)
        layout.addWidget(self.entry)
        layout.addWidget(self.browse_btn)
        
        # Set fixed size for the whole widget
        self.setFixedHeight(35)  # Einheitliche Höhe
        self.setMinimumWidth(650)  # Minimale Gesamtbreite
    
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
        layout.setSpacing(10)

        # Create widgets with fixed sizes
        self.label = QLabel("Log File Location:")
        self.label.setFixedWidth(150)
        self.label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        
        self.entry = QLineEdit()
        self.entry.setFixedWidth(400)
        
        self.browse_btn = QPushButton("Browse")
        self.browse_btn.setFixedWidth(80)
        
        # Connect browse button
        self.browse_btn.clicked.connect(self.browse_folder)

        # Add widgets to layout
        layout.addWidget(self.label)
        layout.addWidget(self.entry)
        layout.addWidget(self.browse_btn)
        
        # Set fixed size for the whole widget
        self.setFixedHeight(35)
        self.setMinimumWidth(650)
    
    def browse_folder(self):
        """Open folder selection dialog."""
        folder = QFileDialog.getExistingDirectory(self, "Select Directory")
        if folder:
            self.entry.setText(folder)