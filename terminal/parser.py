from dataclasses import dataclass

@dataclass
class ParsedCommand:
    name: str
    arguments: list[str]

class CommandParser:
    def parse(self, raw):
        parts = raw.strip().split()
        return ParsedCommand(parts[0].lower(), parts[1:]) if parts else ParsedCommand("", [])
