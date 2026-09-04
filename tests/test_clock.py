import unittest
from game.clock import GameClock

class ClockTests(unittest.TestCase):
    def test_rollover(self):
        c=GameClock(1,23); c.advance()
        self.assertEqual((c.day,c.hour),(2,0))
    def test_multiple(self):
        c=GameClock(1,8); c.advance(20)
        self.assertEqual((c.day,c.hour),(2,4))

if __name__=="__main__": unittest.main()
