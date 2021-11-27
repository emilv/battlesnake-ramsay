from dataclasses import dataclass


@dataclass
class RoyaleRules:
    shrinkEveryNTurns: int


@dataclass
class SquadRules:
    allowBodyCollisions: bool
    sharedElimination: bool
    sharedHealth: bool
    sharedLength: bool


@dataclass
class RulesetSettings:
    foodSpawnChance: int
    minimumFood: int
    hazardDamagePerTurn: int
    royale: RoyaleRules
    squad: SquadRules


@dataclass
class Ruleset:
    name: str
    version: str
    settings: RulesetSettings


@dataclass
class Game:
    id: str
    ruleset: Ruleset
    timeout: int
    source: str
