import tkinter as tk


class WorldView(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(
            parent,
            bd=1,
            relief="sunken",
            bg="#080a0d"
        )

        self.controller = controller

        self.canvas = tk.Canvas(
            self,
            bg="#080a0d",
            highlightthickness=0
        )

        self.canvas.pack(
            fill="both",
            expand=True
        )

        self.canvas.bind(
            "<Configure>",
            self.draw
        )

        self.canvas.bind(
            "<Motion>",
            self.on_mouse_move
        )

        self.canvas.bind(
            "<Leave>",
            self.on_mouse_leave
        )

        self.grid_geometry = None

        self.hover_text = None

    def refresh(self):
        self.draw()

    def draw(self, _=None):
        c = self.canvas
        c.delete("all")

        s = self.controller.state
        w = s.world
        p = s.player

        W = max(
            c.winfo_width(),
            500
        )

        H = max(
            c.winfo_height(),
            300
        )

        period = s.clock.period

        palette = {
            "morning": {
                "bg": "#b7d8ef",
                "ground": "#3f754f",
                "ground_alt": "#477f57",
                "road": "#9f8457",
                "grid": "#25342a",
                "text": "#101820"
            },

            "afternoon": {
                "bg": "#8fc9ec",
                "ground": "#347047",
                "ground_alt": "#3e7d50",
                "road": "#a48859",
                "grid": "#1d3025",
                "text": "#0b1115"
            },

            "evening": {
                "bg": "#806f91",
                "ground": "#46505d",
                "ground_alt": "#515b68",
                "road": "#95775b",
                "grid": "#252a32",
                "text": "#ffffff"
            },

            "night": {
                "bg": "#101827",
                "ground": "#1c3529",
                "ground_alt": "#22402f",
                "road": "#514d46",
                "grid": "#314052",
                "text": "#f3f6ff"
            }
        }

        colors = palette[period]

        bg = colors["bg"]
        ground = colors["ground"]
        ground_alt = colors["ground_alt"]
        road = colors["road"]
        grid = colors["grid"]
        text = colors["text"]

        c.configure(bg=bg)

        c.create_rectangle(
            0,
            0,
            W,
            H,
            fill=bg,
            outline=bg
        )

        # Header
        c.create_text(
            18,
            14,
            anchor="nw",
            text="ANOMALY",
            fill=text,
            font=("Consolas", 15, "bold")
        )

        clock_text = s.clock.display()

        if self.controller.time_running:
            clock_text += "  |  RUNNING"
        else:
            clock_text += "  |  STOPPED"

        c.create_text(
            18,
            38,
            anchor="nw",
            text=clock_text,
            fill=text,
            font=("Consolas", 10, "bold")
        )

        # Sun / moon
        body_x = W - 48
        body_y = 38

        if s.clock.is_day:
            c.create_oval(
                body_x - 15,
                body_y - 15,
                body_x + 15,
                body_y + 15,
                fill="#ffe066",
                outline="#fff4b3",
                width=2
            )

            c.create_text(
                W - 48,
                66,
                text="SUN",
                fill=text,
                font=("Consolas", 8, "bold")
            )

        else:
            c.create_oval(
                body_x - 14,
                body_y - 14,
                body_x + 14,
                body_y + 14,
                fill="#f0f4ff",
                outline="#ffffff",
                width=2
            )

            c.create_oval(
                body_x - 6,
                body_y - 15,
                body_x + 14,
                body_y + 5,
                fill=bg,
                outline=bg
            )

            c.create_text(
                W - 48,
                66,
                text="MOON",
                fill=text,
                font=("Consolas", 8, "bold")
            )

        top = 78
        bottom = H - 48
        left = 20
        right = W - 20

        cell = max(
            min(
                (right - left) / w.width,
                (bottom - top) / w.height
            ),
            16
        )

        grid_w = w.width * cell
        grid_h = w.height * cell

        gx = (W - grid_w) / 2
        gy = top + max(
            0,
            (bottom - top - grid_h) / 2
        )

        self.grid_geometry = (
            gx,
            gy,
            cell,
            w.width,
            w.height
        )

        def pos(x, y):
            return (
                gx + x * cell + cell / 2,
                gy + y * cell + cell / 2
            )

        # Ground
        for ix in range(w.width):
            for iy in range(w.height):
                x0 = gx + ix * cell
                y0 = gy + iy * cell

                fill = (
                    ground_alt
                    if (ix + iy) % 5 == 0
                    else ground
                )

                if iy == 0:
                    fill = road

                c.create_rectangle(
                    x0,
                    y0,
                    x0 + cell,
                    y0 + cell,
                    fill=fill,
                    outline=grid
                )

                # Coordinate labels
                if cell >= 19:
                    label_color = (
                        "#d8f0dc"
                        if period in ("night", "evening")
                        else "#17301e"
                    )

                    c.create_text(
                        x0 + 3,
                        y0 + 3,
                        anchor="nw",
                        text=f"{ix},{iy}",
                        fill=label_color,
                        font=(
                            "Consolas",
                            max(5, int(cell * 0.18)),
                            "bold"
                        )
                    )

        # Road
        for x in range(w.width):
            px, py = pos(x, 0)

            c.create_rectangle(
                px - cell / 2,
                py - cell / 2,
                px + cell / 2,
                py + cell / 2,
                fill=road,
                outline=grid
            )

        symbols = {
            "house": ("H", "#ffe09a"),
            "tree": ("T", "#a8e67d"),
            "oak": ("O", "#8fdc68"),
            "well": ("W", "#79d8ff"),
            "bread": ("B", "#ffc766"),
            "shed": ("S", "#e0aa7b"),
            "rock": ("R", "#d2d8df"),
        }

        # Objects
        for o in w.objects.values():
            if o.hidden:
                continue

            x, y = pos(
                o.x,
                o.y
            )

            r = max(
                6,
                cell * 0.28
            )

            symbol, color = symbols.get(
                o.object_id,
                ("?", "#ffffff")
            )

            c.create_oval(
                x - r,
                y - r,
                x + r,
                y + r,
                fill="#111820",
                outline=color,
                width=2
            )

            c.create_text(
                x,
                y,
                text=symbol,
                fill=color,
                font=(
                    "Consolas",
                    max(8, int(cell * 0.28)),
                    "bold"
                )
            )

        # NPCs
        for n in w.npcs.values():
            if not n.alive:
                continue

            x, y = pos(
                n.x,
                n.y
            )

            r = max(
                7,
                cell * 0.30
            )

            c.create_oval(
                x - r,
                y - r,
                x + r,
                y + r,
                fill="#142433",
                outline="#ffd166",
                width=2
            )

            c.create_text(
                x,
                y,
                text="@",
                fill="#ffe6ae",
                font=(
                    "Consolas",
                    max(9, int(cell * 0.30)),
                    "bold"
                )
            )

        # Player
        x, y = pos(
            p.x,
            p.y
        )

        r = max(
            9,
            cell * 0.34
        )

        c.create_oval(
            x - r,
            y - r,
            x + r,
            y + r,
            fill="#7f263e",
            outline="#ffffff",
            width=2
        )

        c.create_text(
            x,
            y,
            text="P",
            fill="#ffffff",
            font=(
                "Consolas",
                max(10, int(cell * 0.34)),
                "bold"
            )
        )

        # Bottom status
        inv = (
            ", ".join(p.inventory)
            if p.inventory
            else "empty"
        )

        hover = (
            self.hover_text
            if self.hover_text
            else "Hover over a tile for coordinates."
        )

        c.create_text(
            18,
            H - 14,
            anchor="sw",
            text=(
                f"Position: ({p.x}, {p.y})    "
                f"Inventory: {inv}    "
                f"|    {hover}"
            ),
            fill=text,
            font=("Consolas", 9, "bold")
        )

    def get_tile_from_mouse(self, mouse_x, mouse_y):
        if not self.grid_geometry:
            return None

        gx, gy, cell, width, height = self.grid_geometry

        world_x = int(
            (mouse_x - gx) // cell
        )

        world_y = int(
            (mouse_y - gy) // cell
        )

        if not (
            0 <= world_x < width
            and 0 <= world_y < height
        ):
            return None

        return world_x, world_y

    def on_mouse_move(self, event):
        tile = self.get_tile_from_mouse(
            event.x,
            event.y
        )

        if tile is None:
            self.hover_text = None
            return

        x, y = tile

        self.hover_text = (
            f"Tile: ({x}, {y})"
        )

        self.draw()

        # Highlight the hovered tile.
        if self.grid_geometry:
            gx, gy, cell, _, _ = self.grid_geometry

            x0 = gx + x * cell
            y0 = gy + y * cell

            self.canvas.create_rectangle(
                x0,
                y0,
                x0 + cell,
                y0 + cell,
                outline="#ffffff",
                width=2
            )

    def on_mouse_leave(self, _):
        self.hover_text = None
        self.draw()