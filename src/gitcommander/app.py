"""
A manager for multiple git repositories across different computers.
"""

import wx
from ExampleFrame import ExampleFrame as Frame
from ExamplePanel import ExamplePanel as Panel


def main():
    """The Main application logic"""
    app = wx.App(False)
    frame = Frame(None, title="Demo with Notebook")
    nb = wx.Notebook(frame)

    nb.AddPage(Panel(nb), "Absolute Positioning")
    nb.AddPage(Panel(nb), "Page Two")
    nb.AddPage(Panel(nb), "Page Three")
    frame.Show()
    app.MainLoop()

# end main
