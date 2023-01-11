import time
import tkinter as tk

import aiohttp

import asyncio


class QueueClient:
    def __init__(self, client_id):
        self.client_id = client_id
        self._queue_flag = True
        self._ping_flag = True
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
                await asyncio.sleep(1)
            await websocket.send_json({"status": "exit_queue", "client_id": self.client_id})

    async def queue_lobby_receiver(self, ws, callback):
        start = time.time()
        while True:
            resp = await ws.receive_json()
            print(resp)
            if resp["status"] == "in_queue":
                callback("queue", time.time() - start)
            elif resp["status"] == "ready":
                callback(status="ready", game_id=resp["game_id"])
                break
            await asyncio.sleep(1)

    def leave_queue(self):
        self._queue_flag = False

    async def connect_to_game(self, game_id, callback: callable):
        async with self._session.ws_connect("ws://127.0.0.1:8000/game") as websocket:
            await websocket.send_json({"field_id": game_id, "client_id": self.client_id})
            data = await websocket.receive_json()
            callback(action=data["action"], data=[data["side"]])

    async def check_ping(self, ping_label: tk.Label):
        while self._ping_flag:
            start = time.time_ns()
            await self._session.get("http://127.0.0.1:8000/ping")
            s_ping = f"ping: {int((time.time_ns()-start)/10**6)}ms"
            ping_label.configure(text=s_ping)
            await asyncio.sleep(2)

    def move_pad(self, event):
        print(event)


class GameClient:
    pass