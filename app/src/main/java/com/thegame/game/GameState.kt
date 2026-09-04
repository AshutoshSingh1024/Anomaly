package com.thegame.game

import com.thegame.world.Player
import com.thegame.world.World

data class GameState(
    val world: World,
    val player: Player,
    var hour: Int = 8,
    var day: Int = 1
) {
    companion object {
        fun createInitial(): GameState {
            val world = World.createInitial()
            val player = Player(
                name = "You",
                x = 0,
                y = 0
            )
            return GameState(
                world = world,
                player = player
            )
        }
    }
}
