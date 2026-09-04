from dataclasses import dataclass

@dataclass
class CommandResult:
    text: str
    consumes_time: bool = True
    quit_requested: bool = False
