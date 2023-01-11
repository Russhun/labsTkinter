import asyncio

import tkinter as tk
from asyncio import AbstractEventLoop

import secrets

from lab4game.client.frames.frames import MainFrame


class App:
    async def exec(self):
        self.window = Window(asyncio.get_event_loop())
        await self.window.show()


class Window(tk.Tk):
    def __init__(self, loop: AbstractEventLoop):
        super().__init__()
        self._client_id = secrets.token_hex(8)
        self.loop = loop
        self._run = True
        self.geometry("750x450")
        self.resizable(width=False, height=False)
        self.protocol("WM_DELETE_WINDOW", self.on_close)
        self.wm_attributes("-transparentcolor", "brown")

        self.menu_frame = MainFrame(self, self._client_id)
        self.menu_frame.pack(side="top", fill="both", expand=True)

    async def show(self):
        while self._run:
            self.update()
            await asyncio.sleep(.1)
        await asyncio.sleep(1)

    def on_close(self):
        print("OnClose")
        self.menu_frame.destroy()
        self._run = False


if __name__ == '__main__':
    asyncio.run(App().exec())


