import wx


class DragSelectList(wx.ListCtrl):
    """My custom list view that has drag selection"""

    def __init__(self, parent):
        super().__init__(parent, wx.ID_ANY, style=wx.LC_HRULES | wx.LC_REPORT | wx.LC_VRULES | wx.LC_SORT_ASCENDING)
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

    def add_item(self, item: str):
        index = self.FindItem(-1, item)
        if index == wx.NOT_FOUND:
            self.InsertItem(self.GetItemCount(), item)

    def to_str_list(self) -> list[str]:
        result = []

        item = self.GetNextItem(-1)
        while item != wx.NOT_FOUND:
            result.append(self.GetItemText(item))

            item = self.GetNextItem(item)

        return result

    def from_str_list(self, str_list: list[str]):
        self.DeleteAllItems()
        for item in str_list:
            self.add_item(item)

    def list_from_sel(self, reset: bool = True) -> list[str]:
        result = []

        item = self.GetFirstSelected(-1)
        while item != wx.NOT_FOUND:
            result.append(self.GetItemText(item))
            item = self.GetNextSelected(item)
            if reset:
                self.Select(item, 0)

        return result
