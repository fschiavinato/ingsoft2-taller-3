import unittest

from magicfuzzer import (
    delete_random_character,
    flip_random_character,
    insert_random_character,
)


class TestCase(unittest.TestCase):
    def test_insert(self):
        test_subject = "prueba"
        l = len(test_subject)
        result = insert_random_character(test_subject)
        all_possibilities = [result[0:i] + result[i + 1 : l + 1] for i in range(l + 1)]

        self.assertTrue(test_subject in all_possibilities)

    def test_delete(self):
        test_subject = "prueba"
        result = delete_random_character(test_subject)
        l = len(test_subject)
        all_possibilities = [
            result[0:i] + test_subject[i] + result[i:l] for i in range(l)
        ]
        self.assertTrue(test_subject in all_possibilities)

    def test_flip(self):
        test_subject = "prueba"
        result = flip_random_character(test_subject)
        l = len(test_subject)
        for i in range(l):
            if result[i] != test_subject[i]:
                self.assertTrue(ord(result[i]) + ord(test_subject[i]) == 255)
            else:
                l -= 1
        self.assertEqual(l, 1)
