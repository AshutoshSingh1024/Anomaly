from dataclasses import dataclass, field

@dataclass
class WorldObject:
    object_id:str
    name:str
    x:int
    y:int
    description:str
    portable:bool=False
    edible:bool=False
    drinkable:bool=False
    hidden:bool=False
    def to_dict(self): return self.__dict__.copy()
    @classmethod
    def from_dict(cls,d): return cls(**d)

@dataclass
class Location:
    location_id:str
    name:str
    x:int
    y:int
    description:str
    radius:int=1
    tags:set[str]=field(default_factory=set)
    def contains(self,x,y): return abs(self.x-x)<=self.radius and abs(self.y-y)<=self.radius
    def to_dict(self): return {**self.__dict__, "tags":sorted(self.tags)}
    @classmethod
    def from_dict(cls,d):
        d=dict(d); d["tags"]=set(d.get("tags",[])); return cls(**d)
