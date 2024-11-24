"""
A manager for multiple git repositories across different computers.
"""

import wx
from gitcommander.Main_Window import Main_Window

def main():
    """ The Main application logic """
    app = wx.App(True)
    Main_Window(None, "Small editor")
    app.MainLoop()
# end main
