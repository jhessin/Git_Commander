"""
A manager for multiple git repositories across different computers.
"""

import wx
from gitcommander.Main_Window import Main_Window


def main():
    app = wx.App(True)
    frame = Main_Window(None, "Small editor")
    app.MainLoop()
