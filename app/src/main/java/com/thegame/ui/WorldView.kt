package com.thegame.ui

import android.content.Context
import android.graphics.Canvas
import android.graphics.Paint
import android.graphics.Typeface
import android.view.View
import com.thegame.game.GameState
import com.thegame.world.Npc
import com.thegame.world.WorldObject
import kotlin.math.max
import kotlin.math.min

class WorldView(context: Context) : View(context) {

    private val paint = Paint(Paint.ANTI_ALIAS_FLAG).apply {
        typeface = Typeface.MONOSPACE
    }

    private var state: GameState? = null

    fun update(newState: GameState) {
        state = newState
        invalidate()
    }

    override fun onDraw(canvas: Canvas) {
        super.onDraw(canvas)

        val current = state ?: return

        canvas.drawColor(android.graphics.Color.rgb(24, 24, 24))

        val width = width.toFloat()
        val height = height.toFloat()

        val centerX = width / 2f
        val centerY = height / 2f

        val gridSize = min(width, height) / 7f
        val scale = gridSize

        paint.style = Paint.Style.STROKE
        paint.strokeWidth = 1f
        paint.color = android.graphics.Color.rgb(55, 55, 55)

        for (i in -4..4) {
            canvas.drawLine(
                centerX + i * scale,
                0f,
                centerX + i * scale,
                height,
                paint
            )

            canvas.drawLine(
                0f,
                centerY + i * scale,
                width,
                centerY + i * scale,
                paint
            )
        }

        // Road
        paint.style = Paint.Style.FILL
        paint.color = android.graphics.Color.rgb(65, 65, 65)

        canvas.drawRect(
            0f,
            centerY - scale / 3f,
            width,
            centerY + scale / 3f,
            paint
        )

        drawObjects(
            canvas,
            current.world.nearby(
                current.player.x,
                current.player.y,
                4
            ),
            current
        )

        drawNpcs(
            canvas,
            current.world.nearbyNpcs(
                current.player.x,
                current.player.y,
                4
            ),
            current
        )

        // Player
        paint.color = android.graphics.Color.WHITE
        canvas.drawCircle(centerX, centerY, scale * 0.22f, paint)

        paint.color = android.graphics.Color.WHITE
        paint.textSize = max(22f, scale * 0.32f)
        paint.textAlign = Paint.Align.CENTER
        canvas.drawText(
            "YOU",
            centerX,
            centerY + scale * 0.55f,
            paint
        )

        paint.textAlign = Paint.Align.LEFT
        paint.textSize = 18f
        paint.color = android.graphics.Color.LTGRAY
        canvas.drawText(
            "DAY ${current.day}   ${formatHour(current.hour)}",
            18f,
            30f,
            paint
        )
    }

    private fun drawObjects(
        canvas: Canvas,
        objects: List<WorldObject>,
        state: GameState
    ) {
        val scale = min(width, height) / 7f
        val centerX = width / 2f
        val centerY = height / 2f

        for (obj in objects) {
            val dx = obj.x - state.player.x
            val dy = obj.y - state.player.y

            val x = centerX + dx * scale
            val y = centerY + dy * scale

            paint.color = android.graphics.Color.rgb(170, 170, 170)
            paint.style = Paint.Style.FILL

            when (obj.name) {
                "tree" -> {
                    canvas.drawRect(
                        x - 8f,
                        y - 18f,
                        x + 8f,
                        y + 15f,
                        paint
                    )
                    canvas.drawCircle(x, y - 20f, 18f, paint)
                }

                "house" -> {
                    canvas.drawRect(
                        x - 20f,
                        y - 15f,
                        x + 20f,
                        y + 18f,
                        paint
                    )
                }

                "well" -> {
                    paint.style = Paint.Style.STROKE
                    paint.strokeWidth = 5f
                    canvas.drawCircle(x, y, 16f, paint)
                }

                else -> {
                    canvas.drawCircle(x, y, 8f, paint)
                }
            }

            paint.style = Paint.Style.FILL
            paint.textSize = 15f
            paint.textAlign = Paint.Align.CENTER
            canvas.drawText(obj.name, x, y + 35f, paint)
        }
    }

    private fun drawNpcs(
        canvas: Canvas,
        npcs: List<Npc>,
        state: GameState
    ) {
        val scale = min(width, height) / 7f
        val centerX = width / 2f
        val centerY = height / 2f

        for (npc in npcs) {
            val dx = npc.x - state.player.x
            val dy = npc.y - state.player.y

            val x = centerX + dx * scale
            val y = centerY + dy * scale

            paint.style = Paint.Style.FILL
            paint.color = android.graphics.Color.rgb(220, 220, 220)

            canvas.drawCircle(x, y, 12f, paint)

            paint.color = android.graphics.Color.WHITE
            paint.textSize = 15f
            paint.textAlign = Paint.Align.CENTER
            canvas.drawText(
                npc.name,
                x,
                y + 30f,
                paint
            )
        }
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
