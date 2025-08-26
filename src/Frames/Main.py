import os
import wx

from src.Panels.repo_list_view import RepoListView


class Main(wx.Frame):
    filename: str
    dir_name: str
    left_list: RepoListView
    right_list: RepoListView

    def __init__(self, parent, title, *args, **kw):
        super().__init__(parent, title=title, size=(200, -1), *args, **kw)

        # Creating a text control for entering data.
        # self.control = wx.TextCtrl(self, style=wx.TE_MULTILINE)

        self.CreateStatusBar()  # A Statusbar in the bottom of the window

        # Setting up the list views
        self.left_list = RepoListView(self)
        self.right_list = RepoListView(self)

        # Setting up the menu.
        # file_menu = wx.Menu()
        # wx.ID_ABOUT and wx.ID_EXIT are standard IDs provided by wxWidgets.
        # menu_open = file_menu.Append(wx.ID_OPEN, "&Open", "Open a file for editing")
        # menu_about = file_menu.Append(
        #     wx.ID_ABOUT, "&About", "Information about this program"
        # )
        # file_menu.AppendSeparator()
        # menu_exit = file_menu.Append(wx.ID_EXIT, "E&xit", "Terminate the program")

        # Creating the menubar
        # menu_bar = wx.MenuBar()
        # menu_bar.Append(file_menu, "&File")  # Adding the filemenu to the menubar
        # self.SetMenuBar(menu_bar)  # Adding the MenuBar to the Frame content.

        # Set events
        # self.Bind(wx.EVT_MENU, self.on_about, menu_about)
        # self.Bind(wx.EVT_MENU, self.on_exit, menu_exit)
        # self.Bind(wx.EVT_MENU, self.on_open, menu_open)

        # Set up sizers
        self.horizontal_sizer: wx.BoxSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.horizontal_sizer.Add(self.left_list, 1, wx.EXPAND)
        self.horizontal_sizer.Add(self.right_list, 1, wx.EXPAND)

        # self.buttons = []
        # for i in range(0, 6):
        #     self.buttons.append(wx.Button(self, -1, f"Button &{str(i)}"))
        #     self.horizontal_sizer.Add(self.buttons[i], 1, wx.EXPAND)

        self.vertical_sizer: wx.BoxSizer = wx.BoxSizer(wx.VERTICAL)
        self.vertical_sizer.Add(self.horizontal_sizer, 0, wx.EXPAND)

        # layout sizers
        self.SetSizer(self.vertical_sizer)
        self.SetAutoLayout(1)
        self.vertical_sizer.Fit(self)

        # Show the window
        self.Show(True)

    def on_open(self, e: wx.Event):
        """Open a file"""
        self.dir_name = ""
        dlg = wx.FileDialog(self, "Choose a file", self.dir_name, "", "*.*", wx.FD_OPEN)
        if dlg.ShowModal() == wx.ID_OK:
            self.filename = dlg.GetFilename()
            self.dir_name = dlg.GetDirectory()
            f = open(os.path.join(self.dir_name, self.filename), "r")
            self.control.SetValue(f.read())
            f.close()
        dlg.Destroy()

    def on_about(self, event: wx.Event):
        # A message dialog box with an OK button. wx.OK is a standard ID in wxWidgets
        dlg = wx.MessageDialog(
            self, "A small text editor", "About Sample Editor", wx.OK
        )
        dlg.ShowModal()  # Show it
        dlg.Destroy()  # finally destroy it when finished

    def on_exit(self, event: wx.Event):
        self.Close(True)
