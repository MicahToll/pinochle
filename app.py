#!/usr/bin/env python

import asyncio
import websockets
import json
import itertools
from main import Game
import secrets


JOIN = {}


async def start(websocket):
    # Initialize Pinochle game, the set of WebSocket connections
    # receiving moves from this game, and secret access token.
    players = ["Lizzy", "Micah", "Dad", "Mom"]
    game = Game(players)
    connected = {websocket}

    join_key = secrets.token_urlsafe(12)
    JOIN[join_key] = game, connected

    try:
        # Send the secret access token to the browser of the first player,
        # where it'll be used for building a "join" link.
        event = {
            "type": "init",
            "join": join_key,
        }
        await websocket.send(json.dumps(event))

        # Temporary - for testing.
        print("first player started game", id(game))
        async for message in websocket:
            print("first player sent", message)

    finally:
        del JOIN[join_key]


async def error(websocket, message):
    event = {
        "type": "error",
        "message": message,
    }
    await websocket.send(json.dumps(event))


async def join(websocket, join_key):
    # Find the Connect Four game.
    try:
        game, connected = JOIN[join_key]
    except KeyError:
        await error(websocket, "Game not found.")
        return

    # Register to receive moves from this game.
    connected.add(websocket)
    try:
        # Temporary - for testing.
        print("second player joined game", id(game))
        async for message in websocket:
            print("second player sent", message)

    finally:
        connected.remove(websocket)


async def handler(websocket, somethingelse):
    # Receive and parse the "init" event from the UI.
    message = await websocket.recv()
    event = json.loads(message)
    assert event["type"] == "init"

    if "join" in event:
        # Second player joins an existing game.
        await join(websocket, event["join"])
    else:
        # First player starts a new game.
        await start(websocket)

async def main():
    async with websockets.serve(handler, "", 8001):
        await asyncio.Future()  # run forever

if __name__ == "__main__":
    asyncio.run(main())

#stuff
"""
what does each client know?
their hand, the playing area

what does the server know?
every player's hand and the play area

so
each message to server should look like: 
{newly_played: [], "other":False}

and each message from server should look like:
{hand:[], play_area: [], new request(if there is one)}
"""