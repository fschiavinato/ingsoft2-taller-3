from typing import Iterable, List, Set, Tuple
import unittest
from crashme import crashme
from magicfuzzer import MagicFuzzer

Location = Tuple[str, int]


class TestCase(unittest.TestCase):
    def test_magic_fuzzer(self):
        self._assert([], set(), [])
        self._assert(["good"], self._locations([2]), ["good"])
        self._assert(["bad!"], self._locations(range(2, 7)), ["bad!"])
        self._assert(["good", "goo"], self._locations([2]), ["good"])
        self._assert(["good", "bad!"], self._locations(range(2, 7)), ["good", "bad!"])
        self._assert(["bad!", "good"], self._locations(range(2, 7)), ["bad!"])
        self._assert(
            ["good", "b", "ba"], self._locations(range(2, 5)), ["good", "b", "ba"]
        )
        self._assert(
            ["good", "b", "bad!"], self._locations(range(2, 7)), ["good", "b", "bad!"]
        )
        self._assert(
            ["good", "go", "b", "bad!"],
            self._locations(range(2, 7)),
            ["good", "b", "bad!"],
        )

    def _assert(self, input, expected_cover: Set, expected_contributing: List):

        fuzzer = MagicFuzzer(input, crashme, "crashme")
        self.assertSetEqual(fuzzer.get_covered_locations(), expected_cover)
        self.assertListEqual(fuzzer.get_contributing_inputs(), expected_contributing)

    def _locations(self, lines: Iterable[int]):
        return set(("crashme", i) for i in lines)
