import os
from pprint import pprint

import toga
from tinydb import TinyDB

from gitcommander.models.repo_list import RepoList, Repo

REPO_FILE_NAME = 'repos.dat'


class RepoListTable(toga.Table):
    """
    A RepoList displays the users list of repos.
    """
    repos: RepoList

    def __init__(self, app: toga.App):
        super().__init__(headings=['Path'], accessors=['path'], multiple_select=True)
        os.makedirs(app.paths.data, exist_ok=True)
        db_path = os.path.join(app.paths.data, REPO_FILE_NAME)
        self.repos = RepoList(db=TinyDB(db_path))
        self.update_data()

    def update_data(self):
        # self.data = self.repos.db.all()
        self.data = sorted(self.repos.data)
        # pprint(self.repos.data)
        pprint([data['path'] for data in self.repos.db.all()])

    def add_row(self, path: str):
        if not self.repos.has(path):
            # print(f"{path} not found. Adding...")
            self.repos.append(Repo(path=path))
            self.update_data()
        # else:
        # print(f"{path} found. Skipping...")

    def rm_row(self, path: str):
        self.repos.rm(path)
        self.update_data()
