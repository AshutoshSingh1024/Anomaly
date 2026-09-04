from world.world import World
from world.objects import WorldObject, Location
from world.npc import NPC


def create_initial_world():
    w = World(width=31, height=21)
    w.locations["village"] = Location(
        "village", "Village", 15, 10,
        "A small settlement connected by an old road.", 6, {"settlement"}
    )

    w.objects["house"] = WorldObject("house", "house", 17, 10, "A modest wooden house with a faded blue door.")
    w.objects["tree"] = WorldObject("tree", "tree", 13, 11, "A broad old tree. Its leaves move gently in the wind.")
    w.objects["well"] = WorldObject("well", "well", 16, 12, "A stone well containing clean, cold water.", drinkable=True)
    w.objects["bread"] = WorldObject("bread", "bread", 15, 10, "A fresh loaf of bread.", portable=True, edible=True)
    w.objects["shed"] = WorldObject("shed", "shed", 10, 8, "A small weathered storage shed.")
    w.objects["rock"] = WorldObject("rock", "rock", 21, 13, "A flat grey stone jutting from the earth.")
    w.objects["oak"] = WorldObject("oak", "oak tree", 23, 6, "A large oak overlooking the road.")

    w.npcs["thomas"] = NPC(
        "thomas", "Thomas", 17, 12,
        "A man carrying a small bundle of firewood.",
        ["Thomas looks at you.", '"Morning."', "He shifts the bundle under his arm."]
    )
    w.npcs["martha"] = NPC(
        "martha", "Martha", 12, 10,
        "An older woman carrying a basket of vegetables.",
        ["Martha studies you for a moment.", '"You are new around here."']
    )
    w.npcs["jonas"] = NPC(
        "jonas", "Jonas", 20, 7,
        "A young man repairing a leather strap.",
        ["Jonas nods without looking up.", '"Busy day."']
    )
    w.npcs["elena"] = NPC(
        "elena", "Elena", 8, 12,
        "A woman gathering herbs beside the road.",
        ["Elena gives you a cautious smile.", '"The woods are quieter today."']
    )
    w.npcs["samuel"] = NPC(
        "samuel", "Samuel", 22, 14,
        "A farmer resting beside a cart.",
        ["Samuel wipes his hands on his trousers.", '"Afternoon."']
    )
    return w
