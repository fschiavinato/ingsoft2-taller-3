import unittest

from magicfuzzer import (
    delete_random_character,
    flip_random_character,
    insert_random_character,
)

def getBitRepresentationOfChar(char):
    bits = []
    number = ord(char)
    for _ in range(7):
        if number % 2 == 1:
            bits.append("1")
        else:
            bits.append("0")
        number = number >> 1

    return "".join(bits[::-1])


class TestCase(unittest.TestCase):
    def test_insert(self):
        test_subject = "abcdefg1"
        l = len(test_subject)
        result = insert_random_character(test_subject)
        all_possibilities = [result[0:i] + result[i + 1 : l + 1] for i in range(l + 1)]

        self.assertTrue(test_subject in all_possibilities)

    def test_delete(self):
        test_subject = "prueba"
        result = delete_random_character(test_subject)
        print(result)
        l = len(test_subject)
        all_possibilities = [
            result[0:i] + test_subject[i] + result[i:l] for i in range(l)
        ]
        self.assertTrue(test_subject in all_possibilities)

    def test_flip(self):
        test_subject = "prueba"
        
        result = flip_random_character(test_subject)
        
        test_subject_bits = "".join([getBitRepresentationOfChar(x) for x in test_subject])
        result_bits = "".join([getBitRepresentationOfChar(x) for x in result])

        self.assertEqual(len(test_subject), len(result))
        amountDifferent = 0
        for i in range(len(test_subject_bits)):
            if test_subject_bits[i] != result_bits[i]:
                amountDifferent += 1
        self.assertEqual(amountDifferent, 1)
