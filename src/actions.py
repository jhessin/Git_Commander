import asyncio
import os
from typing import Any, AsyncGenerator

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from MainFrame import MainFrame


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
