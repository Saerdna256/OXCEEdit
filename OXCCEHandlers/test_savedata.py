import unittest

from savedata import savedata
from bases import base

class TestSavedata(unittest.TestCase):

    def testReportBasesAndGetBase(self) -> None:
        testdata = savedata("test")
        testdata.add_base(base(0, "0"))
        testdata.add_base(base(1, "1"))
        expected = 2
        actual = testdata.get_num_bases()
        self.assertEqual(expected, actual)

        expctedName = "1"
        actualName = testdata.get_base_at_index(1).name
        self.assertEqual(expctedName, actualName)

    def testCredits(self) -> None:
        testdata = savedata("test")
        testdata.set_credits(50001)
        excepted = 50001
        actual = testdata.get_credits()
        self.assertEqual(excepted, actual)

    def testGetAllBases(self) -> None:
        testdata = savedata("test")
        testdata.add_base(base(0, "0"))
        testdata.add_base(base(1, "1"))
        testdata.add_base(base(2, "2"))
        expected = 3
        return_value = testdata.get_all_bases()        
        if return_value != None:
            actual = len(return_value)
        else:
            actual = None
        self.assertEqual(expected, actual)
