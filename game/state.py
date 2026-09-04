from dataclasses import dataclass, field
from game.clock import GameClock
from world.world import World
from world.player import Player

@dataclass
class GameState:
    world: World
    player: Player
    clock: GameClock = field(default_factory=GameClock)

    def to_dict(self):
        return {"clock": {"day": self.clock.day, "hour": self.clock.hour, "minute": self.clock.minute},
                "player": self.player.to_dict(), "world": self.world.to_dict()}

    @classmethod
    def from_dict(cls, data):
        c = data.get("clock", {})
        return cls(World.from_dict(data.get("world", {})),
                   Player.from_dict(data.get("player", {})),
                   GameClock(int(c.get("day", 1)), int(c.get("hour", 8)), int(c.get("minute", 0))))
