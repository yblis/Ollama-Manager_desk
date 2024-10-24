from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, 
                           QPushButton, QLabel, QMessageBox)
from PyQt6.QtCore import Qt, QTimer
from .model_list import ModelListWidget
from .dialogs import PullModelDialog
from ..workers import ModelListWorker

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Ollama Manager")
        self.setMinimumSize(800, 600)
        
        # Create central widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        
        # Add header
        header = QLabel("Ollama Model Manager")
        header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(header)
        
        # Add model list widget
        self.model_list = ModelListWidget()
        layout.addWidget(self.model_list)
        
        # Add buttons
        button_layout = QVBoxLayout()
        self.pull_button = QPushButton("Pull New Model")
        self.pull_button.clicked.connect(self.show_pull_dialog)
        button_layout.addWidget(self.pull_button)
        
        self.refresh_button = QPushButton("Refresh")
        self.refresh_button.clicked.connect(self.refresh_models)
        button_layout.addWidget(self.refresh_button)
        
        layout.addLayout(button_layout)
        
        # Set up auto-refresh timer
        self.refresh_timer = QTimer()
        self.refresh_timer.timeout.connect(self.refresh_models)
        self.refresh_timer.start(5000)  # Refresh every 5 seconds
        
        # Initial refresh
        self.refresh_models()
    
    def show_pull_dialog(self):
        dialog = PullModelDialog(self)
        dialog.exec()
        self.refresh_models()
    
    def refresh_models(self):
        self.worker = ModelListWorker()
        self.worker.finished.connect(self.update_model_list)
        self.worker.error.connect(self.show_error)
        self.worker.start()
    
    def update_model_list(self, models):
        self.model_list.update_models(models)
    
    def show_error(self, message):
        QMessageBox.critical(self, "Error", message)
