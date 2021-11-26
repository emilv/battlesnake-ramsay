from typing_extensions import TypedDict


class RoyaleRules(TypedDict):
    shrinkEveryNTurns: int


class SquadRules(TypedDict):
    allowBodyCollisions: bool
    sharedElimination: bool
    sharedHealth: bool
    sharedLength: bool


class RulesetSettings(TypedDict):
    foodSpawnChance: int
    minimumFood: int
    hazardDamagePerTurn: int
    royale: RoyaleRules
    squad: SquadRules


class Ruleset(TypedDict):
    name: str
    version: str
    settings: RulesetSettings


class Game(TypedDict):
    id: str
    ruleset: Ruleset
    timeout: int
    source: str