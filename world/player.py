from dataclasses import dataclass, field

@dataclass
class Player:
    x:int=0
    y:int=0
    inventory:list[str]=field(default_factory=list)
    def move(self,dx,dy): self.x+=dx; self.y+=dy
    def to_dict(self): return {"x":self.x,"y":self.y,"inventory":list(self.inventory)}
    @classmethod
    def from_dict(cls,d): return cls(int(d.get("x",0)),int(d.get("y",0)),list(d.get("inventory",[])))
