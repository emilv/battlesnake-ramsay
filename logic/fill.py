import collections
from typing import Optional, Set, Tuple

from api_types.api import Move
from board import Board


def _inside(sq: Board.Square) -> bool:
    is_snake = sq.body and not sq.tail
    return not is_snake


def flood_fill_depth(start: Board.Square, direction: Move) -> int:
    depth = 0
    max_depth = 64
    visited: Set[Tuple[int, int]] = set()

    n = start.move(direction)
    if not n:
        return 0

    q = collections.deque([n])
    while q:
        n = q.popleft()
        visited.add((n.x, n.y))
        if not _inside(n):
            continue
        depth += 1
        if depth > max_depth:
            return depth
        for direction in ["up", "down", "left", "right"]:
            nn = n.move(direction)
            if not nn or (nn.x, nn.y) in visited:
                continue
            q.append(nn)
    return depth
