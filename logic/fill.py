import collections
from typing import Optional, Set, Tuple

from api_types.api import Move
from board import Board


def _inside(sq: Board.Square) -> bool:
    is_snake = sq.body and not sq.tail
    return not is_snake


def flood_fill_depth(start: Board.Square, direction: Move) -> Optional[int]:
    depth = 0
    visited: Set[Tuple[int, int]] = set()
    q = collections.deque([start.move(direction)])
    while q:
        n = q.popleft()
        if not n:
            continue
        coords = n.x, n.y
        visited.add(coords)
        if not _inside(n):
            continue
        depth += 1
        for direction in ["up", "down", "left", "right"]:
            nn = n.move(direction)
            if not nn or (nn.x, nn.y) in visited:
                continue
            q.append(nn)
    return depth
