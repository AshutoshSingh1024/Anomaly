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
        parts += [n.name for n in self.npc_at(p.x,p.y)]
        return "Nearby: "+", ".join(parts) if parts else "Nothing obvious is here."
    def tick(self,state):
        pass
    def to_dict(self):
        return {"width":self.width,"height":self.height,
                "objects":{k:v.to_dict() for k,v in self.objects.items()},
                "locations":{k:v.to_dict() for k,v in self.locations.items()},
                "npcs":{k:v.to_dict() for k,v in self.npcs.items()}}
    @classmethod
    def from_dict(cls,d):
        w=cls(int(d.get("width",15)),int(d.get("height",11)))
        w.objects={k:WorldObject.from_dict(v) for k,v in d.get("objects",{}).items()}
        w.locations={k:Location.from_dict(v) for k,v in d.get("locations",{}).items()}
        w.npcs={k:NPC.from_dict(v) for k,v in d.get("npcs",{}).items()}
        return w
