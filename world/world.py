from dataclasses import dataclass, field
from world.objects import WorldObject, Location
from world.npc import NPC
from world.player import Player

@dataclass
class World:
    width:int=15
    height:int=11
    objects:dict=field(default_factory=dict)
    locations:dict=field(default_factory=dict)
    npcs:dict=field(default_factory=dict)
    weather:str="clear"
    event_log:list[dict]=field(default_factory=list)
    def create_player(self): return Player()
    def object_at(self,x,y): return [o for o in self.objects.values() if not o.hidden and (o.x,o.y)==(x,y)]
    def npc_at(self,x,y): return [n for n in self.npcs.values() if n.alive and (n.x,n.y)==(x,y)]
    def find_object(self,name):
        q=name.lower().strip()
        return next((o for o in self.objects.values() if not o.hidden and (o.name.lower()==q or o.object_id.lower()==q)),None)
    def find_npc(self,name):
        q=name.lower().strip()
        return next((n for n in self.npcs.values() if n.name.lower()==q or n.npc_id.lower()==q),None)
    def nearby_description(self,p):
        parts=[l.name for l in self.locations.values() if l.contains(p.x,p.y)]
        parts += [o.name for o in self.object_at(p.x,p.y)]
        parts += [f"{n.name} ({n.current_activity})" for n in self.npc_at(p.x,p.y)]
        return "Nearby: "+", ".join(parts) if parts else "Nothing obvious is here."

    def tick(self,state):
        clock = state.clock
        if clock.minute % 10:
            return

        self._update_weather(clock)

        for npc in self.npcs.values():
            if not npc.alive:
                continue
            target, activity, schedule_key = self._routine_for(npc, clock)

            if schedule_key != npc.current_schedule_key:
                npc.current_schedule_key = schedule_key
                npc.current_activity = activity
                self.record_event(
                    f"{npc.name} begins {activity}.",
                    clock,
                    "routine",
                    npc.npc_id
                )

            self._move_toward(npc, target)

    def _routine_for(self, npc, clock):
        entry = None
        for candidate in npc.schedule:
            if candidate["start"] <= clock.hour:
                entry = candidate

        if entry is None and npc.schedule:
            entry = npc.schedule[-1]

        if entry is None:
            return npc.home, "returning home", "home"

        target = tuple(entry["target"])
        activity = entry["activity"]

        if self.weather in ("rain", "storm") and entry.get("shelter", True):
            target = npc.home
            activity = "sheltering from the rain"
            schedule_key = f"{entry['key']}:{self.weather}"
        else:
            schedule_key = entry["key"]

        return target, activity, schedule_key

    @staticmethod
    def _move_toward(npc, target):
        target_x, target_y = target
        if npc.x != target_x:
            npc.x += 1 if target_x > npc.x else -1
        elif npc.y != target_y:
            npc.y += 1 if target_y > npc.y else -1

    def _update_weather(self, clock):
        if clock.minute != 0 or clock.hour not in (0, 6, 12, 18):
            return

        weather_cycle = ("clear", "cloudy", "rain", "clear", "windy", "storm")
        next_weather = weather_cycle[(clock.day * 4 + clock.hour // 6) % len(weather_cycle)]
        if next_weather == self.weather:
            return

        self.weather = next_weather
        descriptions = {
            "clear": "The clouds break apart and the sky clears.",
            "cloudy": "A flat blanket of cloud passes over the settlement.",
            "rain": "Rain begins to fall across the road and fields.",
            "windy": "A restless wind stirs the trees and loose doors.",
            "storm": "A distant storm rolls over the settlement."
        }
        self.record_event(descriptions[next_weather], clock, "weather")

    def record_event(self, text, clock, kind="world", subject=None):
        event = {
            "text": text,
            "day": clock.day,
            "hour": clock.hour,
            "minute": clock.minute,
            "kind": kind,
            "subject": subject
        }
        self.event_log.append(event)
        self.event_log = self.event_log[-60:]

        for npc in self.npcs.values():
            if not npc.alive:
                continue
            if subject == npc.npc_id or abs(npc.x - self.width // 2) <= 12:
                npc.remember(text, clock.day, clock.hour)

    def recent_events(self, limit=8):
        return self.event_log[-limit:]
    def to_dict(self):
        return {"width":self.width,"height":self.height,
                "objects":{k:v.to_dict() for k,v in self.objects.items()},
                "locations":{k:v.to_dict() for k,v in self.locations.items()},
                "npcs":{k:v.to_dict() for k,v in self.npcs.items()},
                "weather": self.weather,
                "event_log": list(self.event_log)}
    @classmethod
    def from_dict(cls,d):
        w=cls(int(d.get("width",15)),int(d.get("height",11)))
        w.objects={k:WorldObject.from_dict(v) for k,v in d.get("objects",{}).items()}
        w.locations={k:Location.from_dict(v) for k,v in d.get("locations",{}).items()}
        w.npcs={k:NPC.from_dict(v) for k,v in d.get("npcs",{}).items()}
        w.weather=d.get("weather", "clear")
        w.event_log=list(d.get("event_log", []))
        return w
