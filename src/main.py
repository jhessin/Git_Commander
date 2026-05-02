import asyncio

import wx
from wxasync import WxAsyncApp

from .MainFrame import MainFrame


class GitCommander(WxAsyncApp):
    frame: MainFrame

    def OnInit(self):
        self.frame = MainFrame(None, wx.ID_ANY, "")
        self.SetTopWindow(self.frame)
        self.frame.Show()
        return True


async def main_async():
    app = GitCommander(1)
    await app.MainLoop()

def main(*args, **kwargs) -> None:
    asyncio.run(main_async())


if __name__ == "__main__":
    main()
