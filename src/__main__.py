import asyncio

import wx
from wxasync import WxAsyncApp
from MyFrame import MyFrame


class GitCommander(WxAsyncApp):
    frame: MyFrame

    def OnInit(self):
        self.frame = MyFrame(None, wx.ID_ANY, "")
        self.SetTopWindow(self.frame)
        self.frame.Show()
        return True


async def main():
    app = GitCommander(1)
    await app.MainLoop()

if __name__ == "__main__":
    asyncio.run(main())