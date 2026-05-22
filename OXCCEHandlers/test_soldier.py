import unittest

from constants import *
from soldier import soldier

class TestSoldier(unittest.TestCase):

    def test_setBaseStats(self) -> None:
        expected_current_tu = 150
        testSoldier = soldier(1, "test")
        testSoldier.set_base_stat(TU, 150) # Should also set the actual tu to 150 since they start at 0
        actual_current_tu = testSoldier.stats[TU][CURRENT]
        self.assertEqual(expected_current_tu, actual_current_tu)

    def test_setCurrentStats(self) -> None:
        expected_base_firing = 10
        testSoldier = soldier(1, "test")
        testSoldier.set_base_stat(FIRING, 100)
        testSoldier.set_current_stat(FIRING, 10) # Should also set the base firing stat back to 10
        actual_base_firing = testSoldier.stats[FIRING][BASE]
        self.assertEqual(expected_base_firing, actual_base_firing)