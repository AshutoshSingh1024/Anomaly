import unittest

from game.state import GameState
from world.generation import create_initial_world


class WorldSimulationTests(unittest.TestCase):
    def setUp(self):
        self.world = create_initial_world()
        self.state = GameState(self.world, self.world.create_player())

    def test_npcs_follow_a_scheduled_activity(self):
        self.state.clock.hour = 8
        self.state.clock.minute = 10
        thomas = self.world.npcs["thomas"]

        self.world.tick(self.state)

        self.assertEqual(thomas.current_activity, "collecting firewood near the shed")
        self.assertEqual((thomas.x, thomas.y), (16, 12))
        self.assertTrue(self.world.event_log)
        self.assertTrue(thomas.memories)

    def test_rain_changes_npc_behavior_to_shelter(self):
        self.state.clock.hour = 14
        self.state.clock.minute = 10
        self.world.weather = "rain"
        thomas = self.world.npcs["thomas"]

        self.world.tick(self.state)

        self.assertEqual(thomas.current_activity, "sheltering from the rain")
        self.assertEqual((thomas.x, thomas.y), (17, 11))

    def test_world_events_and_weather_survive_serialization(self):
        self.state.clock.hour = 18
        self.state.clock.minute = 0

        self.world.tick(self.state)
        restored = type(self.world).from_dict(self.world.to_dict())

        self.assertTrue(restored.event_log)
        self.assertEqual(restored.weather, self.world.weather)
        self.assertEqual(
            restored.npcs["thomas"].memories,
            self.world.npcs["thomas"].memories
        )


if __name__ == "__main__":
    unittest.main()
