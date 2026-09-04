from dataclasses import dataclass, field

@dataclass
class NPC:
    npc_id:str
    name:str
    x:int
    y:int
    description:str
    dialogue:list[str]=field(default_factory=list)
    alive:bool=True
    def to_dict(self): return self.__dict__.copy()
    @classmethod
    def from_dict(cls,d): return cls(**d)
