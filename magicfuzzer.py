from collections import defaultdict
import random
import string
from typing import Dict, Set, List

from fuzzingbook.Coverage import Location
from fuzzingbook.MutationFuzzer import FunctionCoverageRunner
from fuzzingbook.GreyboxFuzzer import getPathID

"""
Ejercicio 1
"""

chars = (
    string.ascii_uppercase + string.ascii_lowercase + string.digits + "+" + "%" + " "
)


def insert_random_character(s: str) -> str:
    l = len(s)
    i = random.randint(0, l)
    return s[:i] + random.choice(chars) + s[i:]


def delete_random_character(s: str) -> str:
    l = len(s)
    if l > 0:
        i = random.randint(0, l)
        return s[0:i] + s[i + 1 : l]
    else:
        return s


def flip_random_character(s: str) -> str:
    l = len(s)
    if l > 0:
        i = random.randint(0, l)
        c = chr(~ord(s[i]) & 0xFF)
        s = s[:i] + c + s[i + 1 :]
    return s


"""
Ejercicio 2
"""


class MagicFuzzer:
    def __init__(self, initial_inputs, function_to_call, function_name_to_call) -> None:
        self._contributing_inputs = []
        self._covered_locations = set()
        runner = FunctionCoverageRunner(function_to_call)
        for input in initial_inputs:
            last_covered = len(self._covered_locations)
            _, outcome = runner.run(input)
            locations = runner.coverage()
            for location in locations:
                if location[0] == function_name_to_call:
                    self._covered_locations.add(location)
            if len(self._covered_locations) > last_covered:
                self._contributing_inputs.append(input)

    def get_contributing_inputs(self) -> List[str]:
        return self._contributing_inputs

    def get_covered_locations(self) -> Set[Location]:
        return self._covered_locations


"""
Ejercicio 3
"""


class RouletteInputSelector:
    def __init__(self, exponent: int):
        self._exponent = exponent
        self._keys: Dict[str, int] = {}
        self._frequency: Dict[str, int] = defaultdict(lambda: 0)

    def add_new_execution(self, s: str, s_path: Set[Location]):
        k = getPathID(s_path)
        self._keys[s] = k
        self._frequency[k] += 1

    def get_energy(self, s: str) -> float:
        frequency = self.get_frequency(s)
        if frequency == 0:
            raise Exception("input not executed")
        return 1 / (frequency**self._exponent)

    def get_frequency(self, s: str) -> float:
        k = self._keys[s]
        return self._frequency[k]

    def select(self) -> str:
        energies = {s: self.get_energy(s) for s in self._keys}
        x = random.random() * sum(energies.values())
        for s, e_s in energies.items():
            if x <= e_s:
                return s
            else:
                x -= e_s


"""
Ejercicio 4
"""


class MagicFuzzer(MagicFuzzer):
    def mutate(self, s: str) -> str:
        op = random.randint(0, 2)
        if op == 0:
            return insert_random_character(s)
        elif op == 1:
            return delete_random_character(s)
        else:
            return flip_random_character(s)

    def fuzz(self) -> None:
        selector = RouletteInputSelector(2)
        
