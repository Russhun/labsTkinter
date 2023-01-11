import tkinter as tk
from utils import RecurNumCounter
from abst import AbstractCanvas

numsys_dict = {
    "2->10": [0, 1],
    "3урв->10": [0, 1, -1],
    "2-10->10": [0, 1]
}


class NumCircleToggle(tk.Canvas):
    def __init__(self, parent: AbstractCanvas, *args, **kwargs):
        tk.Canvas.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.num_counter = RecurNumCounter([0, 1])
        self.create_oval(5, 5, 65, 65, fill="black", outline="black")
        self.text = self.create_text(35, 35, text='0', fill="white", font=("", 16))
        self.bind("<Button-1>", self._click)

    def get_num(self) -> int:
        return self.num_counter.get_current()

    def reset(self, new_sys) -> None:
        self.itemconfigure(self.text, text=0)
        self.num_counter.set_list(numsys_dict[new_sys])

    def _click(self, event) -> None:
        self.itemconfigure(self.text, text=self.num_counter.next())
        self.parent.calc()
