"""
This will handle the display and upkeep of the list of repositories.
"""

import wx
from Models.repo_list import RepoList



class RepoListView(wx.ListBox):

    data: RepoList = RepoList()

    def __init__(self, *args, **kwargs):
        super(RepoListView, self).__init__(*args, **kwargs)
