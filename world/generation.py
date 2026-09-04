from world.world import World
from world.objects import WorldObject, Location
from world.npc import NPC

def create_initial_world():
    w=World()
    w.locations["village"]=Location("village","Village",0,0,"A small settlement connected by an old road.",4,{"settlement"})
    w.objects["house"]=WorldObject("house","house",2,0,"A modest wooden house with a faded blue door.")
    w.objects["tree"]=WorldObject("tree","tree",-2,1,"A broad old tree. Its leaves move gently in the wind.")
    w.objects["well"]=WorldObject("well","well",1,2,"A stone well containing clean, cold water.",drinkable=True)
    w.objects["bread"]=WorldObject("bread","bread",0,0,"A fresh loaf of bread.",portable=True,edible=True)
    w.npcs["thomas"]=NPC("thomas","Thomas",2,2,"A man carrying a small bundle of firewood.",
                          ["Thomas looks at you.",'"Morning."',"He shifts the bundle under his arm."])
    return w
