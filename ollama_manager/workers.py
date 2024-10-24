from PyQt6.QtCore import QThread, pyqtSignal
from .api import OllamaAPI

class ModelListWorker(QThread):
    finished = pyqtSignal(list)
    error = pyqtSignal(str)
    
    def run(self):
        try:
            models = OllamaAPI.list_models()
            self.finished.emit(models)
        except Exception as e:
            self.error.emit(str(e))

class ModelPullWorker(QThread):
    finished = pyqtSignal(bool)
    error = pyqtSignal(str)
    progress = pyqtSignal(str)
    
    def __init__(self, model_name: str):
        super().__init__()
        self.model_name = model_name
    
    def run(self):
        try:
            success = OllamaAPI.pull_model(self.model_name)
            self.finished.emit(success)
        except Exception as e:
            self.error.emit(str(e))

class ModelDeleteWorker(QThread):
    finished = pyqtSignal(bool)
    error = pyqtSignal(str)
    
    def __init__(self, model_name: str):
        super().__init__()
        self.model_name = model_name
    
    def run(self):
        try:
            success = OllamaAPI.delete_model(self.model_name)
            self.finished.emit(success)
        except Exception as e:
            self.error.emit(str(e))
