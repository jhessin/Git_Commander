# Git Commander

When you just want to Git stuff done!

Git Commander is a simple UI that can be used to pull and push multiple git
repos for you so you can just focus on working. This software is provided as is
and will add all files to your repos with a simple timestamp commit. Use with
caution as this can push things to github that you didn't intend to push.

It is open-sourced and you can see everything it does.

## Features

- Simple UI
- No bells and whistles.
- manages repos for you!

## What Git Commander doesn't do

- No granular control over what files get added to your repository.
- no merging help.
- no diffing.

## What's the point?

I use git to sync many different projects between my various work/home computers
and this tool helps me do that. It isn't really designed for multi-user
collaboration, but for multi-computer colaboration.

## Installation

To install Git Commander you first need to have git (obviously) and the [Github
Cli tool](https://cli.github.com/).

Once that is done you can download the
[latest release](https://github.com/jhessin/Git_Commander/releases/latest).

To get the current test version you can clone this repository and use 
[Poetry](https://python-poetry.org/) to install it

```bash
poetry install
```

Afterward you can either run it directly:

```bash
poetry run gc
```

or you can build and install it:

```bash
poetry build
pipx install dist/git_commander-0.1.0-py3-none-any.whl
```

Then you can run it from anywhere with:

```bash
gc.exe
```

I will eventually be submitting this project to [PyPI](https://pypi.org/) once I think it is ready, but that is not for a while.


Git Commander will store a single config file with your list of repos.
This is stored here: `$(PKG_CONFIG_PATH:~/.config/GitCommander)/repos.dat`. 
