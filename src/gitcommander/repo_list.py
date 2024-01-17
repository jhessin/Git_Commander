"""
A basic wrapper for a DetailList view.
"""
import os

import toga
from tinydb import TinyDB
from gitcommander.repo_list_source import RepoListSource

REPO_FILE_NAME = 'repos.dat'
REPO_TABLE_NAME = 'repos'


class RepoList(toga.DetailedList):
    """
    A RepoList displays the users list of repos.
    """
    db_path: os.PathLike

    def __init__(self, app: toga.App):
        super().__init__(accessors=('', 'name', 'path'), data=RepoListSource(app))
        os.makedirs(app.paths.data, exist_ok=True)
        self.db = TinyDB(os.path.join(app.paths.data, REPO_FILE_NAME))
        self.data = self.db.table(REPO_TABLE_NAME)
