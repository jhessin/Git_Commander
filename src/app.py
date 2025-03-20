"""
A manager for multiple git repositories across different computers.
"""

import wx
from Frames import Main


def main():
    app = wx.App(True)
    frame = Main(None, "Small editor")
    app.MainLoop()


def test():
    print('Test successful!')
