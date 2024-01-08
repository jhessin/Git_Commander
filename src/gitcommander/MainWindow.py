import toga

from gitcommander.RepoList import RepoList


class MainWindow(toga.Box):
    def __init__(self, app: toga.App):
        super().__init__()

        self.add(RepoList(app))
