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
    home:tuple[int, int]=(0, 0)
    schedule:list[dict]=field(default_factory=list)
    memories:list[dict]=field(default_factory=list)
    current_activity:str="going about their business"
    current_schedule_key:str=""

    def remember(self, text, day, hour):
        self.memories.append({
            "text": text,
            "day": day,
            "hour": hour
        })
        self.memories = self.memories[-20:]

    def to_dict(self):
        data = self.__dict__.copy()
        data["home"] = list(self.home)
        return data

    @classmethod
    def from_dict(cls, d):
        data = dict(d)
        data["home"] = tuple(data.get("home", (data["x"], data["y"])))
        data.setdefault("schedule", [])
        data.setdefault("memories", [])
        data.setdefault("current_activity", "going about their business")
        data.setdefault("current_schedule_key", "")
        return cls(**data)
