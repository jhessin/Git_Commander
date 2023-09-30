# This Python file uses the following encoding: utf-8
import sys
from PyQt6.QtWidgets import QApplication
from PyQt6 import uic


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = uic.loadUi("MainWindow.ui")
    window.show()
    # ...
    sys.exit(app.exec())
