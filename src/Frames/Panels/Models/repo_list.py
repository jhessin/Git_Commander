"""
This is the model for the RepoList.
It will handle holding and sorting the full list of repositories that we will be managing.
"""


class Repo(object):
    _name: str
    _url: str


class RepoList(list[Repo]):
    pass