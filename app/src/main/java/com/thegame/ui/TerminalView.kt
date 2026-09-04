package com.thegame.ui

import android.content.Context
import android.graphics.Color
import android.graphics.Typeface
import android.view.Gravity
import android.view.KeyEvent
import android.view.inputmethod.EditorInfo
import android.widget.EditText
import android.widget.LinearLayout
import android.widget.ScrollView
import android.widget.TextView

class TerminalView(context: Context) : LinearLayout(context) {

    private val output = TextView(context)
    private val input = EditText(context)

    private var commandHandler: ((String) -> Unit)? = null

    init {
        orientation = VERTICAL
        setBackgroundColor(Color.rgb(11, 11, 11))
        setPadding(12, 8, 12, 8)

        val scrollView = ScrollView(context)

        output.setTextColor(Color.rgb(225, 225, 225))
        output.setTextSize(14f)
        output.typeface = Typeface.MONOSPACE
        output.setPadding(4, 4, 4, 8)
        output.gravity = Gravity.BOTTOM
        output.textIsSelectable = true

        scrollView.addView(
            output,
            LayoutParams(
                LayoutParams.MATCH_PARENT,
                LayoutParams.MATCH_PARENT
            )
        )

        input.setTextColor(Color.WHITE)
        input.setHintTextColor(Color.rgb(110, 110, 110))
        input.setHint("type a command...")
        input.setTextSize(14f)
        input.typeface = Typeface.MONOSPACE
        input.setSingleLine(true)
        input.imeOptions = EditorInfo.IME_ACTION_SEND

        val inputRow = LinearLayout(context).apply {
            orientation = HORIZONTAL
            gravity = Gravity.CENTER_VERTICAL
        }

        val prompt = TextView(context).apply {
            text = "> "
            setTextColor(Color.WHITE)
            textSize = 14f
            typeface = Typeface.MONOSPACE
        }

        inputRow.addView(
            prompt,
            LayoutParams(
                LayoutParams.WRAP_CONTENT,
                LayoutParams.WRAP_CONTENT
            )
        )

        inputRow.addView(
            input,
            LayoutParams(
                0,
                LayoutParams.WRAP_CONTENT,
                1f
            )
        )

        addView(
            scrollView,
            LayoutParams(
                LayoutParams.MATCH_PARENT,
                0,
                1f
            )
        )

        addView(
            inputRow,
            LayoutParams(
                LayoutParams.MATCH_PARENT,
                LayoutParams.WRAP_CONTENT
            )
        )

        input.setOnEditorActionListener { _, actionId, event ->
            val enterPressed =
                event?.keyCode == KeyEvent.KEYCODE_ENTER &&
                    event.action == KeyEvent.ACTION_DOWN

            if (actionId == EditorInfo.IME_ACTION_SEND || enterPressed) {
                submit()
                true
            } else {
                false
            }
        }
    }

    fun setCommandHandler(handler: (String) -> Unit) {
        commandHandler = handler
    }

    fun addOutput(text: String) {
        output.append("$text\n")
        output.post {
            (output.parent as? ScrollView)?.fullScroll(ScrollView.FOCUS_DOWN)
        }
    }

    private fun submit() {
        val command = input.text.toString().trim()

        if (command.isEmpty()) {
            return
        }

        input.text.clear()
        commandHandler?.invoke(command)
        input.requestFocus()
    }
}
