# This Python file uses the following encoding: utf-8
import logging
import os
import pickle
import subprocess
import sys
from datetime import datetime
from pickle import dump, load

from PyQt6 import uic
from PyQt6.QtCore import QObject, pyqtSignal, QRunnable, pyqtSlot, QThreadPool, Qt
from PyQt6.QtWidgets import (
    QApplication, QMainWindow,
    QPushButton, QListWidget, QMenuBar, QStatusBar, QPlainTextEdit, QFileDialog, QDialog, QDialogButtonBox,
    QListWidgetItem,
)


def resource_path(*relative_path: str) -> os.path:
    """ Get absolute path to resource, works for dev and for PyInstaller """
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, *relative_path)


def data_path(*relative_path: str) -> os.path:
    """
    Get the absolute path of the data file from configuration.
    :param relative_path: The relative path of the data object you want
    :return: The absolute path within the config directory
    """
    base_path = getattr(sys, 'PKG_CONFIG_PATH', os.path.join(os.path.expanduser('~'), '.config', 'GitCommander'))
    os.makedirs(base_path, exist_ok=True)
    return os.path.join(base_path, *relative_path)


PICKLE_FILE = data_path('repos.dat')
REPOS_DIRECTORY = os.path.join(os.path.expanduser('~'), 'repos')


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


def clone(repo_name: str) -> str:
    print(REPOS_DIRECTORY)
    os.makedirs(REPOS_DIRECTORY, exist_ok=True)
    path = os.path.join(REPOS_DIRECTORY, repo_name.split('/')[-1])
    print(f'cloning repo {repo_name} to {path}')
    subprocess.run(['gh', 'repo', 'clone', repo_name, path])
    return path


def push_repo(path: str):
    print(f"committing and pushing {path}")
    date = datetime.now()
    subprocess.run(['git', 'add', '.'], cwd=path)
    subprocess.run(['git', 'commit', f'-m "{date}"'], cwd=path)
    subprocess.run(['git', 'push'], cwd=path)


def pull_repo(path: str):
    print(f"pulling {path}")
    subprocess.run(['git', 'pull'], cwd=path)


class RepoSearch(QRunnable):
    """
    Search for repos asynchronously and return them when we are done.
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


class RepoSelector(QDialog):
    buttonBox: QDialogButtonBox
    repoList: QListWidget

    def __init__(self):
        super().__init__()
        uic.loadUi(resource_path('ui', 'RepoSelector.ui'), self)
        self.result: str = ''
        repo_list: list[str] = subprocess.run(
            ['gh', 'repo', 'list'],
            capture_output=True,
            encoding='utf-8').stdout.splitlines()
        for repo in repo_list:
            result: str = ''
            for char in repo:
                if char == '\t':
                    break
                else:
                    result += char
            self.add_to_repo_list(result)
        self.repoList.currentItemChanged.connect(self.selection_changed)

    def add_to_repo_list(self, item: str):
        if len(self.repoList.findItems(item, Qt.MatchFlag.MatchExactly)) == 0:
            self.repoList.addItem(item)

    def selection_changed(self, new_selection: QListWidgetItem):
        self.result = new_selection.text()

    def accept(self):
        if self.result == '':
            return False
        else:
            super().accept()


class MainWindow(QMainWindow):
    pullAllButton: QPushButton
    pullRepoButton: QPushButton
    pushAllButton: QPushButton
    pushRepoButton: QPushButton

    addRepo: QPushButton
    rmRepo: QPushButton
    cloneRepoButton: QPushButton

    repoList: QListWidget
    searchButton: QPushButton

    menubar: QMenuBar
    statusbar: QStatusBar

    def __init__(self):
        super().__init__()

        uic.loadUi(resource_path('ui', 'MainWindow.ui'), self)

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
        self.cloneRepoButton.clicked.connect(self.clone_repo)

    def search_for_repos(self):
        worker = RepoSearch()
        worker.signals.result.connect(self.add_to_repo_list)
        self.threadpool.start(worker)

    def clone_repo(self):
        # TODO: show repo window and clone and add repo to repos directory.
        dialog = RepoSelector()
        result = dialog.exec()
        if result:
            path = clone(dialog.result)
            self.add_to_repo_list(path)

    def add_to_repo_list(self, item: str):
        if len(self.repoList.findItems(item, Qt.MatchFlag.MatchExactly)) == 0:
            self.repoList.addItem(item)
            save_repos(self.repoList)

    def manual_repo_add(self):
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
