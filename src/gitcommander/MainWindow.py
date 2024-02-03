import os.path

import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW
from toga.widgets.button import OnPressHandler

from gitcommander.views.repo_list_table import RepoListTable


class MainWindow(toga.Box):
    search_for_repos: OnPressHandler
    rm_repo: OnPressHandler

    def __init__(self, app: toga.App):
        super().__init__(style=Pack(direction=COLUMN))
        # TODO: Add all components to the main window here.
        self.table = RepoListTable(app)
        self.add_button = toga.Button('Search for Repos', on_press=self.search_for_repos)
        self.rm_button = toga.Button('-', on_press=self.rm_repo)

        self.add(self.table)
        self.add(self.add_button)
        self.add(self.rm_button)

    async def search_for_repos(self, btn: toga.Button):
        home = os.path.expanduser('~')
        repo_list = []
        for root, dirs, _ in os.walk(home):
            if '.git' in dirs:
                # print(f"Found repo {root}!")
                repo_list.append(root)
                self.table.add_row(path=root)
        self.table.update_data()
        print('Finished searching for repos')

    async def rm_repo(self, btn: toga.Button):
        if not self.table.selection:
            return
