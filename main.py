import sys
import os
from PyQt6.QtWidgets import QApplication
from ollama_manager.ui.main_window import MainWindow

def main():
    # Set Qt to use the minimal platform plugin
    os.environ['QT_QPA_PLATFORM'] = 'minimal'
    
    app = QApplication(sys.argv)
    app.setApplicationName("Ollama Manager")
    app.setStyle('Fusion')  # Modern look across platforms
    
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
