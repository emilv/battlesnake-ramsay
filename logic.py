from api_types.api import MoveRequest, MoveResponse


def move(state: MoveRequest) -> MoveResponse:
    return {"move": "up", "shout": None}