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

        self.top_bar = tk.Frame(main, bg="#111820", height=34)
        self.top_bar.pack(fill="x", padx=8, pady=(8, 0))
        self.top_bar.pack_propagate(False)
        tk.Label(
            self.top_bar,
            text="ANOMALY // WORLD INTERFACE",
            bg="#111820",
            fg="#d8e7f4",
            font=("Consolas", 10, "bold")
        ).pack(side="left", padx=10)
        tk.Button(
            self.top_bar,
            text="WORLD LOG",
            command=self.show_world_log,
            bg="#263746",
            fg="#ffffff",
            activebackground="#3b566b",
            activeforeground="#ffffff",
            relief="flat",
            font=("Consolas", 9, "bold")
        ).pack(side="right", padx=6, pady=4)

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

        # The entry is disabled while waiting for acknowledgement, so its
        # widget-level binding cannot be the only way to receive Enter.
        # This binding also works if focus has moved elsewhere in the window.
        self.root.bind(
            "<Return>",
            self.handle_global_enter,
            add="+"
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

        if self.controller.interaction_paused:
            self.terminal.lock()

    def handle_global_enter(self, _=None):
        """Resume a locked interaction without submitting another command."""
        if not self.terminal.locked:
            return None

        self.continue_interaction()
        return "break"

    def continue_interaction(self):
        if not self.controller.interaction_paused:
            return

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
            self.controller.advance_realtime(2)

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

    def show_world_log(self):
        log_window = tk.Toplevel(self.root)
        log_window.title("Anomaly — World Log")
        log_window.geometry("620x380")
        log_window.configure(bg="#080a0d")
        output = tk.Text(
            log_window, bg="#080a0d", fg="#e7edf4", wrap="word",
            font=("Consolas", 10), relief="flat", state="normal"
        )
        output.pack(fill="both", expand=True, padx=10, pady=10)
        output.insert("end", "WORLD LOG\n\n")
        events = self.controller.state.world.recent_events(30)
        if events:
            for event in events:
                output.insert(
                    "end",
                    f"Day {event['day']} {event['hour']:02d}:{event['minute']:02d} — "
                    f"{event['text']}\n"
                )
        else:
            output.insert("end", "No recent world events have been recorded.\n")
        output.insert("end", "\nANOMALY STATUS: No anomaly has been noticed.\n")
        output.config(state="disabled")

    def close(self):
        if messagebox.askyesno(
            "Anomaly",
            "Exit the game?"
        ):
            self.root.destroy()

    def run(self):
        self.root.mainloop()
