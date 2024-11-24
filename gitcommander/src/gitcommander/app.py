"""
A manager for multiple git repositories across different computers.
"""

import wx
from gitcommander.ExampleFrame import ExampleFrame as Frame


def main():
    """The Main application logic"""
    app = wx.App(True)
    Frame(None)
    app.MainLoop()


# end main
