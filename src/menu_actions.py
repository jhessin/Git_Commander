import asyncio
from typing import TYPE_CHECKING

import wx

if TYPE_CHECKING:
    from MainFrame import MainFrame


async def _save(frame: MainFrame):
    await asyncio.sleep(1)
    await frame.threader.save_repos((frame.list_all_repos.to_str_list(), frame.list_working_repos.to_str_list()))
    wx.CallAfter(frame.finished)


async def _load(frame: MainFrame):
    await asyncio.sleep(1)
    try:
        all_repos, working_repos = await frame.threader.load_repos()
    except TypeError:
        all_repos, working_repos = [], []
    frame.list_all_repos.from_str_list(all_repos)
    frame.list_working_repos.from_str_list(working_repos)
    wx.CallAfter(frame.finished)
    wx.CallAfter(frame.on_selection_changed)


async def _final_save(frame: MainFrame):
    await _save(frame)
    wx.CallAfter(frame.Close, True)


def save_task(frame: MainFrame):
    frame.SetStatusText("Saving...")
    frame.threader.run_async_task(_save(frame))


def load_task(frame: MainFrame):
    frame.SetStatusText("Loading...")
    frame.threader.run_async_task(_load(frame))


def final_save_task(frame: MainFrame):
    frame.SetStatusText("Saving before quitting...")
    frame.threader.run_async_task(_final_save(frame))
