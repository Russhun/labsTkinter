import secrets
from asyncio import CancelledError

import websockets.connection
from sanic import Sanic, Request, Websocket

from sanic.response import json, text
import json as js
import asyncio
import random as rnd

from websockets.exceptions import ConnectionClosed

from lab4game.server.models.models import GameField
from lab4game.server.repository.repository import GameRepository

app = Sanic("MyHelloWorldApp")
games_repository = GameRepository()

lobbies: dict = {}
game_connections = {}
ws_store = {}


@app.websocket("/findgame")
async def find_game(request: Request, ws: Websocket):
    ws.close_timeout = 5
    data = js.loads(await ws.recv())
    if data["action"] == "find_game":
        if len(lobbies) > 0:
            lobby_id = list(lobbies.keys())[0]
            lobbies[lobby_id].append([ws, data["client_id"]])
            if lobbies[lobby_id][0][0].ws_proto.state == websockets.connection.State.OPEN:
                game_id = secrets.token_hex(16)
                await lobbies[lobby_id][0][0].send(js.dumps({"status": "ready", "game_id": game_id}))
                await ws.send(js.dumps({"status": "ready", "game_id": game_id}))
                games_repository.add_game_field(game_id, GameField(game_id, lobbies[lobby_id][0][0],
                                                                   lobbies[lobby_id][0][1]))
            else:
                await lobbies[lobby_id][0][0].close()
            lobbies.pop(lobby_id)
            print(f"Lobby {lobby_id} removed")
        lobby_id = str(rnd.randint(1000, 9999))
        lobbies[lobby_id] = [[ws, data["client_id"]]]
        await ws.send(js.dumps({"status": "in_queue", "lobby_id": lobby_id}))

        # noinspection PyAsyncCall
        request.app.add_task(queue_receiver(ws, lobby_id), name=f"receiver_{data['client_id']}")
        try:
            while True:
                print("HEREREE")
                await ws.send(js.dumps({"status": "in_queue", "lobby_id": lobby_id}))
                print("SENDED1")
                await asyncio.sleep(1)
        except CancelledError:
            pass
        finally:
            print("HEREREERERERERERE2")
            await request.app.cancel_task(f"receiver_{data['client_id']}")
            request.app.purge_tasks()


async def queue_receiver(ws: Websocket, lobby_id):
    while True:
        print("reciever")
        data = js.loads(await ws.recv())
        print(data)
        if data["status"] == "exit_queue":
            if lobby_id in lobbies:
                lobbies.pop(lobby_id)
            print("terminated")
            await ws.close()
            break


@app.websocket("/game")
async def game(request: Request, ws: Websocket):
    data = js.loads(await ws.recv())
    game_field = games_repository.get_game_field(data["field_id"])
    if game_field.field_id not in game_connections:
        game_connections[game_field.field_id] = {}
    if data["client_id"] == game_field.player1_id:
        game_connections[game_field.field_id]["player_1"] = data["client_id"]
        await ws.send(js.dumps({"action": "set_side", "side": "player_1"}))
    elif data["client_id"] == game_field.player2_id:
        game_connections[game_field.field_id]["player_2"] = data["client_id"]
        await ws.send(js.dumps({"action": "set_side", "side": "player_2"}))
    while True:
        await asyncio.sleep(1)


async def send_game_data(ws: Websocket):
    pass


async def receive_game_data(ws: Websocket):
    pass



@app.get("/ping")
async def ping(request: Request):
    return text("pong")
