package com.thegame.terminal

import com.thegame.game.CommandResult
import com.thegame.game.GameState

class CommandExecutor {

    fun execute(command: Command, state: GameState): CommandResult {
        return when (command.verb) {
            "look", "observe" -> look(state)
            "move", "go", "walk" -> move(command.target, state)
            "find", "search" -> find(command.target, state)
            "inspect", "examine" -> inspect(command.target, state)
            "take", "get", "pick" -> take(command.target, state)
            "drop" -> drop(command.target, state)
            "eat" -> eat(command.target, state)
            "drink" -> drink(command.target, state)
            "talk", "speak" -> talk(command.target, state)
            "wait" -> CommandResult(
                "You wait for a while.",
                timePassed = true
            )
            "help" -> help()
            else -> CommandResult(
                "Unknown command '${
                    command.verb
                }'. Type 'help' for available commands.",
                timePassed = false
            )
        }
    }

    private fun look(state: GameState): CommandResult {
        val nearbyObjects = state.world.nearby(
            state.player.x,
            state.player.y
        )

        val nearbyNpcs = state.world.nearbyNpcs(
            state.player.x,
            state.player.y
        )

        val lines = mutableListOf<String>()

        lines += "Day ${state.day}, ${formatHour(state.hour)}."
        lines += "You are standing on a dirt road."

        if (nearbyObjects.isNotEmpty()) {
            lines += ""
            lines += "Nearby:"
            nearbyObjects.forEach {
                lines += "  ${it.name}"
            }
        }

        if (nearbyNpcs.isNotEmpty()) {
            lines += ""
            lines += "People:"
            nearbyNpcs.forEach {
                lines += "  ${it.name}"
            }
        }

        if (state.player.inventory.isNotEmpty()) {
            lines += ""
            lines += "Inventory:"
            state.player.inventory.forEach {
                lines += "  ${it.name}"
            }
        }

        return CommandResult(
            lines.joinToString("\n"),
            timePassed = false
        )
    }

    private fun move(
        target: String?,
        state: GameState
    ): CommandResult {
        val direction = target?.lowercase()

        when (direction) {
            "north", "n" -> state.player.y--
            "south", "s" -> state.player.y++
            "east", "e" -> state.player.x++
            "west", "w" -> state.player.x--
            else -> return CommandResult(
                "Move where? Try north, south, east, or west.",
                timePassed = false
            )
        }

        return CommandResult(
            "You move $direction.",
            timePassed = true
        )
    }

    private fun find(
        target: String?,
        state: GameState
    ): CommandResult {
        if (target.isNullOrBlank()) {
            return CommandResult(
                "Find what?",
                timePassed = false
            )
        }

        val objectFound = state.world.findObject(
            target,
            state.player.x,
            state.player.y
        )

        if (objectFound != null) {
            return CommandResult(
                "You find ${objectFound.name} nearby.\n${objectFound.description}",
                timePassed = true
            )
        }

        val npcFound = state.world.findNpc(
            target,
            state.player.x,
            state.player.y
        )

        if (npcFound != null) {
            return CommandResult(
                "You find ${npcFound.name} nearby.",
                timePassed = true
            )
        }

        return CommandResult(
            "You search, but you don't find $target.",
            timePassed = true
        )
    }

    private fun inspect(
        target: String?,
        state: GameState
    ): CommandResult {
        if (target.isNullOrBlank()) {
            return CommandResult(
                "Inspect what?",
                timePassed = false
            )
        }

        val objectFound = state.world.findObject(
            target,
            state.player.x,
            state.player.y
        )

        if (objectFound != null) {
            return CommandResult(
                objectFound.description,
                timePassed = true
            )
        }

        val npcFound = state.world.findNpc(
            target,
            state.player.x,
            state.player.y
        )

        if (npcFound != null) {
            return CommandResult(
                npcFound.description,
                timePassed = true
            )
        }

        return CommandResult(
            "You don't see $target here.",
            timePassed = false
        )
    }

    private fun take(
        target: String?,
        state: GameState
    ): CommandResult {
        if (target.isNullOrBlank()) {
            return CommandResult(
                "Take what?",
                timePassed = false
            )
        }

        val objectFound = state.world.findObject(
            target,
            state.player.x,
            state.player.y
        ) ?: return CommandResult(
            "You don't see $target here.",
            timePassed = false
        )

        if (!objectFound.portable) {
            return CommandResult(
                "You can't take the ${objectFound.name}.",
                timePassed = false
            )
        }

        state.world.objects.remove(objectFound)
        state.player.inventory.add(objectFound)

        return CommandResult(
            "You take the ${objectFound.name}.",
            timePassed = true
        )
    }

    private fun drop(
        target: String?,
        state: GameState
    ): CommandResult {
        if (target.isNullOrBlank()) {
            return CommandResult(
                "Drop what?",
                timePassed = false
            )
        }

        val item = state.player.inventory.firstOrNull {
            it.name.equals(target, ignoreCase = true)
        } ?: return CommandResult(
            "You don't have $target.",
            timePassed = false
        )

        state.player.inventory.remove(item)
        item.x = state.player.x
        item.y = state.player.y
        state.world.objects.add(item)

        return CommandResult(
            "You drop the ${item.name}.",
            timePassed = true
        )
    }

    private fun eat(
        target: String?,
        state: GameState
    ): CommandResult {
        if (target.isNullOrBlank()) {
            return CommandResult(
                "Eat what?",
                timePassed = false
            )
        }

        val item = state.player.inventory.firstOrNull {
            it.name.equals(target, ignoreCase = true)
        }

        if (item == null) {
            return CommandResult(
                "You don't have $target.",
                timePassed = false
            )
        }

        if (!item.edible) {
            return CommandResult(
                "You can't eat that.",
                timePassed = false
            )
        }

        state.player.inventory.remove(item)

        return CommandResult(
            "You eat the ${item.name}.",
            timePassed = true
        )
    }

    private fun drink(
        target: String?,
        state: GameState
    ): CommandResult {
        if (target.isNullOrBlank()) {
            return CommandResult(
                "Drink what?",
                timePassed = false
            )
        }

        val nearby = state.world.findObject(
            target,
            state.player.x,
            state.player.y
        )

        if (nearby != null && nearby.drinkable) {
            return CommandResult(
                "You drink from the ${nearby.name}.",
                timePassed = true
            )
        }

        return CommandResult(
            "You can't drink that here.",
            timePassed = false
        )
    }

    private fun talk(
        target: String?,
        state: GameState
    ): CommandResult {
        if (target.isNullOrBlank()) {
            return CommandResult(
                "Talk to whom?",
                timePassed = false
            )
        }

        val npc = state.world.findNpc(
            target,
            state.player.x,
            state.player.y
        ) ?: return CommandResult(
            "There is nobody named $target nearby.",
            timePassed = false
        )

        return CommandResult(
            "${npc.name} says, \"Morning. Fine day for working.\"",
            timePassed = true
        )
    }

    private fun help(): CommandResult {
        return CommandResult(
            """
            Commands:
              look
              move north/south/east/west
              find <thing>
              inspect <thing>
              take <thing>
              drop <thing>
              eat <thing>
              drink <thing>
              talk <person>
              wait
              help
            """.trimIndent(),
            timePassed = false
        )
    }

    private fun formatHour(hour: Int): String {
        val suffix = if (hour >= 12) "PM" else "AM"
        val display = when {
            hour == 0 -> 12
            hour > 12 -> hour - 12
            else -> hour
        }
        return "$display:00 $suffix"
    }
}
