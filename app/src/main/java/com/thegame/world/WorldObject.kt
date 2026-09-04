package com.thegame.world

data class WorldObject(
    val id: String,
    val name: String,
    val description: String,
    var x: Int,
    var y: Int,
    val portable: Boolean = false,
    val edible: Boolean = false,
    val drinkable: Boolean = false
)
