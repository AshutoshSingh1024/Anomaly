package com.thegame

import android.os.Bundle
import android.app.Activity
import com.thegame.game.GameController
import com.thegame.game.GameState
import com.thegame.ui.TerminalView
import com.thegame.ui.WorldView

class MainActivity : Activity() {

    private lateinit var gameController: GameController
    private lateinit var worldView: WorldView
    private lateinit var terminalView: TerminalView

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)

        setContentView(R.layout.activity_main)

        val state = GameState.createInitial()
        gameController = GameController(state)

        worldView = WorldView(this)
        terminalView = TerminalView(this)

        findViewById<android.widget.FrameLayout>(R.id.world_container)
            .addView(worldView)

        findViewById<android.widget.FrameLayout>(R.id.terminal_container)
            .addView(terminalView)

        terminalView.setCommandHandler { command ->
            val result = gameController.execute(command)
            terminalView.addOutput("> $command")
            terminalView.addOutput(result.message)
            worldView.update(gameController.state)
        }

        terminalView.addOutput("THE GAME")
        terminalView.addOutput("A small world is waiting.")
        terminalView.addOutput("Type 'look' to observe your surroundings.")
        terminalView.addOutput("")
    }
}
