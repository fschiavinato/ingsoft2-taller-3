import unittest

from magicfuzzer import RouletteInputSelector


class TestCase(unittest.TestCase):
    def test_1(self):
        selector = RouletteInputSelector(2)
        selector.add_new_execution("good", [("crashme", 2)])
        selector.add_new_execution("goo", [("crashme", 2)])
        selector.add_new_execution("go", [("crashme", 2)])
        selector.add_new_execution("b", [("crashme", 2), ("crashme", 3)])
        selector.add_new_execution("bx", [("crashme", 2), ("crashme", 3)])
        selector.add_new_execution("by", [("crashme", 2), ("crashme", 3)])
        selector.add_new_execution(
            "bad", [("crashme", 2), ("crashme", 3), ("crashme", 4), ("crashme", 5)]
        )
        self.assertEqual(selector.get_frequency("good"), 3)
        self.assertEqual(selector.get_frequency("goo"), 3)
        self.assertEqual(selector.get_frequency("go"), 3)
        self.assertEqual(selector.get_frequency("b"), 3)
        self.assertEqual(selector.get_frequency("bx"), 3)
        self.assertEqual(selector.get_frequency("by"), 3)
        self.assertEqual(selector.get_frequency("bad"), 1)
        selection = selector.select()
        self.assertIn(selection, {"good", "goo", "go", "b", "bx", "by", "bad"})
