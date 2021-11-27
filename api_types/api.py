from typing import Optional

from typing_extensions import Literal, TypedDict

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


Move = Literal["up", "down", "left", "right"]


class MoveResponse(TypedDict):
    move: Move
    shout: Optional[str]


class EndRequest(State):
    pass
