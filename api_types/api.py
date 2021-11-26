from typing import Optional, Literal

from typing_extensions import TypedDict

from api_types.game import State


class InfoResponse(TypedDict):
    apiversion: str
    author: str
    color: str
    head: str
    tail: str
    version: Optional[str]


class StartRequest(State):
    pass


class MoveRequest(State):
    pass


class MoveResponse(TypedDict):
    move: Literal["up", "down", "left", "right"]
    shout: Optional[str]


class EndRequest(State):
    pass
