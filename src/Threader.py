from typing import TYPE_CHECKING, Coroutine, Any, AsyncGenerator

if TYPE_CHECKING:
    from MainFrame import MainFrame

from . import constants as consts
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
                                    *args, **kwargs
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
            if os.path.exists(consts.PICKLE_FILE):
                with open(consts.PICKLE_FILE, "rb") as f:
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
        with open(consts.PICKLE_FILE, "wb") as f:
            dump(repos, f, HIGHEST_PROTOCOL)
        print('repository lists saved')

    def push_repo(self, path: str, force: bool = False):
        """
        Push the given repository to the origin.
        :param force: Forces an overwrite of the repository.
        :param path: The path of the repository to push.
        :return: None
        """
        print(f'Pushing repository {path}')
        date = datetime.now().strftime("%Y%m%d%H%M%S")
        self._run_subprocess(['git', 'add', '.'], cwd=path)
        self._run_subprocess(['git', 'commit', f"-m {date}"], cwd=path)
        self.run_subprocess(["git", "push", "-f"] if force else ["git", "push"], cwd=path)

    def pull_repo(self, path: str):
        """
        Pull the given repository from the origin.
        :param path: The path of the repository to pull.
        :return: None
        """
        print(f'Pulling repository {path}')
        self.run_subprocess(["git", "pull"], cwd=path)

    @staticmethod
    async def _repo_search() -> AsyncGenerator[str, None]:
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

    @staticmethod
    def get_gh_repos() -> list[tuple[str, str]]:
        import json

        command = ['gh', 'repo', 'list', '--json', 'name', '--json', 'description']
        result = subprocess.run(command, capture_output=True, text=True)
        json_output = result.stdout.strip()

        try:
            result = []
            data = json.loads(json_output)
            for repo in data:
                result.append((repo['name'], repo['description']))
            return result
        except json.decoder.JSONDecodeError as e:
            return [('gh was not installed or not logged in', str(e))]

    def clone_repo(self, repo_url: str, target_dir: str = consts.REPOS_DIRECTORY) -> str:
        f"""
        Clones the given repo using the git command
        :param repo_url: The url of the repo to clone.
        :param target_dir: The directory to clone the repo to defaults to ${consts.REPOS_DIRECTORY}
        :return: The directory the repo was cloned to.
        """
        os.makedirs(target_dir, exist_ok=True)
        path = os.path.join(target_dir, repo_url.split("/")[-1])
        print(f"cloning repo {repo_url} to {path}")
        self.run_subprocess(["git", "clone", repo_url, path])
        return path

    def clone_with_gh(self, repo_name: str, target_dir: str = consts.REPOS_DIRECTORY) -> str:
        f"""
        Clones the given repo using the GitHub cli
        :param repo_name: The name of the repo from GitHub
        :param target_dir: The directory to clone the repo to defaults to ${consts.REPOS_DIRECTORY}
        :return: The directory the repo was cloned to.
        """
        # print(consts.REPOS_DIRECTORY)
        os.makedirs(target_dir, exist_ok=True)
        path = os.path.join(target_dir, repo_name.split("/")[-1])
        print(f"cloning repo {repo_name} to {path}")
        # self._run_subprocess(["gh", "repo", "clone", repo_name, path], check=True)
        self.run_subprocess(["gh", "repo", "clone", repo_name, path])
        return path
