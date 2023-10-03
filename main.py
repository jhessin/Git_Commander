# This Python file uses the following encoding: utf-8
import os
import sys

from PyQt6 import uic
from PyQt6.QtWidgets import (
    QApplication, QMainWindow,
    QPushButton, QListWidget, QListWidgetItem, QMenuBar, QStatusBar,
)
from PyQt6.QtCore import QModelIndex


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

        self.searchButton.clicked.connect(self.search_for_repos)
        self.repoList.itemClicked.connect(self.repo_selected)

    def search_for_repos(self):
        values = ['one', 'two', 'three']
        for i in values:
            self.repoList.addItem(QListWidgetItem(i))

    def repo_selected(self, item: QListWidgetItem):
        print(item.text())


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    # ...
    sys.exit(app.exec())
