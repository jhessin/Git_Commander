"""
This will handle the display and upkeep of the list of repositories.
"""

import wx


class RepoListView(wx.ListBox):

    def __init__(self, *args, **kwargs):
        super(RepoListView, self).__init__(*args, **kwargs)
