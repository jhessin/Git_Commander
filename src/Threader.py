from typing import TYPE_CHECKING, Coroutine, Any, AsyncGenerator

if TYPE_CHECKING:
    from MainFrame import MainFrame

from constants import Consts
import asyncio
import os
import subprocess
import threading
import wx
from datetime import datetime
from pickle import dump, load, HIGHEST_PROTOCOL


class Threader:
    frame: MainFrame
    queue: asyncio.Queue[str] = asyncio.Queue()

    def __init__(self, frame: MainFrame):
        self.frame = frame

    @staticmethod
    def run_async_task(coroutine: Coroutine[Any, Any, None]):
        loop = asyncio.get_event_loop()
        asyncio.ensure_future(coroutine, loop=loop)

    def _run_subprocess(self, cmd: list[str], *args, **kwargs):
        try:
            result = subprocess.run(cmd,
                                    capture_output=True,
                                    text=True,
                                    check=True, *args, **kwargs
                                    )
            wx.CallAfter(self.frame.log_window.AppendText, result.stdout)
            wx.CallAfter(self.frame.finished)
        except subprocess.CalledProcessError as e:
            wx.CallAfter(self.frame.log_window.AppendText, e.stderr)

    def run_subprocess(self, cmd: list[str], *args, **kwargs):
        thread = threading.Thread(target=self._run_subprocess, args=[cmd, *args], kwargs=kwargs)
        thread.daemon = True
        thread.start()

    @staticmethod
    async def load_repos() -> tuple[list[Any], list[Any]] | None | Any:
        """
        Load the repositories from the pickle file
        :return: a tuple of two directory lists, first the list of all repositories
            then a list containing working repositories.
        """
        try:
            if os.path.exists(Consts.PICKLE_FILE):
                with open(Consts.PICKLE_FILE, "rb") as f:
                    return load(f)
        except FileNotFoundError:
            return [], []

    @staticmethod
    async def save_repos(repos: tuple[list[str], list[str]]) -> None:
        """
        Save the repositories to the pickle file
        :param repos: A tuple of two directory lists, first the list of all repositories
            then a list containing working repositories.
        :return: None
        """
        with open(Consts.PICKLE_FILE, "wb") as f:
            dump(repos, f, HIGHEST_PROTOCOL)

    def push_repo(self, path: str):
        """
        Push the given repository to the origin.
        :param path: The path of the repository to push.
        :return: None
        """
        date = datetime.now().strftime("%Y%m%d%H%M%S")
        subprocess.run(['git', 'add', '.'], cwd=path)
        subprocess.run(['git', 'commit', f"-m {date}"], cwd=path)
        self.run_subprocess(["git", "push"])

    def pull_repo(self, path: str):
        """
        Pull the given repository from the origin.
        :param path: The path of the repository to pull.
        :return: None
        """
        self.run_subprocess(["git", "pull"], cwd=path)

    @staticmethod
    async def _repo_search() -> AsyncGenerator[tuple[str, str], None]:
        """Scans the users home folder for repositories."""
        home = os.path.expanduser("~")
        repo_list = []
        print('Searching for repositories in ' + home)
        for root, dirs, files in os.walk(home):
            await asyncio.sleep(0.001)
            if '.git' in dirs:
                repo_list.append(root)
                yield root
        if len(repo_list) > 1:
            print(f"Found {len(repo_list)} repositories")
        elif len(repo_list) == 1:
            print(f"Found {len(repo_list)} repositories")
        else:
            print(f"Found no repositories")

    @staticmethod
    def reset_repo(path: str, force: bool = False):
        print(f"Resetting repository {path}")
        cmd = ["git", "reset", "--hard"] if force else ["git", "reset"]
        subprocess.run(cmd, cwd=path)

    async def _scan_for_repos(self):
        """
        Manages the _repo_search method so that it can be canceled.
        :return: None
        """
        async for value in self._repo_search():
            msg = await self.queue.get()
            if msg == 'STOP':
                break
            self.frame.list_all_repos.add_item(value)

        wx.CallAfter(self.frame.finished_scanning)

    def scan_task(self):
        if self.frame.is_scanning:
            self.frame.queue.put_nowait('STOP')
            self.frame.is_scanning = False
        else:
            self.frame.is_scanning = True
            self.frame.btn_scan_for_repos.SetLabel("Stop scanning")
            self.frame.SetStatusText("Scanning...")
            self.run_async_task(self._scan_for_repos())

    def clone(self, repo_name: str) -> str:
        """
        Clones the given repo using the GitHub cli
        :param repo_name: The name of the repo from GitHub
        :return: The directory the repo was cloned to.
        """
        print(Consts.REPOS_DIRECTORY)
        os.makedirs(Consts.REPOS_DIRECTORY, exist_ok=True)
        path = os.path.join(Consts.REPOS_DIRECTORY, repo_name.split("/")[-1])
        print(f"cloning repo {repo_name} to {path}")
        # subprocess.run(["gh", "repo", "clone", repo_name, path], check=True)
        self.run_subprocess(["gh", "repo", "clone", repo_name, path])
        return path
