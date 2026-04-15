import asyncio
import os
import subprocess
import sys
import threading
from datetime import datetime
from pickle import dump, load, HIGHEST_PROTOCOL
from typing import Any, AsyncGenerator

import wx

import utils
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from MyFrame import MyFrame


def _run_subprocess(cmd: list[str], *args, **kwargs):
    try:
        result = subprocess.run(cmd,
                                capture_output=True,
                                text=True,
                                check=True, *args, **kwargs
                                )
        frame: MyFrame | None = utils.Main_Frame
        if frame:
            wx.CallAfter(frame.log_window.AppendText, result.stdout)
        else:
            wx.CallAfter(print, result.stdout)
        wx.CallAfter(utils.finished)
    except subprocess.CalledProcessError as e:
        wx.CallAfter(print, e.stderr)


def run_subprocess(cmd: list[str], *args, **kwargs):
    thread = threading.Thread(target=_run_subprocess, args=[cmd, *args], kwargs = kwargs)
    thread.daemon = True
    thread.start()

def data_path(*relative_path: str) -> str:
    """
    Get the absolute path of the data file from configuration.
    :param relative_path: The relative path of the data object you want
    :return: The absolute path within the config directory
    """
    base_path = getattr(
        sys, "PKG_CONFIG_PATH", os.path.join(os.path.expanduser("~"), ".config")
    )
    base_path = os.path.join(base_path, "GitCommander")
    os.makedirs(base_path, exist_ok=True)
    return os.path.join(base_path, *relative_path)

PICKLE_FILE = data_path("repos.dat")
REPOS_DIRECTORY = os.path.join(os.path.expanduser("~"), "repos")

async def load_repos() -> list[str]:
    """
    Load the repos from the pickle file.
    :return: a list of directories (str) that hold repos.
    """
    # TODO Load the working list as well.
    if os.path.exists(PICKLE_FILE):
        with open(PICKLE_FILE, "rb") as file:
            return load(file)
    else:
        return []

async def save_repos(data: list[str]):
    # TODO Save the working list as well.
    with open(PICKLE_FILE, 'wb') as file:
        dump(data, file, HIGHEST_PROTOCOL)

def clone(repo_name: str) -> str:
    """
    Clones the given repo using the GitHub cli
    :param repo_name: The name of the repo from GitHub
    :return: The directory the repo was cloned to.
    """
    print(REPOS_DIRECTORY)
    os.makedirs(REPOS_DIRECTORY, exist_ok=True)
    path = os.path.join(REPOS_DIRECTORY, repo_name.split("/")[-1])
    print(f"cloning repo {repo_name} to {path}")
    # subprocess.run(["gh", "repo", "clone", repo_name, path], check=True)
    run_subprocess(["gh", "repo", "clone", repo_name, path])
    return path

def push_repo(path: str):
    """
    Push the given repo.
    :param path: The path to a repo.
    :return: None
    """
    print(f"committing and pushing {path}")
    date = datetime.now()
    # run_subprocess(["git", "add", "."], cwd=path, check=False)
    subprocess.run(["git", "add", "."], cwd=path)
    subprocess.run(["git", "commit", f'-m "{date}"'], cwd=path)
    run_subprocess(["git", "push"], cwd=path)
    # subprocess.run(["git", "push"], cwd=path, check=False)

def pull_repo(path: str):
    """
    Pull a given repo from GitHub
    :param path: The path to the repo
    :return: None
    """
    print(f"pulling {path}")
    # subprocess.run(["git", "pull"], cwd=path, check=False)
    run_subprocess(["git", "pull"], cwd=path)

def is_valid_repo(path: str) -> bool:
    """
    Validate the given repo. To see if it is a valid git repository.
    :param path: The path to the repo
    :return: True if the repo is valid, False otherwise
    """
    return os.path.exists(path) and '.git' in os.listdir(path)

async def repo_search() -> AsyncGenerator[str, Any]:
    home = os.path.expanduser('~')
    repo_list = []
    print('Searching for repos...')
    for root, dirs, _ in os.walk(home):
        await asyncio.sleep(.001)
        if '.git' in dirs:
            repo_list.append(root)
            # yield repo_list
            yield root
    if len(repo_list) > 1:
        print(f"{len(repo_list)} repos found!")
    elif len(repo_list) == 1:
        print('Only 1 repo found.')
    else:
        print('No repos found.')

def reset_repo(path: str, hard: bool = False):
    print(f'resetting repo {path}')
    cmd = ["git", "reset", "--hard"] if hard else ["git", "reset"]
    subprocess.run(cmd, cwd=path)
