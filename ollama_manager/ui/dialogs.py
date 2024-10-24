from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QLineEdit, 
                           QPushButton, QLabel, QProgressBar)
from ..workers import ModelPullWorker

class PullModelDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Pull New Model")
        self.setModal(True)
        
        layout = QVBoxLayout(self)
        
        # Add input field
        self.model_input = QLineEdit()
        self.model_input.setPlaceholderText("Enter model name (e.g., llama2)")
        layout.addWidget(self.model_input)
        
        # Add progress indicator
        self.progress = QProgressBar()
        self.progress.setVisible(False)
        layout.addWidget(self.progress)
        
        # Add status label
        self.status_label = QLabel()
        layout.addWidget(self.status_label)
        
        # Add buttons
        self.pull_button = QPushButton("Pull Model")
        self.pull_button.clicked.connect(self.pull_model)
        layout.addWidget(self.pull_button)
        
        self.cancel_button = QPushButton("Cancel")
        self.cancel_button.clicked.connect(self.reject)
        layout.addWidget(self.cancel_button)
    
    def pull_model(self):
        model_name = self.model_input.text().strip()
        if not model_name:
            self.status_label.setText("Please enter a model name")
            return
        
        self.progress.setVisible(True)
        self.progress.setRange(0, 0)  # Indeterminate progress
        self.pull_button.setEnabled(False)
        self.status_label.setText("Pulling model...")
        
        self.worker = ModelPullWorker(model_name)
        self.worker.finished.connect(self.handle_pull_complete)
        self.worker.error.connect(self.handle_pull_error)
        self.worker.start()
    
    def handle_pull_complete(self, success):
        self.progress.setVisible(False)
        self.status_label.setText("Model pulled successfully!")
        self.accept()
    
    def handle_pull_error(self, error_message):
        self.progress.setVisible(False)
        self.pull_button.setEnabled(True)
        self.status_label.setText(f"Error: {error_message}")
