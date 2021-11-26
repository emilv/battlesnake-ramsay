import logging
import os

from quart import Quart
from quart import request

import logic
from api_types.api import InfoResponse, StartRequest, MoveResponse, MoveRequest, EndRequest

app = Quart(__name__)


@app.get("/")
async def handle_info() -> InfoResponse:
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
async def handle_start() -> str:
    data: StartRequest = await request.get_json()
    print(f"{data['game']['id']} START")
    return "."


@app.post("/move")
async def handle_move() -> MoveResponse:
    data: MoveRequest = await request.get_json()
    return logic.move(data)


@app.post("/end")
async def end() -> str:
    """
    This function is called when a game your snake was in ends.
    It's purely for informational purposes, you don't have to make any decisions here.
    """
    data: EndRequest = await request.get_json()

    print(f"{data['game']['id']} END")
    return "."


if __name__ == "__main__":
    logging.getLogger("werkzeug").setLevel(logging.ERROR)

    print("Starting...")
    port = int(os.environ.get("PORT", "8080"))
    app.run(host="0.0.0.0", port=port, debug=True)
