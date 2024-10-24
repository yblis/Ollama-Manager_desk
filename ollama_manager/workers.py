from PyQt6.QtCore import QThread, pyqtSignal, QObject, QTimer, pyqtSlot
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

class RunningModelListWorker(QThread):
    finished = pyqtSignal(list)
    error = pyqtSignal(str)
    
    def run(self):
        try:
            instances = OllamaAPI.list_running()
            self.finished.emit(instances)
        except Exception as e:
            self.error.emit(str(e))

class RunningModelStopWorker(QThread):
    finished = pyqtSignal(bool)
    error = pyqtSignal(str)
    
    def __init__(self, instance_id: str):
        super().__init__()
        self.instance_id = instance_id
        self.should_stop = False
    
    def run(self):
        try:
            success = OllamaAPI.stop_instance(self.instance_id)
            if not self.should_stop:
                self.finished.emit(success)
        except Exception as e:
            if not self.should_stop:
                self.error.emit(str(e))
    
    def stop(self):
        self.should_stop = True
        self.wait()

class BackgroundWorker(QObject):
    error = pyqtSignal(str)
    models_updated = pyqtSignal(list)
    running_updated = pyqtSignal(list)

    def __init__(self):
        super().__init__()
        self._timer = None
        self._thread = QThread()
        self.moveToThread(self._thread)
        self._thread.started.connect(self.start_timer)
        self._thread.finished.connect(self._thread.deleteLater)

    def start(self):
        self._thread.start()

    def stop(self):
        if self._timer:
            self._timer.stop()
        self._thread.quit()
        self._thread.wait()

    @pyqtSlot()
    def start_timer(self):
        self._timer = QTimer()
        self._timer.setInterval(30000)  # 30 seconds
        self._timer.timeout.connect(self.refresh)
        self._timer.start()

    @pyqtSlot()
    def refresh(self):
        try:
            models = OllamaAPI.list_models()
            self.models_updated.emit(models)
            running = OllamaAPI.list_running()
            self.running_updated.emit(running)
        except Exception as e:
            self.error.emit(str(e))
