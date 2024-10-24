from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QTableWidget, 
                           QTableWidgetItem, QPushButton, QMessageBox)
from PyQt6.QtCore import Qt
from ..models import OllamaModel
from ..workers import ModelDeleteWorker

class ModelListWidget(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        
        # Create table
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels([
            "Name", "Size", "Modified", "Status", "Actions"
        ])
        layout.addWidget(self.table)
        
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
    
    def update_models(self, models):
        self.table.setRowCount(0)
        for model_data in models:
            model = OllamaModel.from_dict(model_data)
            row = self.table.rowCount()
            self.table.insertRow(row)
            
            # Add model information
            self.table.setItem(row, 0, QTableWidgetItem(model.name))
            self.table.setItem(row, 1, QTableWidgetItem(f"{model.size / 1024 / 1024:.1f} MB"))
            self.table.setItem(row, 2, QTableWidgetItem(
                model.modified.strftime("%Y-%m-%d %H:%M")
            ))
            self.table.setItem(row, 3, QTableWidgetItem("Installed"))
            
            # Add delete button
            delete_button = QPushButton("Delete")
            delete_button.clicked.connect(
                lambda checked, m=model.name: self.delete_model(m)
            )
            self.table.setCellWidget(row, 4, delete_button)
        
        self.table.resizeColumnsToContents()
    
    def delete_model(self, model_name):
        reply = QMessageBox.question(
            self,
            "Confirm Deletion",
            f"Are you sure you want to delete {model_name}?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            worker = ModelDeleteWorker(model_name)
            worker.finished.connect(lambda: self.handle_delete_complete(model_name))
            worker.error.connect(self.show_error)
            worker.start()
    
    def handle_delete_complete(self, model_name):
        QMessageBox.information(
            self,
            "Success",
            f"Model {model_name} has been deleted."
        )
    
    def show_error(self, message):
        QMessageBox.critical(self, "Error", message)
