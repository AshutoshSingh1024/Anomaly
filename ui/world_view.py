import tkinter as tk
import math


class WorldView(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bd=1, relief="sunken", bg="#11151a")
        self.controller = controller
        self.canvas = tk.Canvas(self, bg="#11151a", highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)
        self.canvas.bind("<Configure>", self.draw)

    def refresh(self):
        self.draw()

    def draw(self, _=None):
        c = self.canvas
        c.delete("all")
        s = self.controller.state
        w = s.world
        p = s.player
        W = max(c.winfo_width(), 500)
        H = max(c.winfo_height(), 300)

        period = s.clock.period
        palette = {
            "morning": ("#a9c9e8", "#eaf4ff", "#56708a"),
            "afternoon": ("#8ec5e8", "#f7fcff", "#45657d"),
            "evening": ("#7c789b", "#f3c58d", "#594e72"),
            "night": ("#18233b", "#d7e4ff", "#7183a8"),
        }
        bg, fg, grid = palette[period]
        c.configure(bg=bg)
        c.create_rectangle(0, 0, W, H, fill=bg, outline=bg)

        # Header
        c.create_text(18, 14, anchor="nw", text="ANOMALY", fill=fg,
                      font=("Consolas", 14, "bold"))
        c.create_text(18, 36, anchor="nw", text=s.clock.display(), fill=fg,
                      font=("Consolas", 10))

        # Sun / moon
        body_x, body_y = W - 48, 38
        if s.clock.is_day:
            c.create_oval(body_x - 14, body_y - 14, body_x + 14, body_y + 14,
                          fill="#ffd86b", outline="#ffe9a6", width=2)
            c.create_text(W - 48, 65, text="SUN", fill=fg, font=("Consolas", 8, "bold"))
        else:
            c.create_oval(body_x - 13, body_y - 13, body_x + 13, body_y + 13,
                          fill="#e8edf7", outline="#ffffff", width=2)
            c.create_oval(body_x - 5, body_y - 14, body_x + 14, body_y + 4,
                          fill=bg, outline=bg)
            c.create_text(W - 48, 65, text="MOON", fill=fg, font=("Consolas", 8, "bold"))

        top = 78
        bottom = H - 48
        left = 20
        right = W - 20
        cell = max(min((right - left) / w.width, (bottom - top) / w.height), 16)
        grid_w = w.width * cell
        grid_h = w.height * cell
        gx = (W - grid_w) / 2
        gy = top + max(0, (bottom - top - grid_h) / 2)

        minx = 0
        miny = 0

        def pos(x, y):
            return gx + x * cell + cell / 2, gy + y * cell + cell / 2

        # Ground cells and coordinates
        for ix in range(w.width):
            for iy in range(w.height):
                x0 = gx + ix * cell
                y0 = gy + iy * cell
                world_x = ix
                world_y = iy
                fill = "#3c6b4a" if (world_x + world_y) % 5 else "#477754"
                if world_y == 0:
                    fill = "#9b845d"
                c.create_rectangle(x0, y0, x0 + cell, y0 + cell, fill=fill, outline=grid)

                # Coordinate labels, subtle but useful.
                if cell >= 19:
                    c.create_text(x0 + 3, y0 + 3, anchor="nw",
                                  text=f"{world_x},{world_y}", fill="#c8d4bd",
                                  font=("Consolas", max(5, int(cell * 0.18))))

        # Road
        for x in range(0, w.width):
            px, py = pos(x, 0)
            c.create_rectangle(px - cell / 2, py - cell / 2, px + cell / 2, py + cell / 2,
                               fill="#9b845d", outline=grid)

        symbols = {
            "house": ("H", "#f0d49a"),
            "tree": ("T", "#b7e08b"),
            "oak": ("O", "#a7dc7a"),
            "well": ("W", "#9dd8ff"),
            "bread": ("B", "#f2bd6b"),
            "shed": ("S", "#d4a37a"),
            "rock": ("R", "#b5bcc4"),
        }
        for o in w.objects.values():
            if o.hidden:
                continue
            x, y = pos(o.x, o.y)
            r = max(6, cell * .28)
            symbol, color = symbols.get(o.object_id, ("?", "#ffffff"))
            c.create_oval(x-r, y-r, x+r, y+r, fill="#182018", outline=color, width=2)
            c.create_text(x, y, text=symbol, fill=color,
                          font=("Consolas", max(8, int(cell*.28)), "bold"))

        for n in w.npcs.values():
            if not n.alive:
                continue
            x, y = pos(n.x, n.y)
            r = max(7, cell * .30)
            c.create_oval(x-r, y-r, x+r, y+r, fill="#263a4a", outline="#ffd28a", width=2)
            c.create_text(x, y, text="@", fill="#ffe3b0",
                          font=("Consolas", max(9, int(cell*.30)), "bold"))

        x, y = pos(p.x, p.y)
        r = max(9, cell * .34)
        c.create_oval(x-r, y-r, x+r, y+r, fill="#6d2838", outline="#ffffff", width=2)
        c.create_text(x, y, text="P", fill="#ffffff",
                      font=("Consolas", max(10, int(cell*.34)), "bold"))

        inv = ", ".join(p.inventory) if p.inventory else "empty"
        c.create_text(18, H-14, anchor="sw",
                      text=f"Position: ({p.x}, {p.y})    Inventory: {inv}    Grid coordinates: x,y",
                      fill=fg, font=("Consolas", 9))
