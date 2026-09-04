# Anomaly

Windows-first prototype for a living-world text game.

> The player is not the protagonist of the world. The player is an intrusion into it.

## Phase 1

- Windows desktop application
- Python + Tkinter
- Fully offline
- No network, accounts, analytics, ads, WebView, or external services
- Text-command terminal
- Small rendered world
- Player movement and object interaction
- Basic NPC interaction
- World clock
- JSON save/load

## Run

Install Python 3.10+ on Windows, then run `python main.py`, or double-click `run.bat`.

## Commands

`look`, `move north|south|east|west`, `find <thing>`, `inspect <thing>`, `take <thing>`, `drop <thing>`, `eat <thing>`, `drink <thing>`, `talk <person>`, `wait`, `start`/`resume`, `stop`, `save`, `load`, `clear`, `help`, `quit`.

## Architecture

`UI -> GameController -> CommandParser/Executor -> World/Entities/Clock -> GameState`



## Future Scope

NPC schedules, needs, goals, relationships, memory, knowledge, rumors, economy, autonomous events, anomaly detection, larger worlds, and optional C++ acceleration can be added later.


## Current prototype features

- Colored world grid with visible `x,y` coordinates.
- In-game time advances automatically: **1 real second = 2 in-game minutes** (5 real seconds = 10 in-game minutes).
- After each command, the terminal waits for a physical Enter press before accepting the next command. This interaction pause never changes game time; a manual `stop` remains in effect after it is dismissed.
- Basic day/night cycle with sun and moon indicators.
- Expanded starting village with several NPCs and world objects.
- Coordinate movement such as `move to (10,15)` or `move 10 15`.
- Directional movement remains available with `move north`, `move south`, etc.
