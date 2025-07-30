from PySide6.QtWidgets import (
    QApplication, QMainWindow
)
import sys
import os
from model.load_models import load_all_models
from pipeline.manager.base import AutomaticTranslationBase

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Main Window")
        self.setMinimumSize(800, 600)

        sb, tc, ocr = load_all_models()

        self.ye = AutomaticTranslationBase(sb, tc, ocr)

        folder_path = "out"

        file_paths = [
            os.path.join(folder_path, f)
            for f in os.listdir(folder_path)
            if os.path.isfile(os.path.join(folder_path, f)) and f.lower().endswith(('.png', '.jpg', '.jpeg'))
        ]

        self.ye.receive_selected_files.emit(file_paths)


    

def main():
    app = QApplication(sys.argv)

    main_window = MainWindow()
    main_window.show()

    sys.exit(app.exec())
 

if __name__ == "__main__":
    main()  
    