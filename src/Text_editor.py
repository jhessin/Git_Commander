import wx


class Text_editor(wx.Frame):
    """We simply derive a new class of Frame."""

    def __init__(self, parent, title, *args, **kw):
        super().__init__(parent, title=title, size=(200, 100), *args, **kw)
        self.control = wx.TextCtrl(self, style=wx.TE_MULTILINE)
        self.Show(True)
