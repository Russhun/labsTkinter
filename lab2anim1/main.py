import tkinter as tk
from canvas import NumberSystemCanvas


class MainApplication(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent

        self.c = NumberSystemCanvas(self.parent, width=600, height=500)
        self.c.pack(anchor="nw", side="top")


if __name__ == '__main__':
    root = tk.Tk()
    root.geometry("600x500")
    MainApplication(root).pack(side="top", fill="both", expand=True)
    root.mainloop()
