import tkinter as tk


class TerminalView(tk.Frame):
    def __init__(self, parent, on_command, on_continue):
        super().__init__(
            parent,
            bd=1,
            relief="sunken",
            bg="#080a0d"
        )

        self.on_command = on_command
        self.on_continue = on_continue

        self.locked = False

        self.output = tk.Text(
            self,
            height=12,
            wrap="word",
            bg="#080a0d",
            fg="#f2f4f7",
            insertbackground="#ffffff",
            selectbackground="#3d5870",
            font=("Consolas", 10),
            state="disabled",
            relief="flat"
        )

        self.output.pack(
            fill="both",
            expand=True,
            padx=6,
            pady=(6, 3)
        )

        bottom = tk.Frame(
            self,
            bg="#080a0d"
        )

        bottom.pack(
            fill="x",
            padx=6,
            pady=(3, 6)
        )

        tk.Label(
            bottom,
            text=">",
            bg="#080a0d",
            fg="#ffffff",
            font=("Consolas", 11, "bold")
        ).pack(
            side="left",
            padx=(0, 6)
        )

        self.entry = tk.Entry(
            bottom,
            bg="#11151a",
            fg="#ffffff",
            insertbackground="#ffffff",
            selectbackground="#3d5870",
            disabledbackground="#0b0d10",
            disabledforeground="#555b63",
            relief="flat",
            font=("Consolas", 11)
        )

        self.entry.pack(
            side="left",
            fill="x",
            expand=True
        )

        # Physical keyboard Enter.
        self.entry.bind(
            "<Return>",
            self.handle_enter
        )

        self.status = tk.Label(
            self,
            text="READY",
            bg="#080a0d",
            fg="#7dff9b",
            font=("Consolas", 8, "bold")
        )

        self.status.pack(
            anchor="e",
            padx=8,
            pady=(0, 4)
        )

        self.entry.focus_set()

    def handle_enter(self, _=None):
        if self.locked:
            self.on_continue()
            return "break"

        self.submit()
        return "break"

    def submit(self):
        text = self.entry.get().strip()

        if not text:
            return

        self.entry.delete(
            0,
            "end"
        )

        self.on_command(text)

    def lock(self):
        self.locked = True

        self.entry.config(
            state="disabled"
        )

        self.status.config(
            text="PAUSED • PRESS ENTER",
            fg="#ffd166"
        )

    def unlock(self):
        self.locked = False

        self.entry.config(
            state="normal"
        )

        self.status.config(
            text="READY",
            fg="#7dff9b"
        )

        self.entry.focus_set()

    def refresh(self, text):
        self.output.config(
            state="normal"
        )

        self.output.delete(
            "1.0",
            "end"
        )

        self.output.insert(
            "end",
            text
        )

        self.output.see(
            "end"
        )

        self.output.config(
            state="disabled"
        )