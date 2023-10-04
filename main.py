# This Python file uses the following encoding: utf-8
import os
import sys

from PyQt6 import uic
from PyQt6.QtWidgets import (
    QApplication, QMainWindow,
    QPushButton, QListWidget, QListWidgetItem, QMenuBar, QStatusBar,
)


class MainWindow(QMainWindow):
    pullAllButton: QPushButton
    pullRepoButton: QPushButton
    pushAllButton: QPushButton
    pushRepoButton: QPushButton

    addRepo: QPushButton
    rmRepo: QPushButton

    repoList: QListWidget
    searchButton: QPushButton

    menubar: QMenuBar
    statusbar: QStatusBar

    def __init__(self):
        super().__init__()

        uic.loadUi('MainWindow.ui', self)

        self.repoList.setSelectionMode(QListWidget.SelectionMode.ExtendedSelection)

        self.searchButton.clicked.connect(self.search_for_repos)
        self.rmRepo.clicked.connect(self.rm_repo)

    def search_for_repos(self):
        home = os.path.expanduser('~')
        for root, dirs, files in os.walk(home):
            if '.git' in dirs:
                self.repoList.addItem(root)

    def rm_repo(self):
        for item in self.repoList.selectedItems():
            row = self.repoList.row(item)
            self.repoList.takeItem(row)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    # ...
    sys.exit(app.exec())
