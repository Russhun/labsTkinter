import time
import tkinter as tk

import aiohttp

import asyncio

from aiohttp import ClientWebSocketResponse


class QueueClient:
    def __init__(self, client_id):
        self.client_id = client_id
        self._queue_flag = True
        self._ping_flag = True
        self.game_websocket: ClientWebSocketResponse | None = None
        self.is_pad_move_up: bool | None = None
        self._session = aiohttp.ClientSession()

    async def queue_lobby(self, callback: callable):
        payload = {"action": "find_game", "client_id": self.client_id}
        self._queue_flag = True
        async with self._session.ws_connect("ws://127.0.0.1:8000/findgame") as websocket:
            await websocket.send_json(payload)
            asyncio.get_running_loop().create_task(self.queue_lobby_receiver(websocket, callback))
            while self._queue_flag:
                print("Here1")
                await websocket.send_json({"status": "check_queue", "client_id": self.client_id})
                await asyncio.sleep(0.1)
            await websocket.send_json({"status": "exit_queue", "client_id": self.client_id})

    async def queue_lobby_receiver(self, ws, callback):
        start = time.time()
        while True:
            resp = await ws.receive_json()
            print(resp)
            if resp["status"] == "in_queue":
                callback("queue", time.time() - start)
            elif resp["status"] == "ready":
                print("STATUS: READY")
                self._queue_flag = False
                callback(status="ready", game_id=resp["game_id"])
                print("AFTER CALLBACK")
                break
            await asyncio.sleep(0.1)

    def leave_queue(self):
        self._queue_flag = False

    async def connect_to_game(self, game_id, callback: callable):
        print(game_id)
        async with self._session.ws_connect("ws://127.0.0.1:8000/game") as websocket:
            self.game_websocket = websocket
            await websocket.send_json({"field_id": game_id, "client_id": self.client_id})
            print("1 SANDED")
            data = await websocket.receive_json()
            print("2 RECEIVED")
            callback(action=data["action"], data=[data["side"]])
            data = await websocket.receive_json()
            print("3 RECEIVED")
            if data["action"] == "start":
                callback(action="start")
                while True:
                    data = await websocket.receive_json()
                    if data["action"] == "update_field":
                        callback(action="update_field", data=[data])




    async def check_ping(self, ping_label: tk.Label):
        while self._ping_flag:
            start = time.time_ns()
            await self._session.get("http://127.0.0.1:8000/ping")
            s_ping = f"ping: {int((time.time_ns()-start)/10**6)}ms"
            ping_label.configure(text=s_ping)
            await asyncio.sleep(2)

    def move_pad_up(self):
        self.is_pad_move_up = True

    def move_pad_down(self):
        self.is_pad_move_up = False

    def move_pad(self, event):
        print(event)


class GameClient:
    pass