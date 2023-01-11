import tkinter as tk
import tkinter.ttk as ttk


class AbstractMenuCanvas(tk.Canvas):
    ping_label: tk.Label
    title_label: tk.Label
    play_btn: ttk.Button
    style: ttk.Style
