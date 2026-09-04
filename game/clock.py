from dataclasses import dataclass

@dataclass
class GameClock:
    day: int = 1
    hour: int = 8

    def advance(self, hours: int = 1):
        if hours < 0:
            raise ValueError("Time cannot move backwards.")
        total = self.hour + hours
        self.day += total // 24
        self.hour = total % 24

    @property
    def period(self):
        if 6 <= self.hour < 12: return "morning"
        if 12 <= self.hour < 18: return "afternoon"
        if 18 <= self.hour < 22: return "evening"
        return "night"

    def display(self):
        return f"Day {self.day} | {self.hour:02d}:00 | {self.period}"
