import logging
import os
import time
from typing import cast

from flask import Flask
from flask import request

import logic
from api_types.api import InfoResponse, StartRequest, MoveResponse, MoveRequest, EndRequest

app = Flask(__name__)


@app.get("/")
def handle_info() -> InfoResponse:
    print("INFO")
    return {
        "apiversion": "1",
        "author": "lajm",
        "color": "#6699cc",
        "head": "all-seeing",
        "tail": "default",
        "version": "0.0.1"
    }


@app.post("/start")
def handle_start() -> str:
    data = cast(StartRequest, request.get_json())
    print(f"{data['game']['id']} START")
    return "."


@app.post("/move")
def handle_move() -> MoveResponse:
    data = cast(MoveRequest, request.get_json())
    move = logic.get_move(data)
    print(f"{data['game']['id']} MOVE: {move['move']}")
    return move


@app.post("/end")
def handle_end() -> str:
    data = cast(EndRequest, request.get_json())

    print(f"{data['game']['id']} END")
    return "."


if __name__ == "__main__":
    logging.getLogger("werkzeug").setLevel(logging.ERROR)

    print("Starting...")
    port = int(os.environ.get("PORT", "8080"))
    app.run(host="0.0.0.0", port=port, debug=True)
