import wx


class ExampleFrame(wx.Frame):
    def __init__(self, parent, *args, **kw):
        wx.Frame.__init__(self, parent, *args, **kw)

        panel = wx.Panel(self)

        self.quote = wx.StaticText(panel, label="Your quote: ", pos=(20, 30))
        clearButton = wx.Button(self, wx.ID_CLEAR)

        self.Show()

    # end constructor


# end class
