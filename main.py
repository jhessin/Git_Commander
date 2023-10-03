# This Python file uses the following encoding: utf-8
import sys
from PyQt6.QtWidgets import QApplication, QMainWindow
from PyQt6 import uic
from pyqtgraph import PlotWidget


class MainWindow(QMainWindow):
    graphWidget: PlotWidget

    def __init__(self):
        super().__init__()

        uic.loadUi('MainWindow.ui', self)

        self.plot([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], [30, 32, 34, 32, 33, 31, 29, 32, 35, 45])

    def plot(self, hour, temperature):
        self.graphWidget.plot(hour, temperature)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    # ...
    sys.exit(app.exec())
