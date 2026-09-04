from dataclasses import dataclass


@dataclass
class GameClock:
    day: int = 1
    hour: int = 8
    minute: int = 0

    # 5 real seconds = 10 in-game minutes.
    # Therefore:
    # 1 real second = 2 in-game minutes.
    REAL_SECONDS_PER_GAME_MINUTE = 0.5

    def advance_minutes(self, minutes: int = 10):
        if minutes < 0:
            raise ValueError("Time cannot move backwards.")

        total = self.hour * 60 + self.minute + minutes

        self.day += total // (24 * 60)
        total %= 24 * 60

        self.hour = total // 60
        self.minute = total % 60

    def advance(self, hours: int = 1):
        self.advance_minutes(hours * 60)

    @property
    def period(self):
        if 6 <= self.hour < 12:
            return "morning"
        if 12 <= self.hour < 18:
            return "afternoon"
        if 18 <= self.hour < 22:
            return "evening"
        return "night"

    @property
    def is_day(self):
        return 6 <= self.hour < 18

    @property
    def celestial_body(self):
        return "sun" if self.is_day else "moon"

    def display(self):
        return (
            f"Day {self.day} | "
            f"{self.hour:02d}:{self.minute:02d} | "
            f"{self.period}"
        )