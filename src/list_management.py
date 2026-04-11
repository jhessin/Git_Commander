from typing import TYPE_CHECKING

import wx

import actions
import utils

if TYPE_CHECKING:
    from MyFrame import MyFrame


async def _scan_for_repos(frame: MyFrame):
    frame.SetStatusText("Scanning...")

    async for value in actions.repo_search():
        utils.add_item_to_list(frame.list_all_repos, value)

    frame.SetStatusText("Done. - Ready.")


def scan_task(frame: MyFrame):
    utils.run_async_task(_scan_for_repos(frame))


def copy_repos(src: wx.ListCtrl, target: wx.ListCtrl):
    item = src.GetNextItem(-1)

    while item != wx.NOT_FOUND:
        item_name = src.GetItemText(item)

        utils.add_item_to_list(target, item_name)
        # src.Select(item, 0 )

        item = src.GetNextItem(item)


def copy_selection(src: wx.ListCtrl, target: wx.ListCtrl):
    item = src.GetFirstSelected(-1)

    while src.GetSelectedItemCount() > 0:
        if item != -1:
            item_name = src.GetItemText(item)

            utils.add_item_to_list(target, item_name)
            src.Select(item, 0)
        item = src.GetNextSelected(item)


def move_selection(src: wx.ListCtrl, target: wx.ListCtrl):
    item = src.GetFirstSelected(-1)

    while src.GetSelectedItemCount() > 0:
        if item != -1:
            item_name = src.GetItemText(item)

            utils.add_item_to_list(target, item_name)
            src.DeleteItem(item)

        item = src.GetNextSelected(item)


def remove_selection(src: wx.ListCtrl):
    item = src.GetFirstSelected(-1)

    while src.GetSelectedItemCount() > 0:
        if item != -1:
            src.DeleteItem(item)

        item = src.GetNextSelected(item)


def move_repos(src: wx.ListCtrl, target: wx.ListCtrl):
    item = src.GetNextItem(-1)

    while src.GetItemCount() > 0:
        if item != wx.NOT_FOUND:
            item_name = src.GetItemText(item)
            # print(item_name)

            utils.add_item_to_list(target, item_name)
            src.DeleteItem(item)

        item = src.GetNextItem(item)
