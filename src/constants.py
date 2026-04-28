import os
import sys


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


class classproperty:
    def __init__(self, fget):
        self.fget = fget

    def __get__(self, instance, owner):
        return self.fget(owner)


class Consts:
    @classproperty
    def PICKLE_FILE(cls) -> str:
        return data_path('repos.dat')

    @classproperty
    def REPOS_DIRECTORY(cls) -> str:
        return os.path.join(os.path.expanduser("~"), "repos")
