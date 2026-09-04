import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from game.controller import GameController


class ControllerTimeTests(unittest.TestCase):
    def setUp(self):
        self.controller = GameController()

    def clock_position(self):
        clock = self.controller.state.clock
        return clock.day, clock.hour, clock.minute

    def test_command_advances_then_pauses_interaction(self):
        result = self.controller.execute("look")

        self.assertTrue(result.consumes_time)
        self.assertEqual(self.clock_position(), (1, 8, 2))
        self.assertTrue(self.controller.interaction_paused)

        # Real-time ticks must have no effect until Enter dismisses the pause.
        self.controller.advance_time(2)
        self.assertEqual(self.clock_position(), (1, 8, 2))

        self.controller.continue_after_interaction()
        self.controller.advance_time(2)
        self.assertEqual(self.clock_position(), (1, 8, 4))

    def test_stop_survives_interaction_continue(self):
        self.controller.execute("stop")

        self.assertFalse(self.controller.time_running)
        self.assertTrue(self.controller.interaction_paused)

        self.controller.continue_after_interaction()
        self.controller.advance_time(2)
        self.assertEqual(self.clock_position(), (1, 8, 0))

    def test_resume_restores_progress_after_interaction_continue(self):
        self.controller.stop_time()
        self.controller.execute("resume")

        self.assertTrue(self.controller.time_running)
        self.assertTrue(self.controller.interaction_paused)

        self.controller.continue_after_interaction()
        self.controller.advance_time(2)
        self.assertEqual(self.clock_position(), (1, 8, 2))

    def test_empty_input_does_not_pause_or_advance_time(self):
        result = self.controller.execute("   ")

        self.assertFalse(result.consumes_time)
        self.assertFalse(self.controller.interaction_paused)
        self.assertEqual(self.clock_position(), (1, 8, 0))

    def test_save_and_load_preserve_the_clock_state(self):
        self.controller.advance_time(7)

        with TemporaryDirectory() as directory:
            save_path = Path(directory) / "save.json"
            self.controller.save(save_path)
            self.controller.advance_time(9)
            self.controller.load(save_path)

        self.assertEqual(self.clock_position(), (1, 8, 7))


if __name__ == "__main__":
    unittest.main()
