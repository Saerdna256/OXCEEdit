import unittest

from bases import base
from soldier import soldier
from constants import *

class test_Bases(unittest.TestCase):
    
    def test_addSoldier(self) -> None:
        testBase = base(1, "test")
        testSoldier = soldier(0, "OXCE")
        testBase.add_soldier_to_base(testSoldier)
        expected = "OXCE"
        actual = testBase.soldiers[0].name
        self.assertEqual(expected, actual)

    def test_soldierById(self) -> None:
        testBase = base()
        testBase.add_soldier_to_base(soldier(0, "wrong"))
        testBase.add_soldier_to_base(soldier(26, "right"))
        testBase.add_soldier_to_base(soldier(3, "wrong"))
        testBase.add_soldier_to_base(soldier(5, "wrong"))
        expected = "right"
        actual = testBase.get_soldier_by_id(26).name
        self.assertEqual(expected, actual)
        