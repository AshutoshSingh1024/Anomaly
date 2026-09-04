import tkinter as tk


class TerminalView(tk.Frame):
    def __init__(self, parent, on_command, on_continue):
        super().__init__(
            parent,
            bd=1,
            relief="sunken",
            bg="#0b0d10"
        )

        self.on_command = on_command
        self.on_continue = on_continue

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
            bg="#0b0d10"
        )

        bottom.pack(
            fill="x",
            padx=6,
            pady=(3, 6)
        )

        tk.Label(
            bottom,
            text=">",
            bg="#0b0d10",
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
            relief="flat",
            font=("Consolas", 11)
        )

        self.entry.pack(
            side="left",
            fill="x",
            expand=True
        )

        self.entry.bind(
            "<Return>",
            self.submit
        )

        self.enter_button = tk.Button(
            bottom,
            text="ENTER",
            command=self.continue_interaction,
            bg="#27313b",
            fg="#ffffff",
            activebackground="#3c4d5c",
            activeforeground="#ffffff",
            relief="flat",
            padx=14,
            pady=4,
            font=("Consolas", 9, "bold"),
            state="disabled"
        )

        self.enter_button.pack(
            side="left",
            padx=(8, 0)
        )

        self.status = tk.Label(
            self,
            text="READY",
            bg="#0b0d10",
            fg="#7dff9b",
            font=("Consolas", 8, "bold")
        )

        self.status.pack(
            anchor="e",
            padx=8,
            pady=(0, 4)
        )

        self.entry.focus_set()

    def submit(self, _=None):
        if str(self.entry["state"]) == "disabled":
            return "break"

        text = self.entry.get().strip()

        if text:
            self.entry.delete(0, "end")
            self.on_command(text)

        return "break"

    def lock(self):
        self.entry.config(state="disabled")

        self.enter_button.config(
            state="normal"
        )

        self.status.config(
            text="WAITING FOR ENTER",
            fg="#ffd166"
        )

    def unlock(self):
        self.entry.config(state="normal")

        self.enter_button.config(
            state="disabled"
        )

        self.status.config(
            text="READY",
            fg="#7dff9b"
        )

        self.entry.focus_set()

    def continue_interaction(self):
        self.on_continue()

    def refresh(self, text):
        self.output.config(state="normal")

        self.output.delete(
            "1.0",
            "end"
        )

        self.output.insert(
            "end",
            text
        )

        self.output.see("end")

        self.output.config(
            state="disabled"
        )