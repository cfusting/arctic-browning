import unittest
import numpy as np
import numpy.ma as ma
import numpy.testing as npt
from lib import build_qa_mask


class MaskTest(unittest.TestCase):
    def test(self):
        inputarray = np.array([-3000, 3244, 1000, 2320, 1232, 9093, -3000])
        reliability = np.array([-1, 0, 1, 2, 3, 0, 0])
        correctmask = np.array([1, 0, 1, 1, 1, 0, 1])
        build_qa_mask(inputarray, reliability)
        npt.assert_array_equal(reliability, correctmask)
        self.assertEqual(ma.array(inputarray, mask=reliability).sum(), 12337)
