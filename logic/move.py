import random
from typing import Dict, Set, Tuple

from api_types.api import Move, MoveRequest, MoveResponse
from board import Board
from logic.fill import flood_fill_depth


def best_direction(directions: Set[Move], board: Board, start: Tuple[int, int]) -> Move:
    x, y = start
    square = board[x][y]
    scored = [(flood_fill_depth(square, direction), direction) for direction in directions]
    filtered = [(s, d) for s, d in scored if s]
    sort = sorted(filtered, key=lambda x: x[0], reverse=True)
    best_score = sort[0][0]
    best_group = [b for a, b in sort if a == best_score]
    print(sort)
    print(best_group)
    return random.choice(best_group)


def get_move(state: MoveRequest) -> MoveResponse:
    board = Board(state)
    you = state.you

    all_moves: Set[Move] = {"up", "down", "left", "right"}
    opposites: Dict[Move, Move] = {"up": "down", "down": "up", "left": "right", "right": "left"}
    possible_moves: Set[Move] = all_moves.copy()

    border_moves: Set[Move] = set()
    food_moves: Set[Move] = set()
    first_food_moves: Set[Move] = set()
    fight_moves: Set[Move] = set()

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

    # Identify border moves
    for move in possible_moves:
        sq = head.move(move)
        if sq and sq.is_border:
            border_moves.add(move)

    # What happens when we move two steps?
    for move1 in possible_moves.copy():
        first = head.move(move1)
        second_possible = False
        if first:
            if first.food:
                food_moves.add(move1)
                first_food_moves.add(move1)
            for move2 in all_moves - {opposites[move1]}:
                second = first.move(move2)
                if second:
                    if not second.snake and not second.tail:
                        second_possible = True
                    if second.head and second.snake.length >= you.length:
                        fight_moves.add(move1)
                        second_possible = True
                    if second.food:
                        food_moves.add(move1)
        if not second_possible:
            possible_moves.discard(move1)

    # Pick move
    safe_moves = possible_moves - fight_moves

    hungry = (safe_moves & food_moves) if you.health < 30 else set()
    neutral_moves = safe_moves - border_moves - first_food_moves

    prio = [
        ("hungry", hungry),
        ("neutral food stink", neutral_moves - food_moves),
        ("neutral", neutral_moves),
        ("safe no border", safe_moves - border_moves),
        ("safe border", safe_moves & border_moves),
        ("safe", safe_moves),
        ("fight", fight_moves),
    ]

    my_move: Move = "up"
    found = False
    for txt, prio_set in prio:
        st = possible_moves & prio_set
        if not st:
            continue
        my_move = best_direction(st, board, (you.head.x, you.head.y))
        print(f"PICK best   FROM {txt}")
        found = True
        break

    if not found:
        print("DEATH BY head-on crash?")
        my_move = current_direction
        for direction in all_moves - {opposites[current_direction]}:
            mv = head.move(direction)
            if not mv:
                if not found:
                    print("DEATH BY border?")
                    my_move = direction
                continue
            if mv.you:
                print("DEATH BY seppuku?")
                my_move = direction
                found = True
                continue
            if not mv.snake:
                print("DEATH BY freedom!")
                my_move = direction
                break

    return MoveResponse(move=my_move, shout=None)
