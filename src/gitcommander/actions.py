import os
import subprocess
import sys
from datetime import datetime
from pickle import dump, load

REPOS_DIRECTORY = os.path.join(os.path.expanduser('~'), 'repos')


async def clone(repo_name: str) -> str:
    """
    Clones the given repo using the GitHub cli
    :param repo_name: The name of the repo from GitHub
    :return: The directory the repo was cloned to.
    """
    print(REPOS_DIRECTORY)
    os.makedirs(REPOS_DIRECTORY, exist_ok=True)
    path = os.path.join(REPOS_DIRECTORY, repo_name.split('/')[-1])
    print(f'cloning repo {repo_name} to {path}')
    subprocess.run(['gh', 'repo', 'clone', repo_name, path], check=True)
    return path


async def push_repo(path: str):
    """
    Push the given repo.
    :param path: The path to a repo.
    :return: None
    """
    print(f"committing and pushing {path}")
    date = datetime.now()
    subprocess.run(['git', 'add', '.'], cwd=path, check=False)
    subprocess.run(['git', 'commit', f'-m "{date}"'], cwd=path, check=False)
    subprocess.run(['git', 'push'], cwd=path, check=False)


async def pull_repo(path: str):
    """
    Pull a given repo from GitHub
    :param path: The path to the repo
    :return: None
    """
    print(f"pulling {path}")
    subprocess.run(['git', 'pull'], cwd=path, check=False)
