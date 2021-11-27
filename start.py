import logging
import os
from dataclasses import asdict
from typing import Type, TypeVar

from dacite import from_dict
from flask import Flask, jsonify, request

import logic
from api_types.api import (EndRequest, InfoResponse, MoveRequest, MoveResponse,
                           StartRequest)

app = Flask(__name__)

T = TypeVar("T")


def _get_json(data_class: Type[T]) -> T:
    data = request.get_json()
    if not isinstance(data, dict):
        raise TypeError
    return from_dict(data_class=data_class, data=data)


@app.get("/")
def handle_info():
    print("INFO")
    return jsonify(InfoResponse(
        apiversion="1",
        author="lajm",
        color="#6699cc",
        head="all-seeing",
        tail="default",
        version="0.0.2",
    ))


@app.post("/start")
def handle_start():
    data = _get_json(StartRequest)
    print(f"{data.game.id} START")
    return "."


@app.post("/move")
def handle_move():
    data = _get_json(MoveRequest)
    move = logic.get_move(data)
    print(f"{data.game.id} MOVE: {move.move}")
    return jsonify(move)


@app.post("/end")
def handle_end():
    data = _get_json(EndRequest)
    print(f"{data.game.id} END")
    return "."


if __name__ == "__main__":
    logging.getLogger("werkzeug").setLevel(logging.ERROR)

    print("Starting...")
    port = int(os.environ.get("PORT", "8080"))
    app.run(host="0.0.0.0", port=port, debug=True)
