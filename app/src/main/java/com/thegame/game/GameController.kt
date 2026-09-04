package com.thegame.game

import com.thegame.terminal.CommandExecutor
import com.thegame.terminal.CommandParser

class GameController(
    val state: GameState
) {
    private val parser = CommandParser()
    private val executor = CommandExecutor()

    fun execute(rawCommand: String): CommandResult {
        val command = parser.parse(rawCommand)
            ?: return CommandResult("I don't understand that command.")

        val result = executor.execute(command, state)

        if (result.timePassed) {
            advanceTime()
        }

        return result
    }

    private fun advanceTime() {
        state.hour++

        if (state.hour >= 24) {
            state.hour = 0
            state.day++
        }
    }
}

data class CommandResult(
    val message: String,
    val timePassed: Boolean = true
)
