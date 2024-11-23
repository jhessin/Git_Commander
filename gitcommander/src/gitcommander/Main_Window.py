import os
import wx


class Main_Window(wx.Frame):

    control: wx.TextCtrl

    def __init__(self, parent, title, *args, **kw):
        super().__init__(parent, title=title, size=(200, 100), *args, **kw)
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
        self.Show(True)

        # Set events
        self.Bind(wx.EVT_MENU, self.OnAbout, menuAbout)
        self.Bind(wx.EVT_MENU, self.OnExit, menuExit)
        self.Bind(wx.EVT_MENU, self.OnOpen, menuOpen)

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
