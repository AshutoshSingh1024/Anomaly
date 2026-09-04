import json
from pathlib import Path
from game.state import GameState
from terminal.parser import CommandParser
from terminal.executor import CommandExecutor
from world.generation import create_initial_world

class GameController:
    def __init__(self):
        world = create_initial_world()
        self.state = GameState(world, world.create_player())
        self.parser = CommandParser()
        self.executor = CommandExecutor(self)
        self.messages = [
            "You are standing on a quiet road.",
            "Nothing appears to be waiting for you.",
            "", self.state.clock.display(), "Type 'help' for commands."
        ]

    def execute(self, raw):
        command = self.parser.parse(raw)
        if not command.name:
            return self.executor.result("")
        result = self.executor.execute(command)
        if result.consumes_time:
            self.state.clock.advance()
            self.state.world.tick(self.state)
        self.messages.extend([result.text, self.state.clock.display()])
        return result

    def save(self, path=Path("saves/save.json")):
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(self.state.to_dict(), indent=2), encoding="utf-8")

    def load(self, path=Path("saves/save.json")):
        self.state = GameState.from_dict(json.loads(path.read_text(encoding="utf-8")))
        self.messages = ["Saved world loaded.", "", self.state.clock.display()]

    def transcript(self):
        return "\n".join(self.messages[-80:])
