import os.path
import asyncio

import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW
from toga.widgets.button import OnPressHandler

from gitcommander.actions import push_repo, pull_repo
from gitcommander.views.repo_list_table import RepoListTable

WAIT_OBJECT = '...'


class MainWindow(toga.Box):
    search_for_repos: OnPressHandler
    rm_repo: OnPressHandler

    push_repo: OnPressHandler
    pull_repo: OnPressHandler
    push_all: OnPressHandler
    pull_all: OnPressHandler

    def __init__(self, app: toga.App):
        super().__init__(style=Pack(direction=COLUMN))

        button_width = Pack(width=100)

        # First create the overall structure
        top_box = toga.Box(style=Pack(direction=ROW, flex=9))
        bottom_button_box = toga.Box(style=Pack(direction=ROW, height=50))

        # top_box items
        self.table = RepoListTable(app, style=Pack(flex=5))
        right_button_box = toga.Box(style=Pack(direction=COLUMN, width=250))

        # right_top_box
        pull_repo_btn = toga.Button('Pull', on_press=self.pull_repo, style=button_width)
        pull_all_btn = toga.Button('Pull All', on_press=self.pull_all, style=button_width)
        right_button_box_top = toga.Box(style=Pack(direction=ROW))
        right_button_box_top.add(pull_repo_btn, pull_all_btn)

        # right bottom box
        push_repo_btn = toga.Button('Push', on_press=self.push_repo, style=button_width)
        push_all_btn = toga.Button('Push All', on_press=self.push_all, style=button_width)
        right_button_box_bottom = toga.Box(style=Pack(direction=ROW))
        right_button_box_bottom.add(push_repo_btn, push_all_btn)

        # right box
        right_button_box.add(right_button_box_top, right_button_box_bottom)

        # bottom_button items
        add_button = toga.Button('Search for Repos', on_press=self.search_for_repos)
        rm_button = toga.Button('-', on_press=self.rm_repo)

        # Finally add all the components together
        top_box.add(self.table, right_button_box)

        bottom_button_box.add(add_button, rm_button)

        self.statusLabel = toga.Label('Ready.')

        self.add(top_box, bottom_button_box, self.statusLabel)

    async def search_for_repos(self, btn: toga.Button):
        home = os.path.expanduser('~')
        repo_list = []
        for root, dirs, _ in os.walk(home):
            if '.git' in dirs:
                repo_list.append(root)
                self.table.add_row(path=root)
        self.table.update_data()

    async def rm_repo(self, btn: toga.Button):
        if not self.table.selection:
            return
        for row in self.table.selection:
            self.table.rm_row(row.path)

    async def push_repo(self, btn: toga.Button):
        if not self.table.selection:
            return
        self.statusLabel.text = 'Working...'
        for row in self.table.selection:
            await asyncio.sleep(1)
            await push_repo(row.path)
            await asyncio.sleep(1)
        self.statusLabel.text = 'Ready.'

    async def push_all(self, btn: toga.Button):
        self.statusLabel.text = 'Working...'
        for row in self.table.data:
            await asyncio.sleep(1)
            await push_repo(row.path)
            await asyncio.sleep(1)
        self.statusLabel.text = 'Ready.'

    async def pull_repo(self, btn: toga.Button):
        if not self.table.selection:
            return
        self.statusLabel.text = 'Working...'
        for row in self.table.selection:
            await asyncio.sleep(1)
            await pull_repo(row.path)
            await asyncio.sleep(1)
        self.statusLabel.text = 'Ready.'

    async def pull_all(self, btn: toga.Button):
        self.statusLabel.text = 'Working...'
        for row in self.table.data:
            await asyncio.sleep(1)
            await pull_repo(row.path)
            await asyncio.sleep(1)
        self.statusLabel.text = 'Ready.'
