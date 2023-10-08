# This Python file uses the following encoding: utf-8
import logging
import subprocess
import os
import pickle
import sys
from datetime import datetime

from pickle import dump, load
from PyQt6 import uic
from PyQt6.QtCore import QMimeData, QMimeType, QObject, pyqtSignal, QRunnable, pyqtSlot, QThreadPool, Qt
from PyQt6.QtWidgets import (
    QApplication, QMainWindow,
    QPushButton, QListWidget, QListWidgetItem, QMenuBar, QStatusBar, QPlainTextEdit, QFileDialog,
)


def resource_path(relative_path: str):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)


PICKLE_FILE = 'repos.dat'


class QTextEditLogger(logging.Handler, QObject):
    appendPlainText = pyqtSignal(str)

    def __init__(self, parent):
        super().__init__()
        QObject.__init__(self)
        self.widget = QPlainTextEdit(parent)
        self.widget.setReadOnly(True)
        self.appendPlainText.connect(self.widget.appendPlainText)

    def emit(self, record):
        msg = self.format(record)
        self.appendPlainText.emit(msg)


def load_repos() -> list[str]:
    if os.path.exists(PICKLE_FILE):
        with open(PICKLE_FILE, 'rb') as file:
            return load(file)
    else:
        return []


def list_repos(data: QListWidget) -> list[str]:
    items = []
    for i in range(data.count()):
        items.append(data.item(i).text())
    return items


def save_repos(data: QListWidget):
    items = list_repos(data)
    try:
        with open(PICKLE_FILE, 'wb') as file:
            dump(items, file, pickle.HIGHEST_PROTOCOL)
    except Exception as e:
        print(e)
        sys.exit()


def push_repo(path: str):
    print(f"committing and pushing {path}")
    # TODO: commit all and push the repo
    date = datetime.now()
    subprocess.run('git add .', cwd=path)
    subprocess.run(f"git commit -m \"{date}\"", cwd=path)
    subprocess.run('git push', cwd=path)


def pull_repo(path: str):
    print(f"pulling {path}")
    # TODO: pull the given repo
    subprocess.run('git pull', cwd=path)


class RepoSearch(QRunnable):
    """
    Search for repos asyncronously and return them when we are done.
    """

    class Signals(QObject):
        result = pyqtSignal(str)

    signals = Signals()

    @pyqtSlot()
    def run(self):
        home = os.path.expanduser('~')
        repo_list = []
        for root, dirs, files in os.walk(home):
            if '.git' in dirs:
                repo_list.append(root)
                self.signals.result.emit(root)


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

        uic.loadUi(resource_path('MainWindow.ui'), self)

        self.repoList.setSelectionMode(QListWidget.SelectionMode.ExtendedSelection)
        self.repoList.setSortingEnabled(True)

        self.repoList.addItems(load_repos())

        self.threadpool = QThreadPool()

        self.pullAllButton.clicked.connect(self.pull_all)
        self.pullRepoButton.clicked.connect(self.pull_selected)
        self.pushAllButton.clicked.connect(self.push_all)
        self.pushRepoButton.clicked.connect(self.push_selected)
        self.searchButton.clicked.connect(self.search_for_repos)
        self.rmRepo.clicked.connect(self.rm_repo)
        self.addRepo.clicked.connect(self.manual_repo_add)

    def search_for_repos(self):
        worker = RepoSearch()
        worker.signals.result.connect(self.add_to_repo_list)
        self.threadpool.start(worker)

    def add_to_repo_list(self, item: str):
        if len(self.repoList.findItems(item, Qt.MatchFlag.MatchExactly)) == 0:
            self.repoList.addItem(item)
            save_repos(self.repoList)

    def manual_repo_add(self):
        home = os.path.expanduser('~')
        dialog = QFileDialog(self)
        dialog.setFileMode(QFileDialog.FileMode.Directory)
        if dialog.exec():
            directories = dialog.selectedFiles()
            for directory in directories:
                self.add_to_repo_list(os.path.abspath(directory))

    def rm_repo(self):
        for item in self.repoList.selectedItems():
            row = self.repoList.row(item)
            self.repoList.takeItem(row)
        save_repos(self.repoList)

    def push_all(self):
        repos = list_repos(self.repoList)
        for repo in repos:
            push_repo(repo)
        print('Finished Pushing all repos')

    def pull_all(self):
        repos = list_repos(self.repoList)
        for repo in repos:
            pull_repo(repo)
        print('Finished Pulling all repos')

    def push_selected(self):
        repos = self.repoList.selectedItems()
        for repo in repos:
            push_repo(repo.text())
        print('Finished pushing selected repos')

    def pull_selected(self):
        repos = self.repoList.selectedItems()
        for repo in repos:
            pull_repo(repo.text())
        print('Finished pulling selected repos')


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    # ...
    sys.exit(app.exec())
