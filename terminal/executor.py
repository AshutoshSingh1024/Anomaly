from terminal.commands import CommandResult

class CommandExecutor:
    def __init__(self, controller):
        self.controller = controller

    @property
    def state(self): return self.controller.state
    @property
    def world(self): return self.state.world
    @property
    def player(self): return self.state.player

    def result(self, text, consumes_time=False, quit_requested=False):
        return CommandResult(text, consumes_time, quit_requested)

    def execute(self, command):
        handlers = {
            "help": self.help, "look": self.look, "observe": self.look,
            "move": self.move, "go": self.move, "walk": self.move,
            "find": self.find, "search": self.find,
            "inspect": self.inspect, "examine": self.inspect,
            "take": self.take, "get": self.take, "pick": self.take,
            "drop": self.drop, "eat": self.eat, "drink": self.drink,
            "talk": self.talk, "speak": self.talk, "wait": self.wait,
            "clear": self.clear, "save": self.save, "load": self.load,
            "quit": self.quit, "exit": self.quit
        }
        fn = handlers.get(command.name)
        return fn(command.arguments) if fn else self.result(
            f"Unknown command: {command.name!r}. Type 'help'.", False)

    def help(self, _):
        text = (
            "Commands:\n"
            "  look / observe\n"
            "  move north|south|east|west\n"
            "  find <thing>\n"
            "  inspect <thing>\n"
            "  take <thing>\n"
            "  drop <thing>\n"
            "  eat <thing>\n"
            "  drink <thing>\n"
            "  talk <person>\n"
            "  wait\n"
            "  save / load\n"
            "  clear\n"
            "  quit"
        )
        return self.result(text, False)

    def look(self, _):
        return self.result(f"You are at ({self.player.x}, {self.player.y}).\n{self.world.nearby_description(self.player)}")

    def move(self, args):
        if not args: return self.result("Move where? north, south, east or west.", False)
        dirs = {"north":(0,-1),"south":(0,1),"east":(1,0),"west":(-1,0),"n":(0,-1),"s":(0,1),"e":(1,0),"w":(-1,0)}
        if args[0].lower() not in dirs: return self.result("That is not a valid direction.", False)
        dx,dy = dirs[args[0].lower()]
        nx,ny = self.player.x+dx,self.player.y+dy
        if abs(nx)>self.world.width//2 or abs(ny)>self.world.height//2:
            return self.result("You cannot go that way.", False)
        self.player.move(dx,dy)
        return self.result(f"You move {args[0]} to ({nx}, {ny}).\n{self.world.nearby_description(self.player)}")

    def find(self, args):
        if not args: return self.result("Find what?", False)
        q=" ".join(args); obj=self.world.find_object(q); npc=self.world.find_npc(q)
        if obj: return self.result(f"You know where the {obj.name} is: ({obj.x}, {obj.y}).")
        if npc: return self.result(f"{npc.name} is at ({npc.x}, {npc.y}).")
        return self.result(f"You cannot find {q!r}.")

    def inspect(self, args):
        if not args: return self.result("Inspect what?", False)
        q=" ".join(args); obj=self.world.find_object(q)
        if obj:
            if (obj.x,obj.y)!=(self.player.x,self.player.y): return self.result(f"The {obj.name} is not close enough to inspect.")
            return self.result(obj.description)
        npc=self.world.find_npc(q)
        if npc:
            if (npc.x,npc.y)!=(self.player.x,self.player.y): return self.result(f"{npc.name} is not close enough to inspect.")
            return self.result(npc.description)
        return self.result(f"You do not see {q!r}.")

    def take(self,args):
        if not args: return self.result("Take what?",False)
        obj=self.world.find_object(" ".join(args))
        if not obj: return self.result("You cannot find that.",False)
        if not obj.portable: return self.result(f"You cannot take the {obj.name}.",False)
        if (obj.x,obj.y)!=(self.player.x,self.player.y): return self.result(f"The {obj.name} is not here.",False)
        if obj.object_id in self.player.inventory: return self.result("You already have that.",False)
        self.player.inventory.append(obj.object_id); obj.hidden=True
        return self.result(f"You take the {obj.name}.")

    def drop(self,args):
        if not args: return self.result("Drop what?",False)
        obj=self.world.find_object(" ".join(args))
        if not obj or obj.object_id not in self.player.inventory: return self.result("You are not carrying that.",False)
        self.player.inventory.remove(obj.object_id); obj.x,obj.y=self.player.x,self.player.y; obj.hidden=False
        return self.result(f"You drop the {obj.name}.")

    def eat(self,args):
        if not args: return self.result("Eat what?",False)
        obj=self.world.find_object(" ".join(args))
        if not obj or obj.object_id not in self.player.inventory: return self.result("You are not carrying that.",False)
        if not obj.edible: return self.result(f"You cannot eat the {obj.name}.",False)
        self.player.inventory.remove(obj.object_id)
        return self.result(f"You eat the {obj.name}.")

    def drink(self,args):
        if not args: args=["water"]
        if " ".join(args).lower() in ("water","well"):
            well=self.world.find_object("well")
            if well and (well.x,well.y)==(self.player.x,self.player.y): return self.result("You drink cold water from the well.")
            return self.result("There is no water here.")
        return self.result("You cannot drink that.",False)

    def talk(self,args):
        if not args: return self.result("Talk to whom?",False)
        npc=self.world.find_npc(" ".join(args))
        if not npc: return self.result("You cannot find that person.",False)
        if (npc.x,npc.y)!=(self.player.x,self.player.y): return self.result(f"{npc.name} is not here.",False)
        return self.result("\n".join(npc.dialogue))

    def wait(self,_): return self.result("You wait.")
    def clear(self,_):
        self.controller.messages.clear()
        return self.result("Terminal cleared.",False)
    def save(self,_):
        self.controller.save()
        return self.result("Game saved to saves/save.json.",False)
    def load(self,_):
        from pathlib import Path
        if not Path("saves/save.json").exists(): return self.result("No save file exists.",False)
        try:
            self.controller.load(); return self.result("Game loaded.",False)
        except (OSError,ValueError,TypeError) as e: return self.result(f"Could not load save: {e}",False)
    def quit(self,_): return self.result("Closing Anomaly.",False,True)
