package com.thegame.world

class World(
    val objects: MutableList<WorldObject>,
    val npcs: MutableList<Npc>
) {

    companion object {
        fun createInitial(): World {
            return World(
                objects = mutableListOf(
                    WorldObject(
                        id = "house",
                        name = "house",
                        description = "A small wooden house. Its door is closed.",
                        x = 2,
                        y = 0
                    ),
                    WorldObject(
                        id = "tree",
                        name = "tree",
                        description = "A broad old tree stands beside the road.",
                        x = -2,
                        y = 1
                    ),
                    WorldObject(
                        id = "well",
                        name = "well",
                        description = "A stone well. Clear water can be seen below.",
                        x = 1,
                        y = 2,
                        drinkable = true
                    ),
                    WorldObject(
                        id = "bread",
                        name = "bread",
                        description = "A piece of fresh bread.",
                        x = 0,
                        y = 0,
                        portable = true,
                        edible = true
                    )
                ),
                npcs = mutableListOf(
                    Npc(
                        id = "thomas",
                        name = "Thomas",
                        description = "A farmer carrying a worn wooden tool.",
                        x = 2,
                        y = 2
                    )
                )
            )
        }
    }

    fun nearby(x: Int, y: Int, radius: Int = 3): List<WorldObject> {
        return objects.filter {
            distance(x, y, it.x, it.y) <= radius
        }
    }

    fun nearbyNpcs(x: Int, y: Int, radius: Int = 3): List<Npc> {
        return npcs.filter {
            distance(x, y, it.x, it.y) <= radius
        }
    }

    fun findObject(name: String, x: Int, y: Int): WorldObject? {
        return objects.firstOrNull {
            it.name.equals(name, ignoreCase = true) &&
                distance(x, y, it.x, it.y) <= 5
        }
    }

    fun findNpc(name: String, x: Int, y: Int): Npc? {
        return npcs.firstOrNull {
            it.name.equals(name, ignoreCase = true) &&
                distance(x, y, it.x, it.y) <= 5
        }
    }

    private fun distance(x1: Int, y1: Int, x2: Int, y2: Int): Int {
        return kotlin.math.abs(x1 - x2) + kotlin.math.abs(y1 - y2)
    }
}

data class Npc(
    val id: String,
    val name: String,
    val description: String,
    var x: Int,
    var y: Int
)
