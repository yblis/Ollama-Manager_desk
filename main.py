import sys
import os
from PyQt6.QtWidgets import QApplication, QMessageBox
from ollama_manager.ui.main_window import MainWindow

def main():
    # Set Qt to use the minimal platform plugin
    os.environ['QT_QPA_PLATFORM'] = 'minimal'
    
    app = QApplication(sys.argv)
    app.setApplicationName("Ollama Manager")
    app.setStyle('Fusion')  # Modern look across platforms
    
    # Suppress platform plugin warnings
    def message_handler(mode, context, message):
        if "propagateSizeHints" not in message:
            print(f"{mode}: {message}")
    
    app.messageHandler = message_handler
    
    try:
        window = MainWindow()
        window.show()
        return app.exec()
    except Exception as e:
        QMessageBox.critical(None, "Error", f"Failed to start application: {str(e)}")
        return 1

if __name__ == "__main__":
    sys.exit(main())
