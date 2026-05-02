import asyncio
from asyncio import Queue
from typing import TYPE_CHECKING

import wx

from . import actions
from .DragSelectList import DragSelectList

if TYPE_CHECKING:
    from MainFrame import MainFrame


async def _scan_for_repos(frame: MainFrame, queue: Queue):

    async for value in actions.repo_search():
        msg = await queue.get()
        if msg == "STOP":
            break
        frame.list_all_repos.add_item(value)

    wx.CallAfter(frame.finished_scanning)


def scan_task(frame: MainFrame):
    if frame.is_scanning:
        frame.queue.put_nowait("STOP")
        frame.is_scanning = False
    else:
        frame.is_scanning = True
        frame.btn_scan_for_repos.SetLabel("Stop Scanning")
        frame.SetStatusText("Scanning...")
        frame.threader.run_async_task(_scan_for_repos(frame, frame.queue))


def copy_repos(src: DragSelectList, target: DragSelectList):
    item = src.GetNextItem(-1)

    while item != wx.NOT_FOUND:
        item_name = src.GetItemText(item)

        target.add_item(item_name)
        item = src.GetNextItem(item)
        # src.Select(item, 0 )

        item = src.GetNextItem(item)


def copy_selection(src: DragSelectList, target: DragSelectList):
    item = src.GetFirstSelected(-1)

    while src.GetSelectedItemCount() > 0:
        if item != -1:
            item_name = src.GetItemText(item)

            target.add_item(item_name)

            src.Select(item, 0)
        item = src.GetNextSelected(item)


def move_selection(src: DragSelectList, target: DragSelectList):
    item = src.GetFirstSelected(-1)

    while src.GetSelectedItemCount() > 0:
        if item != -1:
            item_name = src.GetItemText(item)

            target.add_item(item_name)
            src.DeleteItem(item)

        item = src.GetNextSelected(item)


def remove_selection(src: wx.ListCtrl):
    item = src.GetFirstSelected(-1)

    while src.GetSelectedItemCount() > 0:
        if item != -1:
            src.DeleteItem(item)

        item = src.GetNextSelected(item)


def move_repos(src: DragSelectList, target: DragSelectList):
    item = src.GetNextItem(-1)

    while src.GetItemCount() > 0:
        if item != wx.NOT_FOUND:
            item_name = src.GetItemText(item)
            # print(item_name)

            target.add_item(item_name)
            src.DeleteItem(item)

        item = src.GetNextItem(item)
