import tkinter as tk
import asyncio
import secrets

import time
import aiohttp

from lab4game.client.canvas.canvas import MenuCanvas, GameCanvas
from lab4game.client.game_client import QueueClient
from lab4game.client.graphics.graphics import GameBall, GamePad


class MainFrame(tk.Frame):
    def __init__(self, parent, client_id, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.game_client = QueueClient(client_id)
        self._ping_flag = True
        self._find_game_flag = True

        self.menu_canvas = MenuCanvas(self, width=750, height=450, bg="#282828", bd=0, highlightthickness=0)
        self._init_menu_canvas()
        self.menu_canvas.place(x=0, y=0)

        self.game_canvas = GameCanvas(self, width=750, height=450, bg="#282828", bd=0, highlightthickness=0)
        self._init_game_canvas()

    def find_game(self):
        self.menu_canvas.play_btn.place_forget()
        self.menu_canvas.queue_time_label.place(x=375, y=225, anchor="center")
        self.menu_canvas.leave_queue_btn.place(x=375, y=265, anchor="center")
        asyncio.get_running_loop().create_task(self.game_client.queue_lobby(self.queue_callback), name="find_game_task")
        self.menu_canvas.leave_queue_btn.configure(command=self.leave_queue)

    def leave_queue(self):
        self.game_client.leave_queue()
        self.menu_canvas.leave_queue_btn.place_forget()
        self.menu_canvas.queue_time_label.place_forget()
        self.menu_canvas.queue_time_label.configure(text="QueueTime")
        self.menu_canvas.place_initial()

    def queue_callback(self, status="", q_time=0, game_id=""):
        if status == "queue":
            self.menu_canvas.queue_time_label.configure(text=f"~{int(q_time)}сек")
        elif status == "ready":
            self.change_canvas_to_game()
            self.game_canvas.wait_connection()
            asyncio.get_running_loop().create_task(self.game_client.connect_to_game(game_id, self.game_callback))

    def game_callback(self, action="", data: list = None):
        print(data)
        if action == "set_side":
            if data[0] == "player_1":
                self.game_canvas.pad1.configure(bg="red")
                self.game_canvas.pad1.bind("<Key>", self.game_client.move_pad)
            elif data[0] == "player_2":
                self.game_canvas.pad2.configure(bg="red")
                self.game_canvas.pad2.bind("<Key>", self.game_client.move_pad)

    def destroy(self) -> None:
        print("Destroing")
        self.game_client.leave_queue()

    def change_canvas_to_game(self):
        self.menu_canvas.place_forget()
        self.game_canvas.place(x=0, y=0)
        self.game_canvas.place_initial()

    def change_canvas_to_menu(self):
        self.game_canvas.place_forget()
        self.menu_canvas.place(x=0, y=0)

    def _init_menu_canvas(self):
        self.menu_canvas.place_initial()
        self.menu_canvas.play_btn.configure(command=self.find_game)
        asyncio.get_running_loop().create_task(
            self.game_client.check_ping(self.menu_canvas.ping_label),
            name="check_ping_task")

    def _init_game_canvas(self):
        self.game_canvas.ball.bind("<Button-1>", lambda x: print(x))

