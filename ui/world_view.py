import math
import tkinter as tk


class WorldView(tk.Frame):
    """Scrollable tile map with a fixed HUD layered above it."""

    SKY_STOPS = (
        "#101827", "#111c2b", "#17263a", "#263c55", "#466783",
        "#7fa9cb", "#afd2ec", "#b7d8ef", "#a9d6ed", "#99cfeb",
        "#8fc9ec", "#8fc9ec", "#93c9e7", "#9bb7d4", "#d18e63",
        "#806f91", "#4c5068", "#283244", "#172133", "#101827"
    )

    def __init__(self, parent, controller):
        super().__init__(parent, bd=1, relief="sunken", bg="#080a0d")
        self.controller = controller
        self.hover_text = None
        self.grid_geometry = None
        self.zoom = 1.0
        self.visible_tiles = 50
        self.camera_x = None
        self.camera_y = None

        self.header = tk.Canvas(self, height=78, bg="#101827", highlightthickness=0)
        self.header.pack(side="top", fill="x")
        self.status = tk.Label(self, anchor="w", padx=18, pady=4, bg="#101827", fg="#f3f6ff", font=("Consolas", 9, "bold"))
        self.status.pack(side="bottom", fill="x")

        map_area = tk.Frame(self, bg="#080a0d")
        map_area.pack(fill="both", expand=True)
        self.canvas = tk.Canvas(map_area, bg="#101827", highlightthickness=0)
        self.vertical_scroll = tk.Scrollbar(map_area, orient="vertical", command=self.scroll_y)
        self.horizontal_scroll = tk.Scrollbar(map_area, orient="horizontal", command=self.scroll_x)
        self.horizontal_scroll.pack(side="bottom", fill="x")
        self.vertical_scroll.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)

        self.canvas.bind("<Configure>", self.draw)
        self.canvas.bind("<Motion>", self.on_mouse_move)
        self.canvas.bind("<Leave>", self.on_mouse_leave)
        self.canvas.bind("<MouseWheel>", self.on_mouse_wheel)
        self.canvas.bind("<Shift-MouseWheel>", self.on_shift_mouse_wheel)
        self.canvas.bind("<Control-MouseWheel>", self.on_zoom_wheel)
        self.canvas.bind("<Home>", self.follow_player)

    @staticmethod
    def blend(first, second, amount):
        amount = max(0.0, min(1.0, amount))
        first_rgb = tuple(int(first[index:index + 2], 16) for index in (1, 3, 5))
        second_rgb = tuple(int(second[index:index + 2], 16) for index in (1, 3, 5))
        rgb = tuple(round(a + (b - a) * amount) for a, b in zip(first_rgb, second_rgb))
        return "#{:02x}{:02x}{:02x}".format(*rgb)

    def sky_color(self, clock):
        position = (clock.hour * 60 + clock.minute) / (24 * 60)
        scaled = position * len(self.SKY_STOPS)
        index = int(scaled) % len(self.SKY_STOPS)
        return self.blend(self.SKY_STOPS[index], self.SKY_STOPS[(index + 1) % len(self.SKY_STOPS)], scaled - int(scaled))

    @staticmethod
    def daylight(clock):
        hour = clock.hour + clock.minute / 60
        if not 5 <= hour <= 19:
            return 0.0
        return math.sin(math.pi * (hour - 5) / 14)

    def refresh(self):
        self.draw()

    def draw(self, _=None):
        state = self.controller.state
        sky = self.sky_color(state.clock)
        light = self.daylight(state.clock)
        colors = self.map_colors(sky, light, state.world.weather)
        self.draw_header(state, sky, light)
        self.draw_map(state.world, state.player, colors)
        self.draw_status(state.player, colors["bg"])

    def map_colors(self, sky, light, weather):
        ground = self.blend("#1c3529", "#347047", light)
        ground_alt = self.blend("#22402f", "#3e7d50", light)
        road = self.blend("#514d46", "#a48859", light)
        grid = self.blend("#314052", "#1d3025", light)
        weather_amount = {"cloudy": .18, "rain": .32, "storm": .48}.get(weather, 0)
        if weather_amount:
            sky = self.blend(sky, "#5d6875", weather_amount)
            ground = self.blend(ground, "#3c5053", weather_amount)
            ground_alt = self.blend(ground_alt, "#43595b", weather_amount)
        text = "#f3f6ff" if light < .55 else "#101820"
        label = "#d8f0dc" if light < .55 else "#17301e"
        return {"bg": sky, "ground": ground, "ground_alt": ground_alt, "road": road, "grid": grid, "text": text, "label": label}

    def draw_header(self, state, sky, light):
        header = self.header
        header.delete("all")
        width = max(header.winfo_width(), 500)
        header.configure(bg=sky)
        header.create_rectangle(0, 0, width, 78, fill=sky, outline=sky)
        text = "#f3f6ff" if light < .55 else "#101820"
        header.create_text(18, 14, anchor="nw", text="ANOMALY", fill=text, font=("Consolas", 15, "bold"))
        running = "RUNNING" if self.controller.time_running else "STOPPED"
        header.create_text(18, 38, anchor="nw", text=f"{state.clock.display()}  |  {running}  |  SPEED {self.controller.time_speed_display()}  |  WEATHER {state.world.weather.upper()}", fill=text, font=("Consolas", 10, "bold"))

        body_x, body_y = width - 48, 36
        moon_visibility = 1 - light
        sun_radius, moon_radius = 15 * light, 14 * moon_visibility
        if moon_radius > 1:
            moon = self.blend(sky, "#f0f4ff", moon_visibility)
            header.create_oval(body_x - moon_radius, body_y - moon_radius, body_x + moon_radius, body_y + moon_radius, fill=moon, outline=self.blend(sky, "#ffffff", moon_visibility), width=2)
            header.create_oval(body_x - moon_radius * .25, body_y - moon_radius, body_x + moon_radius, body_y + moon_radius * .25, fill=sky, outline=sky)
        if sun_radius > 1:
            sun = self.blend(sky, "#ffe066", light)
            header.create_oval(body_x - sun_radius, body_y - sun_radius, body_x + sun_radius, body_y + sun_radius, fill=sun, outline=self.blend(sky, "#fff4b3", light), width=2)
        header.create_text(body_x, 66, text="SUN" if light >= .5 else "MOON", fill=text, font=("Consolas", 8, "bold"))

    def draw_map(self, world, player, colors):
        canvas = self.canvas
        canvas.delete("all")
        width, height = max(canvas.winfo_width(), 500), max(canvas.winfo_height(), 260)
        visible = min(70, max(12, round(self.visible_tiles / self.zoom)))
        cell = min((width - 20) / visible, (height - 20) / visible)
        center_x = player.x if self.camera_x is None else self.camera_x
        center_y = player.y if self.camera_y is None else self.camera_y
        start_x = max(0, min(world.width - visible, center_x - visible // 2))
        start_y = max(0, min(world.height - visible, center_y - visible // 2))
        self.horizontal_scroll.set(start_x / world.width, (start_x + visible) / world.width)
        self.vertical_scroll.set(start_y / world.height, (start_y + visible) / world.height)
        gx = (width - visible * cell) / 2
        gy = (height - visible * cell) / 2
        self.grid_geometry = (gx, gy, cell, visible, visible, start_x, start_y)
        canvas.configure(bg=colors["bg"], scrollregion=(0, 0, width, height))
        canvas.create_rectangle(0, 0, width, height, fill=colors["bg"], outline=colors["bg"])

        for x in range(start_x, start_x + visible):
            for y in range(start_y, start_y + visible):
                x0, y0 = gx + x * cell, gy + y * cell
                x0, y0 = gx + (x - start_x) * cell, gy + (y - start_y) * cell
                fill, texture = self.region_style(world.region_at(x, y), colors)
                if y == 0 and x < 80:
                    fill, texture = colors["road"], "road"
                canvas.create_rectangle(x0, y0, x0 + cell + .5, y0 + cell + .5, fill=fill, outline=fill)
                self.draw_texture(x0, y0, cell, texture, fill)
                if cell >= 19:
                    canvas.create_text(x0 + 3, y0 + 3, anchor="nw", text=f"{x},{y}", fill=colors["label"], font=("Consolas", max(5, int(cell * .18)), "bold"))

        if world.weather in ("rain", "storm"):
            for index in range(36):
                x, y = (index * 79 + 31) % int(width), (index * 47 + 19) % int(height)
                canvas.create_line(x, y, x - 3, y + 8, fill="#8fc9ec", width=1)

        symbols = {"house": ("H", "#ffe09a"), "tree": ("T", "#a8e67d"), "oak": ("O", "#8fdc68"), "well": ("W", "#79d8ff"), "bread": ("B", "#ffc766"), "shed": ("S", "#e0aa7b"), "rock": ("R", "#d2d8df")}
        for obj in world.objects.values():
            if not obj.hidden:
                self.draw_marker(obj.x, obj.y, cell, gx, gy, symbols.get(obj.object_id, ("?", "#ffffff")), .28)
        for npc in world.npcs.values():
            if npc.alive:
                self.draw_marker(npc.x, npc.y, cell, gx, gy, ("@", "#ffe6ae"), .30)
        self.draw_marker(player.x, player.y, cell, gx, gy, ("P", "#ffffff"), .34, "#7f263e")

    def region_style(self, region, colors):
        styles = {
            "village": (colors["ground"], "grass"),
            "plains": ("#4e8a53", "grass"),
            "forest": ("#315f3c", "leaves"),
            "highlands": ("#697277", "stone"),
            "marsh": ("#476e5b", "marsh"),
            "lake": ("#3d7faa", "water")
        }
        return styles[region]

    def draw_texture(self, x, y, cell, texture, fill):
        if cell < 7:
            return
        canvas = self.canvas
        if texture == "water":
            canvas.create_line(x + cell * .15, y + cell * .42, x + cell * .5, y + cell * .42, fill="#8fc9ec")
            canvas.create_line(x + cell * .55, y + cell * .65, x + cell * .85, y + cell * .65, fill="#8fc9ec")
        elif texture == "leaves":
            canvas.create_oval(x + cell * .25, y + cell * .25, x + cell * .5, y + cell * .5, fill="#527c43", outline="")
            canvas.create_oval(x + cell * .55, y + cell * .55, x + cell * .78, y + cell * .78, fill="#274e32", outline="")
        elif texture == "stone":
            canvas.create_line(x + cell * .15, y + cell * .25, x + cell * .8, y + cell * .75, fill="#8e9697")
        elif texture == "marsh":
            canvas.create_line(x + cell * .3, y + cell * .25, x + cell * .3, y + cell * .72, fill="#7c9f60")
            canvas.create_line(x + cell * .6, y + cell * .35, x + cell * .6, y + cell * .8, fill="#7c9f60")
        elif texture == "road":
            canvas.create_line(x, y + cell * .72, x + cell, y + cell * .72, fill="#b49664")
        else:
            canvas.create_oval(x + cell * .2, y + cell * .2, x + cell * .3, y + cell * .3, fill="#74a95c", outline="")

    def draw_marker(self, x, y, cell, gx, gy, symbol_data, ratio, fill="#111820"):
        _, _, _, visible_x, visible_y, start_x, start_y = self.grid_geometry
        if not (start_x <= x < start_x + visible_x and start_y <= y < start_y + visible_y):
            return
        px = gx + (x - start_x) * cell + cell / 2
        py = gy + (y - start_y) * cell + cell / 2
        symbol, color = symbol_data
        radius = max(6, cell * ratio)
        self.canvas.create_oval(px - radius, py - radius, px + radius, py + radius, fill=fill, outline=color, width=2)
        self.canvas.create_text(px, py, text=symbol, fill=color, font=("Consolas", max(8, int(cell * ratio)), "bold"))

    def draw_status(self, player, background):
        inventory = ", ".join(player.inventory) if player.inventory else "empty"
        hover = self.hover_text or "Wheel pans; Shift + wheel pans sideways; Ctrl + wheel zooms; Home follows player."
        foreground = "#f3f6ff" if self.daylight(self.controller.state.clock) < .55 else "#101820"
        self.status.config(text=f"Position: ({player.x}, {player.y})    Inventory: {inventory}    |    {hover}", bg=background, fg=foreground)

    def get_tile_from_mouse(self, mouse_x, mouse_y):
        if not self.grid_geometry:
            return None
        gx, gy, cell, width, height, start_x, start_y = self.grid_geometry
        mouse_x, mouse_y = self.canvas.canvasx(mouse_x), self.canvas.canvasy(mouse_y)
        world_x, world_y = int((mouse_x - gx) // cell), int((mouse_y - gy) // cell)
        return (world_x + start_x, world_y + start_y) if 0 <= world_x < width and 0 <= world_y < height else None

    def on_mouse_move(self, event):
        tile = self.get_tile_from_mouse(event.x, event.y)
        if tile is None:
            self.hover_text = None
            return
        self.hover_text = f"Tile: ({tile[0]}, {tile[1]})"
        self.draw_status(
            self.controller.state.player,
            self.map_colors(
                self.sky_color(self.controller.state.clock),
                self.daylight(self.controller.state.clock),
                self.controller.state.world.weather
            )["bg"]
        )
        self.canvas.delete("hover")
        gx, gy, cell, _, _, start_x, start_y = self.grid_geometry
        x0, y0 = gx + (tile[0] - start_x) * cell, gy + (tile[1] - start_y) * cell
        self.canvas.create_rectangle(x0, y0, x0 + cell, y0 + cell, outline="#ffffff", width=2, tags="hover")

    def on_mouse_leave(self, _):
        self.hover_text = None
        self.canvas.delete("hover")
        self.draw_status(
            self.controller.state.player,
            self.map_colors(
                self.sky_color(self.controller.state.clock),
                self.daylight(self.controller.state.clock),
                self.controller.state.world.weather
            )["bg"]
        )

    def on_mouse_wheel(self, event):
        self.pan_camera(0, -int(event.delta / 120) * 3)
        return "break"

    def on_shift_mouse_wheel(self, event):
        self.pan_camera(-int(event.delta / 120) * 3, 0)
        return "break"

    def on_zoom_wheel(self, event):
        self.zoom = min(3.0, max(.5, self.zoom * (1.15 if event.delta > 0 else 1 / 1.15)))
        self.draw()
        return "break"

    def pan_camera(self, delta_x, delta_y):
        player = self.controller.state.player
        self.camera_x = max(0, min(self.controller.state.world.width - 1, (self.camera_x if self.camera_x is not None else player.x) + delta_x))
        self.camera_y = max(0, min(self.controller.state.world.height - 1, (self.camera_y if self.camera_y is not None else player.y) + delta_y))
        self.draw()

    def scroll_x(self, *args):
        self.scroll_camera("x", *args)

    def scroll_y(self, *args):
        self.scroll_camera("y", *args)

    def scroll_camera(self, axis, *args):
        world = self.controller.state.world
        if args[0] == "moveto":
            target = float(args[1]) * (world.width - 1 if axis == "x" else world.height - 1)
            if axis == "x":
                self.camera_x = target
            else:
                self.camera_y = target
        else:
            amount = int(args[1]) * 3
            self.pan_camera(amount if axis == "x" else 0, amount if axis == "y" else 0)
            return
        self.draw()

    def follow_player(self, _=None):
        self.camera_x = None
        self.camera_y = None
        self.draw()
        return "break"
