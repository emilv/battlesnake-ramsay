import random
from typing import Dict, Set

from api_types.api import Move, MoveRequest, MoveResponse
from board import Board


def get_move(state: MoveRequest) -> MoveResponse:
    board = Board(state)
    you = state.you

    all_moves: Set[Move] = {"up", "down", "left", "right"}
    opposites: Dict[Move, Move] = {"up": "down", "down": "up", "left": "right", "right": "left"}
    possible_moves: Set[Move] = all_moves.copy()
    disliked_moves: Set[Move] = set()
    preferred_moves: Set[Move] = set()

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

    # Dislike border moves
    for move in possible_moves:
        sq = head.move(move)
        if sq and sq.is_border:
            disliked_moves.add(move)

    # Dislike moves with opponent head two steps away
    # Prefer moves with food 1-2 steps away
    for move1 in possible_moves:
        first = head.move(move1)
        if first:
            if first.food and you.health <= 50:
                preferred_moves.add(move1)
            elif first.food and you.health >= 80:
                disliked_moves.add(move1)
            for move2 in all_moves - {opposites[move1]}:
                second = first.move(move2)
                if second:
                    if second.head:
                        disliked_moves.add(move1)
                    elif second.food and you.health <= 50:
                        preferred_moves.add(move1)

    # Pick move
    my_move: Move = "up"

    preferred_moves -= disliked_moves
    preferred_moves &= possible_moves

    neutral_moves = possible_moves - disliked_moves - preferred_moves

    prio = [
        ("preferred", preferred_moves),
        ("neutral", neutral_moves),
        ("disliked", disliked_moves),
    ]

    for txt, st in prio:
        if not st: continue
        if current_direction in st:
            print(f"pick current direction from {txt}")
            my_move = current_direction
            break
        else:
            print(f"pick random from {txt}")
            my_move = random.choice(list(st))
            break

    return MoveResponse(move=my_move, shout=None)
