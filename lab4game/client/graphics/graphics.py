import asyncio
import tkinter as tk


class GameBall(tk.Canvas):
    def __init__(self, parent, *args, **kwargs):
        tk.Canvas.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.create_oval(0, 0, 19, 19, fill="black")


class GamePad(tk.Canvas):
    def __init__(self, parent, *args, **kwargs):
        tk.Canvas.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.pad = self.create_rectangle(0, 0, 10, 60, fill="black", outline="black")


