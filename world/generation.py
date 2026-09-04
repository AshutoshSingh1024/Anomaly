from world.world import World
from world.objects import WorldObject, Location
from world.npc import NPC


def routine(*entries):
    return [
        {"key": key, "start": start, "target": target, "activity": activity}
        for key, start, target, activity in entries
    ]


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
        ["Thomas looks at you.", '"Morning."', "He shifts the bundle under his arm."],
        home=(17, 10),
        schedule=routine(
            ("night", 0, (17, 10), "sleeping at home"),
            ("morning", 6, (10, 8), "collecting firewood near the shed"),
            ("afternoon", 12, (17, 12), "stacking firewood by the well"),
            ("evening", 18, (17, 10), "returning home before dark")
        )
    )
    w.npcs["martha"] = NPC(
        "martha", "Martha", 12, 10,
        "An older woman carrying a basket of vegetables.",
        ["Martha studies you for a moment.", '"You are new around here."'],
        home=(12, 10),
        schedule=routine(
            ("night", 0, (12, 10), "resting at home"),
            ("morning", 6, (16, 12), "drawing water from the well"),
            ("afternoon", 12, (15, 10), "trading vegetables near the road"),
            ("evening", 18, (12, 10), "preparing supper")
        )
    )
    w.npcs["jonas"] = NPC(
        "jonas", "Jonas", 20, 7,
        "A young man repairing a leather strap.",
        ["Jonas nods without looking up.", '"Busy day."'],
        home=(20, 7),
        schedule=routine(
            ("night", 0, (20, 7), "sleeping in his room"),
            ("morning", 6, (21, 13), "repairing tools by the stone"),
            ("afternoon", 12, (17, 10), "running errands through the village"),
            ("evening", 18, (20, 7), "mending leather by lamplight")
        )
    )
    w.npcs["elena"] = NPC(
        "elena", "Elena", 8, 12,
        "A woman gathering herbs beside the road.",
        ["Elena gives you a cautious smile.", '"The woods are quieter today."'],
        home=(8, 12),
        schedule=routine(
            ("night", 0, (8, 12), "keeping to her cottage"),
            ("morning", 6, (8, 12), "gathering herbs beside the road"),
            ("afternoon", 12, (23, 6), "searching beneath the old oak"),
            ("evening", 18, (8, 12), "sorting herbs at home")
        )
    )
    w.npcs["samuel"] = NPC(
        "samuel", "Samuel", 22, 14,
        "A farmer resting beside a cart.",
        ["Samuel wipes his hands on his trousers.", '"Afternoon."'],
        home=(22, 14),
        schedule=routine(
            ("night", 0, (22, 14), "sleeping near the cart"),
            ("morning", 6, (22, 14), "checking the cart and fields"),
            ("afternoon", 12, (13, 11), "working beside the old tree"),
            ("evening", 18, (22, 14), "securing the cart for the night")
        )
    )
    return w
