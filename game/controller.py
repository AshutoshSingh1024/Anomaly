import json
from pathlib import Path

from game.state import GameState
from terminal.parser import CommandParser
from terminal.executor import CommandExecutor
from world.generation import create_initial_world


class GameController:
    def __init__(self):
        world = create_initial_world()

        self.state = GameState(
            world,
            world.create_player()
        )

        self.parser = CommandParser()
        self.executor = CommandExecutor(self)

        # Automatic simulation time.
        self.time_running = True

        # Temporary interaction pause.
        # This is different from the user's manual stop command.
        self.interaction_paused = False

        self.messages = [
            "You are standing on a quiet road.",
            "Nothing appears to be waiting for you.",
            "",
            self.state.clock.display(),
            "Type 'help' for commands."
        ]

    def execute(self, raw):
        command = self.parser.parse(raw)

        if not command.name:
            return self.executor.result("", False)

        result = self.executor.execute(command)

        if result.consumes_time and self.time_running:
            self.advance_time(2)

        self.messages.extend([
            result.text,
            self.state.clock.display()
        ])

        # A completed player command always creates an interaction boundary.
        # Whether the clock is manually running is deliberately independent
        # from this temporary pause.
        if not result.quit_requested:
            self.pause_for_interaction()

        return result

    def advance_time(self, minutes=2):
        if not self.time_running:
            return

        if self.interaction_paused:
            return

        old_day = self.state.clock.day

        self.state.clock.advance_minutes(minutes)

        self.state.world.tick(self.state)

        if self.state.clock.day != old_day:
            self.messages.append(
                f"A new day begins. Day {self.state.clock.day}."
            )

    def pause_for_interaction(self):
        self.interaction_paused = True

    def continue_after_interaction(self):
        self.interaction_paused = False

    def start_time(self):
        self.time_running = True

    def stop_time(self):
        self.time_running = False

    def toggle_time(self):
        self.time_running = not self.time_running
        return self.time_running

    def save(self, path=Path("saves/save.json")):
        path.parent.mkdir(parents=True, exist_ok=True)

        path.write_text(
            json.dumps(
                self.state.to_dict(),
                indent=2
            ),
            encoding="utf-8"
        )

    def load(self, path=Path("saves/save.json")):
        self.state = GameState.from_dict(
            json.loads(
                path.read_text(
                    encoding="utf-8"
                )
            )
        )

        self.messages = [
            "Saved world loaded.",
            "",
            self.state.clock.display()
        ]

    def transcript(self):
        return "\n".join(
            self.messages[-80:]
        )
