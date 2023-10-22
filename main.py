# This Python file uses the following encoding: utf-8
"""
Git Commander

GitCommander is a basic gui for handling multiple git repositories.
"""
import os
import pickle
import subprocess
import sys
from datetime import datetime
from pickle import dump, load

from PyQt6 import uic, QtCore, QtWidgets


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
    base_path = getattr(sys, 'PKG_CONFIG_PATH',
                        os.path.join(os.path.expanduser('~'), '.config'))
    base_path = os.path.join(base_path, 'GitCommander')
    os.makedirs(base_path, exist_ok=True)
    return os.path.join(base_path, *relative_path)


PICKLE_FILE = data_path('repos.dat')
REPOS_DIRECTORY = os.path.join(os.path.expanduser('~'), 'repos')


def load_repos() -> list[str]:
    """
    Load the repos from the pickle file.
    :return: a list of directories that hold repos.
    """
    if os.path.exists(PICKLE_FILE):
        with open(PICKLE_FILE, 'rb') as file:
            return load(file)
    else:
        return []


def list_repos(data: QtWidgets.QListWidget) -> list[str]:
    """
    Get the list of repos from the provided QListWidget.
    :param data: A QListWidget that holds strings.
    :return: a list of strings
    """
    items = []
    for i in range(data.count()):
        items.append(data.item(i).text())
    return items


def save_repos(data: QtWidgets.QListWidget):
    """
    Save the repos from a QListWidget
    :param data: The QListWidget to get data from
    :return: None
    """
    items = list_repos(data)
    with open(PICKLE_FILE, 'wb') as file:
        dump(items, file, pickle.HIGHEST_PROTOCOL)


def clone(repo_name: str) -> str:
    """
    Clones the given repo using the GitHub cli
    :param repo_name: The name of the repo from GitHub
    :return: The directory the repo was cloned to.
    """
    print(REPOS_DIRECTORY)
    os.makedirs(REPOS_DIRECTORY, exist_ok=True)
    path = os.path.join(REPOS_DIRECTORY, repo_name.split('/')[-1])
    print(f'cloning repo {repo_name} to {path}')
    subprocess.run(['gh', 'repo', 'clone', repo_name, path], check=True)
    return path


def push_repo(path: str):
    """
    Push the given repo.
    :param path: The path to a repo.
    :return: None
    """
    print(f"committing and pushing {path}")
    date = datetime.now()
    subprocess.run(['git', 'add', '.'], cwd=path, check=False)
    subprocess.run(['git', 'commit', f'-m "{date}"'], cwd=path, check=False)
    subprocess.run(['git', 'push'], cwd=path, check=False)


def pull_repo(path: str):
    """
    Pull a given repo from GitHub
    :param path: The path to the repo
    :return: None
    """
    print(f"pulling {path}")
    subprocess.run(['git', 'pull'], cwd=path, check=False)


class RepoSearch(QtCore.QRunnable):
    """
    Search for repos asynchronously and return them when we are done.
    """

    class Signals(QtCore.QObject):
        """
        Simple signals to send in Qt
        """
        result = QtCore.pyqtSignal(str)

    signals = Signals()

    @QtCore.pyqtSlot()
    def run(self):
        """
        Run the search for repos
        :return:
        """
        home = os.path.expanduser('~')
        repo_list = []
        for root, dirs, _ in os.walk(home):
            if '.git' in dirs:
                repo_list.append(root)
                self.signals.result.emit(root)

    def stub(self):
        """
        This is only here to make pylint behave.
        Evidently you can't have a class with only a single public method.
        :return: None
        """


class RepoSelector(QtWidgets.QDialog):
    """
    A popup dialog box to help select a repo to clone.
    Uses the GitHub cli to generate a list of repos.
    """
    buttonBox: QtWidgets.QDialogButtonBox
    repoList: QtWidgets.QListWidget

    def __init__(self):
        super().__init__()
        uic.loadUi(resource_path('ui', 'RepoSelector.ui'), self)
        self.result: str = ''
        repo_list: list[str] = subprocess.run(
            ['gh', 'repo', 'list'],
            capture_output=True,
            check=True,
            encoding='utf-8').stdout.splitlines()
        for repo in repo_list:
            result: str = ''
            for char in repo:
                if char == '\t':
                    break
                result += char
            self.add_to_repo_list(result)
        self.repoList.currentItemChanged.connect(self.selection_changed)

    def add_to_repo_list(self, item: str):
        """
        Add a given item to the repo list if it isn't already there.
        :param item: The item to add.
        :return: None
        """
        if len(self.repoList.findItems(item, QtCore.Qt.MatchFlag.MatchExactly)) == 0:
            self.repoList.addItem(item)

    def selection_changed(self, new_selection: QtWidgets.QListWidgetItem):
        """
        Saves the selected item as the result.
        :param new_selection: The item just selected
        :return: None
        """
        self.result = new_selection.text()

    def accept(self):
        """
        Tests to see if the result has been selected before accepting it.
        :return: None
        """
        if self.result == '':
            return
        super().accept()


class MainWindow(QtWidgets.QMainWindow):
    """
    The Main Window of the program.
    """
    pullAllButton: QtWidgets.QPushButton
    pullRepoButton: QtWidgets.QPushButton
    pushAllButton: QtWidgets.QPushButton
    pushRepoButton: QtWidgets.QPushButton

    addRepo: QtWidgets.QPushButton
    rmRepo: QtWidgets.QPushButton
    cloneRepoButton: QtWidgets.QPushButton

    repoList: QtWidgets.QListWidget
    searchButton: QtWidgets.QPushButton

    menubar: QtWidgets.QMenuBar
    statusbar: QtWidgets.QStatusBar

    def __init__(self):
        super().__init__()

        uic.loadUi(resource_path('ui', 'MainWindow.ui'), self)

        self.repoList.setSelectionMode(QtWidgets.QListWidget.SelectionMode.ExtendedSelection)
        self.repoList.setSortingEnabled(True)

        self.repoList.addItems(load_repos())

        self.threadpool = QtCore.QThreadPool()

        self.pullAllButton.clicked.connect(self.pull_all)
        self.pullRepoButton.clicked.connect(self.pull_selected)
        self.pushAllButton.clicked.connect(self.push_all)
        self.pushRepoButton.clicked.connect(self.push_selected)
        self.searchButton.clicked.connect(self.search_for_repos)
        self.rmRepo.clicked.connect(self.rm_repo)
        self.addRepo.clicked.connect(self.manual_repo_add)
        self.cloneRepoButton.clicked.connect(self.clone_repo)

    def search_for_repos(self):
        """
        Search for repos in the users home folder and adds them to the listview
        :return: None
        """
        worker = RepoSearch()
        worker.signals.result.connect(self.add_to_repo_list)
        self.threadpool.start(worker)

    def clone_repo(self):
        """
        Presents a dialog to select a repo to clone and add to the repo list
        :return: None
        """
        dialog = RepoSelector()
        result = dialog.exec()
        if result:
            path = clone(dialog.result)
            self.add_to_repo_list(path)

    def add_to_repo_list(self, item: str):
        """
        Add the given repo to the repo list if it isn't already there.
        :param item: The repo to add.
        :return: None
        """
        if len(self.repoList.findItems(item, QtCore.Qt.MatchFlag.MatchExactly)) == 0:
            self.repoList.addItem(item)
            save_repos(self.repoList)

    def manual_repo_add(self):
        """
        Presents a dialog to add a repo manually
        :return: None
        """
        dialog = QtWidgets.QFileDialog(self)
        dialog.setFileMode(QtWidgets.QFileDialog.FileMode.Directory)
        if dialog.exec():
            directories = dialog.selectedFiles()
            for directory in directories:
                self.add_to_repo_list(os.path.abspath(directory))

    def rm_repo(self):
        """
        Removes the selected repo(s)
        :return: None
        """
        for item in self.repoList.selectedItems():
            row = self.repoList.row(item)
            self.repoList.takeItem(row)
        save_repos(self.repoList)

    def push_all(self):
        """
        Push all the repos!
        :return: None
        """
        repos = list_repos(self.repoList)
        for repo in repos:
            push_repo(repo)
        print('Finished Pushing all repos')

    def pull_all(self):
        """
        Pull all the repos!
        :return: None
        """
        repos = list_repos(self.repoList)
        for repo in repos:
            pull_repo(repo)
        print('Finished Pulling all repos')

    def push_selected(self):
        """
        Push the selected repos.
        :return: None
        """
        repos = self.repoList.selectedItems()
        for repo in repos:
            push_repo(repo.text())
        print('Finished pushing selected repos')

    def pull_selected(self):
        """
        Pull the selected repos.
        :return: None
        """
        repos = self.repoList.selectedItems()
        for repo in repos:
            pull_repo(repo.text())
        print('Finished pulling selected repos')


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    # ...
    sys.exit(app.exec())
