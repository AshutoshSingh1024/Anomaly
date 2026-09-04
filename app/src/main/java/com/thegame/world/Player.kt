package com.thegame.world

data class Player(
    val name: String,
    var x: Int,
    var y: Int,
    val inventory: MutableList<WorldObject> = mutableListOf()
)
