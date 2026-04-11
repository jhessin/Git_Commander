import asyncio
from typing import TYPE_CHECKING

import wx

import actions
import utils

if TYPE_CHECKING:
    from MyFrame import MyFrame


async def save(frame: MyFrame):
    await asyncio.sleep(1)
    await actions.save_repos(utils.ctrl_to_str(frame.list_all_repos))
    wx.CallAfter(utils.finished, frame)


async def load(frame: MyFrame):
    await asyncio.sleep(1)
    utils.str_to_ctrl(await actions.load_repos(), frame.list_all_repos)
    wx.CallAfter(utils.finished, frame)


async def final_save(frame: MyFrame):
    await save(frame)
    wx.CallAfter(frame.Close, True)


def save_task(frame: MyFrame):
    frame.SetStatusText("Saving...")
    utils.run_async_task(save(frame))


def load_task(frame: MyFrame):
    frame.SetStatusText("Loading...")
    utils.run_async_task(load(frame))


def final_save_task(frame: MyFrame):
    frame.SetStatusText("Saving before quitting...")
    utils.run_async_task(final_save(frame))
