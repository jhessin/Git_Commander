import asyncio
from typing import TYPE_CHECKING

import wx

import actions
import utils

if TYPE_CHECKING:
    from MainFrame import MainFrame


async def save(frame: MainFrame):
    await asyncio.sleep(1)
    await actions.save_repos((utils.ctrl_to_str(frame.list_all_repos), utils.ctrl_to_str(frame.list_working_repos)))
    wx.CallAfter(utils.finished, frame)


async def load(frame: MainFrame):
    await asyncio.sleep(1)
    all_repos, working_repos = await actions.load_repos()
    utils.str_to_ctrl(all_repos, frame.list_all_repos)
    utils.str_to_ctrl(working_repos, frame.list_working_repos)
    wx.CallAfter(utils.finished, frame)


async def final_save(frame: MainFrame):
    await save(frame)
    wx.CallAfter(frame.Close, True)


def save_task(frame: MainFrame):
    frame.SetStatusText("Saving...")
    utils.run_async_task(save(frame))


def load_task(frame: MainFrame):
    frame.SetStatusText("Loading...")
    utils.run_async_task(load(frame))


def final_save_task(frame: MainFrame):
    frame.SetStatusText("Saving before quitting...")
    utils.run_async_task(final_save(frame))
