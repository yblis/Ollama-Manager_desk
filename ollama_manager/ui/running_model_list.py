from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QTableWidget, 
                           QTableWidgetItem, QPushButton, QMessageBox)
from PyQt6.QtCore import Qt
from ..models import RunningInstance
from ..workers import RunningModelStopWorker

class RunningModelListWidget(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        
        # Create table
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels([
            "Model Name", "Instance ID", "Start Time", "Actions"
        ])
        layout.addWidget(self.table)
        
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
    
    def update_running_models(self, instances):
        self.table.setRowCount(0)
        for instance_data in instances:
            instance = RunningInstance.from_dict(instance_data)
            row = self.table.rowCount()
            self.table.insertRow(row)
            
            # Add instance information
            self.table.setItem(row, 0, QTableWidgetItem(instance.model_name))
            self.table.setItem(row, 1, QTableWidgetItem(instance.instance_id))
            self.table.setItem(row, 2, QTableWidgetItem(
                instance.started.strftime("%Y-%m-%d %H:%M:%S")
            ))
            
            # Add stop button
            stop_button = QPushButton("Stop")
            stop_button.clicked.connect(
                lambda checked, i=instance.instance_id: self.stop_instance(i)
            )
            self.table.setCellWidget(row, 3, stop_button)
        
        self.table.resizeColumnsToContents()
    
    def stop_instance(self, instance_id):
        reply = QMessageBox.question(
            self,
            "Confirm Stop",
            f"Are you sure you want to stop instance {instance_id}?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            worker = RunningModelStopWorker(instance_id)
            worker.finished.connect(lambda: self.handle_stop_complete(instance_id))
            worker.error.connect(self.show_error)
            worker.start()
    
    def handle_stop_complete(self, instance_id):
        QMessageBox.information(
            self,
            "Success",
            f"Instance {instance_id} has been stopped."
        )
    
    def show_error(self, message):
        QMessageBox.critical(self, "Error", message)