import tkinter as tk
from tkinter import messagebox

from game.controller import GameController
from ui.world_view import WorldView
from ui.terminal_view import TerminalView


class AnomalyApp:
    def __init__(self):
        self.controller = GameController()

        self.root = tk.Tk()
        self.root.title("Anomaly")
        self.root.geometry("1100x700")
        self.root.minsize(850, 550)

        main = tk.Frame(
            self.root,
            bg="#080a0d"
        )

        main.pack(
            fill="both",
            expand=True
        )

        self.world = WorldView(
            main,
            self.controller
        )

        self.world.pack(
            fill="both",
            expand=True,
            padx=8,
            pady=(8, 4)
        )

        self.terminal = TerminalView(
            main,
            self.command,
            self.continue_interaction
        )

        self.terminal.pack(
            fill="both",
            expand=True,
            padx=8,
            pady=(4, 8)
        )

        self.refresh()

        self.root.protocol(
            "WM_DELETE_WINDOW",
            self.close
        )

        self.root.after(
            1000,
            self.realtime_tick
        )

    def command(self, text):
        result = self.controller.execute(text)

        self.terminal.refresh(
            self.controller.transcript()
        )

        self.world.refresh()

        if result.quit_requested:
            self.root.after(
                50,
                self.root.destroy
            )
            return

        # Every interaction pauses the simulation.
        self.controller.pause_for_interaction()
        self.terminal.lock()

    def continue_interaction(self):
        self.controller.continue_after_interaction()

        self.terminal.unlock()

        self.world.refresh()

        self.terminal.refresh(
            self.controller.transcript()
        )

    def realtime_tick(self):
        # 1 real second = 2 game minutes.
        # Therefore 5 real seconds = 10 game minutes.
        if (
            self.controller.time_running
            and not self.controller.interaction_paused
        ):
            self.controller.advance_time(2)

            self.world.refresh()

            self.terminal.refresh(
                self.controller.transcript()
            )

        self.root.after(
            1000,
            self.realtime_tick
        )

    def refresh(self):
        self.terminal.refresh(
            self.controller.transcript()
        )

        self.world.refresh()

    def close(self):
        if messagebox.askyesno(
            "Anomaly",
            "Exit the game?"
        ):
            self.root.destroy()

    def run(self):
        self.root.mainloop()