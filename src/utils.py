import asyncio
from typing import Coroutine, Any
from typing import TYPE_CHECKING

import wx

if TYPE_CHECKING:
    from MyFrame import MyFrame


def run_async_task(coroutine: Coroutine[Any, Any, None]):
    loop = asyncio.get_event_loop()
    asyncio.ensure_future(coroutine, loop=loop)


def add_item_to_list(list_ctrl: wx.ListCtrl, repo_name: str):
    index = list_ctrl.FindItem(-1, repo_name)
    if index == wx.NOT_FOUND:
        list_ctrl.InsertItem(list_ctrl.GetItemCount(), repo_name)


def ctrl_to_str(list_ctrl: wx.ListCtrl) -> list[str]:
    result = []

    item = list_ctrl.GetNextItem(-1)
    while item != wx.NOT_FOUND:
        result.append(list_ctrl.GetItemText(item))

        item = list_ctrl.GetNextItem(item)

    return result


def str_to_ctrl(item_list: list[str], list_ctrl: wx.ListCtrl):
    list_ctrl.DeleteAllItems()
    for item in item_list:
        add_item_to_list(list_ctrl, item)


def finished(frame: MyFrame):
    frame.SetStatusText("Done - Ready.")
