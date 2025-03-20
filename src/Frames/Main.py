import os
import wx


class Main(wx.Frame):
    control: wx.TextCtrl

    def __init__(self, parent, title, *args, **kw):
        super().__init__(parent, title=title, size=(200, -1), *args, **kw)
        self.control = wx.TextCtrl(self, style=wx.TE_MULTILINE)
        self.CreateStatusBar()  # A Statusbar in the bottom of the window

        # Setting up the menu.
        filemenu = wx.Menu()
        # wx.ID_ABOUT and wx.ID_EXIT are standard IDs provided by wxWidgets.
        menuOpen = filemenu.Append(wx.ID_OPEN, "&Open", "Open a file for editing")
        menuAbout = filemenu.Append(
            wx.ID_ABOUT, "&About", "Information about this program"
        )
        filemenu.AppendSeparator()
        menuExit = filemenu.Append(wx.ID_EXIT, "E&xit", "Terminate the program")

        # Creating the menubar
        menuBar = wx.MenuBar()
        menuBar.Append(filemenu, "&File")  # Adding the filemenu to the menubar
        self.SetMenuBar(menuBar)  # Adding the MenuBar to the Frame content.

        # Set events
        self.Bind(wx.EVT_MENU, self.OnAbout, menuAbout)
        self.Bind(wx.EVT_MENU, self.OnExit, menuExit)
        self.Bind(wx.EVT_MENU, self.OnOpen, menuOpen)

        # Set up sizers
        self.horizontalSizer: wx.BoxSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.buttons = []
        for i in range(0, 6):
            self.buttons.append(wx.Button(self, -1, f"Button &{str(i)}"))
            self.horizontalSizer.Add(self.buttons[i], 1, wx.EXPAND)

        self.verticalSizer: wx.BoxSizer = wx.BoxSizer(wx.VERTICAL)
        self.verticalSizer.Add(self.control, 1, wx.EXPAND)
        self.verticalSizer.Add(self.horizontalSizer, 0, wx.EXPAND)

        # layout sizers
        self.SetSizer(self.verticalSizer)
        self.SetAutoLayout(1)
        self.verticalSizer.Fit(self)

        # Show the window
        self.Show(True)

    def OnOpen(self, e: wx.Event):
        """Open a file"""
        self.dirname = ""
        dlg = wx.FileDialog(self, "Choose a file", self.dirname, "", "*.*", wx.FD_OPEN)
        if dlg.ShowModal() == wx.ID_OK:
            self.filename = dlg.GetFilename()
            self.dirname = dlg.GetDirectory()
            f = open(os.path.join(self.dirname, self.filename), "r")
            self.control.SetValue(f.read())
            f.close()
        dlg.Destroy()

    def OnAbout(self, event: wx.Event):
        # A message dialog box with an OK button. wx.OK is a standard ID in wxWidgets
        dlg = wx.MessageDialog(
            self, "A small text editor", "About Sample Editor", wx.OK
        )
        dlg.ShowModal()  # Show it
        dlg.Destroy()  # finally destroy it when finished

    def OnExit(self, event: wx.Event):
        self.Close(True)
