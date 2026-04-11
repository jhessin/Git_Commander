import wx


class DragSelectList(wx.ListCtrl):
    """My custom list view that has drag selection"""

    def __init__(self, parent):
        super().__init__(parent, wx.ID_ANY, style=wx.LC_HRULES | wx.LC_REPORT | wx.LC_VRULES)
        self.Bind(wx.EVT_LEFT_DOWN, self.on_left_down)
        self.Bind(wx.EVT_MOTION, self.on_mouse_drag)
        self.start_item = None

    def on_left_down(self, event):
        self.start_item, _ = self.HitTest(event.GetPosition())
        event.Skip()

    def on_mouse_drag(self, event):
        if event.Dragging() and self.start_item is not None:
            current_item, _ = self.HitTest(event.GetPosition())
            if current_item != -1:
                self.Select(current_item)
        event.Skip()
