from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, 
                           QPushButton, QLabel, QMessageBox, QSplitter)
from PyQt6.QtCore import Qt, QTimer
from .model_list import ModelListWidget
from .running_model_list import RunningModelListWidget
from .dialogs import PullModelDialog
from ..workers import ModelListWorker, RunningModelListWorker

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
        
        # Create splitter for model lists
        splitter = QSplitter(Qt.Orientation.Vertical)
        
        # Add model list widget
        model_list_container = QWidget()
        model_list_layout = QVBoxLayout(model_list_container)
        model_list_label = QLabel("Installed Models")
        model_list_layout.addWidget(model_list_label)
        self.model_list = ModelListWidget()
        model_list_layout.addWidget(self.model_list)
        splitter.addWidget(model_list_container)
        
        # Add running models list widget
        running_list_container = QWidget()
        running_list_layout = QVBoxLayout(running_list_container)
        running_list_label = QLabel("Running Models")
        running_list_layout.addWidget(running_list_label)
        self.running_list = RunningModelListWidget()
        running_list_layout.addWidget(self.running_list)
        splitter.addWidget(running_list_container)
        
        layout.addWidget(splitter)
        
        # Add buttons
        button_layout = QVBoxLayout()
        self.pull_button = QPushButton("Pull New Model")
        self.pull_button.clicked.connect(self.show_pull_dialog)
        button_layout.addWidget(self.pull_button)
        
        self.refresh_button = QPushButton("Refresh")
        self.refresh_button.clicked.connect(self.refresh_all)
        button_layout.addWidget(self.refresh_button)
        
        layout.addLayout(button_layout)
        
        # Set up auto-refresh timer
        self.refresh_timer = QTimer()
        self.refresh_timer.timeout.connect(self.refresh_all)
        self.refresh_timer.start(5000)  # Refresh every 5 seconds
        
        # Initial refresh
        self.refresh_all()
    
    def show_pull_dialog(self):
        dialog = PullModelDialog(self)
        dialog.exec()
        self.refresh_all()
    
    def refresh_all(self):
        self.refresh_models()
        self.refresh_running_models()
    
    def refresh_models(self):
        self.model_worker = ModelListWorker()
        self.model_worker.finished.connect(self.update_model_list)
        self.model_worker.error.connect(self.show_error)
        self.model_worker.start()
    
    def refresh_running_models(self):
        self.running_worker = RunningModelListWorker()
        self.running_worker.finished.connect(self.update_running_list)
        self.running_worker.error.connect(self.show_error)
        self.running_worker.start()
    
    def update_model_list(self, models):
        self.model_list.update_models(models)
    
    def update_running_list(self, instances):
        self.running_list.update_running_models(instances)
    
    def show_error(self, message):
        QMessageBox.critical(self, "Error", message)
