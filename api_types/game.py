from typing import TypedDict, List
from typing_extensions import TypedDict

from api_types.rules import Game


class Coordinates(TypedDict):
    x: int
    y: int


class Battlesnake(TypedDict):
    id: str
    name: str
    squad: str
    latency: str
    health: int
    length: int
    body: List[Coordinates]
    head: Coordinates
    shout: str


class Board(TypedDict):
    height: int
    width: int
    food: List[Coordinates]
    hazards: List[Coordinates]
    snakes: List[Battlesnake]


class State(TypedDict):
    game: Game
    turn: int
    board: Board
    you: Battlesnake
