from dataclasses import dataclass
from typing import List

from api_types.rules import Game


@dataclass
class Coordinates:
    x: int
    y: int


@dataclass
class Battlesnake:
    id: str
    name: str
    squad: str
    latency: str
    health: int
    length: int
    body: List[Coordinates]
    head: Coordinates
    shout: str


@dataclass
class Board:
    height: int
    width: int
    food: List[Coordinates]
    hazards: List[Coordinates]
    snakes: List[Battlesnake]


@dataclass
class State:
    game: Game
    turn: int
    board: Board
    you: Battlesnake
