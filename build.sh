#!/usr/bin/env bash

pyinstaller --noconfirm --onefile \
  --clean \
  --hidden-import wx \
  src/__main__.py