package com.thegame.terminal

data class Command(
    val verb: String,
    val target: String?
)

class CommandParser {

    fun parse(raw: String): Command? {
        val cleaned = raw.trim()

        if (cleaned.isEmpty()) {
            return null
        }

        val parts = cleaned.split(Regex("\\s+"), limit = 2)

        val verb = parts[0].lowercase()
        val target = parts.getOrNull(1)?.trim()

        return Command(verb, target)
    }
}
