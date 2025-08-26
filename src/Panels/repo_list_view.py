"""
This will handle the display and upkeep of the list of repositories.
"""

import wx
import wx.adv
from src.Models.repo_list import RepoList


class RepoListView(wx.adv.EditableListBox):
    selected_item: str
    data: RepoList = RepoList()

    def __init__(self, parent, label='Repos', *args, **kwargs):
        super(RepoListView, self).__init__(parent, *args, label=label,
                                           style=wx.adv.EL_ALLOW_NEW | wx.adv.EL_ALLOW_EDIT | wx.adv.EL_ALLOW_DELETE,
                                           **kwargs)

        self.Bind(wx.EVT_LISTBOX, self.on_item_selected)

    def on_item_selected(self, event: wx.ListEvent):
        self.selected_item = self.GetStrings()[event.GetSelection()]
