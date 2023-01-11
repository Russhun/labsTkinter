import tkinter as tk


class AbstractCanvas(tk.Canvas):
    def __init__(self, parent, *args, **kwargs):
        tk.Canvas.__init__(self, parent, *args, **kwargs)

    def calc(self):
        pass
