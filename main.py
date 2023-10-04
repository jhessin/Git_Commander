# This Python file uses the following encoding: utf-8
import mimetypes
import os
import pickle
import sys

from pickle import dump, load
from PyQt6 import uic
from PyQt6.QtCore import QMimeData, QMimeType
from PyQt6.QtWidgets import (
    QApplication, QMainWindow,
    QPushButton, QListWidget, QListWidgetItem, QMenuBar, QStatusBar,
)

PICKLE_FILE = 'repos.dat'


def load_repos() -> list[str]:
    if os.path.exists(PICKLE_FILE):
        with open(PICKLE_FILE, 'rb') as file:
            return load(file)
    else:
        return []


def save_repos(data: QListWidget):
    items = []
    for i in range(data.count()):
        items.append(data.item(i).text())
    try:
        with open(PICKLE_FILE, 'wb') as file:
            dump(items, file, pickle.HIGHEST_PROTOCOL)
    except Exception as e:
        print(e)
        sys.exit()


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

        self.repoList.addItems(load_repos())

        self.searchButton.clicked.connect(self.search_for_repos)
        self.rmRepo.clicked.connect(self.rm_repo)

    def search_for_repos(self):
        home = os.path.expanduser('~')
        for root, dirs, files in os.walk(home):
            if '.git' in dirs:
                self.repoList.addItem(root)
        save_repos(self.repoList)

    def rm_repo(self):
        for item in self.repoList.selectedItems():
            row = self.repoList.row(item)
            self.repoList.takeItem(row)
        save_repos(self.repoList)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    # ...
    sys.exit(app.exec())
