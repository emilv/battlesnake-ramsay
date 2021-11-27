import dataclasses
import random
from typing import Optional, List, Set, Dict

from api_types.api import MoveRequest, MoveResponse, Move
from api_types.game import Battlesnake


class Board:
    @dataclasses.dataclass
    class Square:
        x: int
        y: int
        left: Optional['Board.Square'] = None
        right: Optional['Board.Square'] = None
        up: Optional['Board.Square'] = None
        down: Optional['Board.Square'] = None

        food: bool = False
        hazard: bool = False

        body: bool = False
        head: bool = False
        tail: bool = False
        you: bool = False
        your_neck: bool = False
        snake: Optional[Battlesnake] = None

        is_border: bool = False
        is_left: bool = False
        is_right: bool = False
        is_top: bool = False
        is_bottom: bool = False

        def move(self, direction: Move) -> Optional['Board.Square']:
            if direction == "left":
                return self.left
            if direction == "right":
                return self.right
            if direction == "up":
                return self.up
            if direction == "down":
                return self.down


    squares: List[List[Square]]

    def __init__(self, state: MoveRequest):
        height = state['board']['height']
        width = state['board']['width']
        self.squares = [
            [self.Square(x, y) for y in range(height)]
            for x in range(width)
        ]

        for col in self.squares:
            for sq in col:
                sq.is_top = sq.y == height - 1
                sq.is_bottom = sq.y == 0
                sq.is_left = sq.x == 0
                sq.is_right = sq.x == width - 1
                sq.is_border = sq.is_top or sq.is_bottom or sq.is_left or sq.is_right

                if not sq.is_top:
                    sq.up = self.squares[sq.x][sq.y + 1]
                if not sq.is_bottom:
                    sq.down = self.squares[sq.x][sq.y - 1]
                if not sq.is_left:
                    sq.left = self.squares[sq.x - 1][sq.y]
                if not sq.is_right:
                    sq.right = self.squares[sq.x + 1][sq.y]

        for xy in state['board']['food']:
            self.squares[xy['x']][xy['y']].food = True
        for xy in state['board']['hazards']:
            self.squares[xy['x']][xy['y']].hazard = True

        you_id = state['you']['id']
        for s in state['board']['snakes']:
            is_you = s['id'] == you_id
            for i, xy in enumerate(s['body']):
                sq = self.squares[xy['x']][xy['y']]
                sq.body = True
                sq.head = i == 0
                sq.your_neck = i == 1 and is_you
                sq.tail = i == s['length'] - 1
                sq.you = is_you
                sq.snake = s

    def get(self, x: int, y: int) -> Square:
        return self.squares[x][y]

    def __getitem__(self, x: int):
        return self.squares[x]


def get_move(state: MoveRequest) -> MoveResponse:
    board = Board(state)
    you = state['you']

    all_moves: Set[Move] = {"up", "down", "left", "right"}
    possible_moves: Set[Move] = all_moves.copy()
    opposites: Dict[Move, Move] = {"up": "down", "down": "up", "left": "right", "right": "left"}

    x = you['head']['x']
    y = you['head']['y']
    head = board[x][y]

    # Find current direction and discard backwards move
    current_direction: Move = "up"
    if you['length'] > 1:
        for move in all_moves:
            sq = head.move(move)
            if sq and sq.your_neck:
                current_direction = opposites[move]
                possible_moves.discard(move)

    # Discard impossible moves
    for move in possible_moves.copy():
        next_square = head.move(move)
        if not next_square:
            possible_moves.discard(move)
            continue
        if next_square.body and not next_square.tail:
            possible_moves.discard(move)

    # Pick move
    my_move: Move = "up"
    #if current_direction in possible_moves:
    #    print("pick current direction")
    #    my_move = current_direction
    #elif
    if possible_moves:
        print("pick random")
        my_move = random.choice(list(possible_moves))

    return {"move": my_move, "shout": None}
