"""
A repo_list_source that is a front end to a TinyDB that holds all the users repos.
"""
import os

import toga
from toga.sources import ListSource
from tinydb import TinyDB

REPO_FILE_NAME = 'repos.dat'
REPO_TABLE_NAME = 'repos'


class RepoListSource(ListSource):
    """
    A RepoListSource is a source that can be used to hold the users git repositories. It is a front end for a TinyDB.
    """
    db: TinyDB

    def __init__(self, app: toga.App):
        super().__init__(accessors=["name", 'path'])
        os.makedirs(app.paths.data, exist_ok=True)
        self.db = TinyDB(os.path.join(app.paths.data, REPO_FILE_NAME))
        self.data = self.db.table(REPO_TABLE_NAME)
