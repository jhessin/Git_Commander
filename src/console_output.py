# Python 3
import wx
import sys


# Custom class to redirect console output to a wx.TextCtrl
class ConsoleOutput:
    text_ctrl: wx.TextCtrl

    def __init__(self, text_ctrl: wx.TextCtrl):
        self.text_ctrl = text_ctrl

    def write(self, message: str):
        # Append message to the text control
        wx.CallAfter(self.text_ctrl.AppendText, message)

    def flush(self):
        # Flush is needed for file-like object behavior
        pass

