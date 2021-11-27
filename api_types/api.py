from dataclasses import dataclass
from typing import Optional

from typing_extensions import Literal

from api_types.game import State


@dataclass
class InfoResponse:
    apiversion: str
    author: str
    color: str
    head: str
    tail: str
    version: Optional[str]


@dataclass
class StartRequest(State):
    pass

@dataclass
class MoveRequest(State):
    pass


Move = Literal["up", "down", "left", "right"]


@dataclass
class MoveResponse:
    move: Move
    shout: Optional[str]

@dataclass
class EndRequest(State):
    pass
