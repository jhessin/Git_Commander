"""
A basic wrapper for a DetailList view.
"""
import os

from pydantic import BaseModel, ConfigDict, PositiveInt
from tinydb import TinyDB, Query


class Repo(BaseModel):
    """
    This is the data model for a repo. It simply holds the path.
    """
    path: str


class RepoList(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    db: TinyDB

    @property
    def data(self) -> list[str]:
        # return [Repo(**data, id=data.doc_id) for data in self.db.all()]
        return [data['path'] for data in self.db.all()]

    def append(self, repo: Repo):
        self.db.insert(repo.__dict__)

    def has(self, path: str):
        return self.db.contains(Query().path == path)

    def rm(self, path: str):
        self.db.remove(Query().path == path)
