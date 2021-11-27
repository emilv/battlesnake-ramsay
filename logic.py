import random
from typing import Dict, Set

from api_types.api import Move, MoveRequest, MoveResponse
from board import Board


def get_move(state: MoveRequest) -> MoveResponse:
    board = Board(state)
    you = state.you

    all_moves: Set[Move] = {"up", "down", "left", "right"}
    possible_moves: Set[Move] = all_moves.copy()
    opposites: Dict[Move, Move] = {"up": "down", "down": "up", "left": "right", "right": "left"}

    x = you.head.x
    y = you.head.y
    head = board[x][y]

    # Find current direction and discard backwards move
    current_direction: Move = "up"
    if you.length > 1:
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
        if next_square.body:
            possible_moves.discard(move)

    # Pick move
    my_move: Move = "up"
    if current_direction in possible_moves:
        print("pick current direction")
        my_move = current_direction
    elif possible_moves:
        print("pick random")
        my_move = random.choice(list(possible_moves))

    for move in possible_moves:
        sq = head.move(move)
        if sq.food:
            print("pick food")
            my_move = move

    return MoveResponse(move=my_move, shout=None)
