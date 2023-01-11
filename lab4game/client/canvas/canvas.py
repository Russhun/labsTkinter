import asyncio
import tkinter as tk
import tkinter.ttk as ttk

from lab4game.client.graphics.graphics import GameBall, GamePad


class MenuCanvas(tk.Canvas):
    def __init__(self, parent, *args, **kwargs):
        tk.Canvas.__init__(self, parent, *args, **kwargs)

        self.ping_label = tk.Label(self, text="ping: -1ms", bg="#282828", fg="#ffffff")

        self.title_label = tk.Label(self, text="Ping-Pong", font=("TkHeadingFont", 32, "bold"), bg="#282828", fg="#ffffff")

        self.style = ttk.Style()
        self.style.configure('My.TButton', font=
        ('calibri', 16, 'bold'),
                        borderwidth='4')

        self.play_btn = ttk.Button(self, text="Найти игру", style="My.TButton")

        self.queue_time_label = tk.Label(self, text="0сек.", bg="#282828", fg="#ffffff", font=("", 14, "bold"))
        self.leave_queue_btn = ttk.Button(self, text="Отмена", style="My.TButton", width=10)

    def place_initial(self):
        self.ping_label.place(x=5, y=5)
        self.title_label.place(relx=0.5, rely=0.15, anchor=tk.CENTER)
        self.play_btn.place(relheight=0.09, relwidth=0.2, relx=0.5, rely=0.40, anchor=tk.CENTER)


class GameCanvas(tk.Canvas):
    def __init__(self, parent, *args, **kwargs):
        tk.Canvas.__init__(self, parent, *args, **kwargs)
        self.parent = parent

        self.c = tk.Canvas(self, width=750, height=450, bg="gray", bd=0, highlightthickness=0)

        self.c.create_line(375, 0, 375, 450, fill="#eeeeee", dash=[100], width=5)

        self.label_score1 = tk.Label(self.c, text="5", bg="gray", font=("", 32, "bold"))

        self.label_score2 = tk.Label(self.c, text="5", bg="gray", font=("", 32, "bold"))

        self.ball = GameBall(self.c, width=20, height=20, bd=0, highlightthickness=0, bg="gray")

        self.pad1 = GamePad(self.c, width=10, height=60, bd=0, highlightthickness=0)

        self.pad2 = GamePad(self.c, width=10, height=60, bd=0, highlightthickness=0)

        self.connection_label = tk.Label(self.c, text="Соединение", bg="#444444", font=("", 32, "bold"))

    def place_initial(self):
        self.c.place(x=0, y=0)
        self.label_score1.place(x=250, y=112, anchor="center")
        self.label_score2.place(x=500, y=112, anchor="center")
        self.ball.place(x=365, y=215)
        self.pad1.place(x=15, y=185)
        self.pad2.place(x=725, y=185)

    def wait_connection(self):
        self.connection_label.place(x=375, y=225, anchor="center")



