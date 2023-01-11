import tkinter as tk
from buttons import NumCircleToggle
from abst import AbstractCanvas
from utils import SystemNumConverter


class NumberSystemCanvas(AbstractCanvas):
    def __init__(self, parent, *args, **kwargs):
        tk.Canvas.__init__(self, parent, *args, **kwargs)
        self.options = ["2->10", "3урв->10", "2-10->10"]
        self.parent: tk.Tk = parent

        self.btn_list = [NumCircleToggle(self, width=65, height=65) for _ in range(8)]
        for btn in self.btn_list:
            btn.pack(side="left")

        self.result_text = tk.Label(self, text="= 0", font=("", 16))
        self.result_text.pack(side="bottom", before=self.btn_list[0])

        self.option = tk.StringVar()
        self.option.set(self.options[0])
        self.option.trace("w", self.reset_toggles)

        self.option_menu = tk.OptionMenu(self, self.option, *self.options)
        self.option_menu.pack(side="bottom", before=self.result_text)
        self.option_menu.bind()

    def reset_toggles(self, *args):
        for btn in self.btn_list:
            btn.reset(self.option.get())
        self.result_text.configure(text="= 0")

    def get_toggles_nums(self) -> list[int]:
        return [btn.get_num() for btn in self.btn_list][::-1]

    def calc(self) -> None:
        d = {
            "2->10": 2,
            "3урв->10": 3
        }
        if self.option.get() in d.keys():
            self.result_text.configure(
                text=SystemNumConverter().from_n_to_10(d[self.option.get()],
                                                       self.get_toggles_nums()))
        else:
            self.result_text.configure(
                text=SystemNumConverter().from_2n10_to_10(self.get_toggles_nums()))

