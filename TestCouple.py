"""Test the AccessODBC module."""
import unittest

from CoupleNew import CalHighFreq

__author__ = 'JokerLiu'


class TestCouple(unittest.TestCase):
    def testHighFreqCouple(self):
        "Test the high freq couple calculate function."
        output = CalHighFreq(1, 20)
        target = {'ECal': 35.872450156127975,
                  'PowerMeter': -12.550009203175698,
                  'Antenna': 316001}
        self.assertEqual(output, target)
        output = CalHighFreq(1.5, 20)
        target = {'ECal': 42.06728989266641,
                  'PowerMeter': -13.967610284476514,
                  'Antenna': 316002}
        self.assertEqual(output, target)
        output = CalHighFreq(2, 20)
        target = {'ECal': 42.222524658966485,
                  'PowerMeter': -13.668065793920942,
                  'Antenna': 316003}
        self.assertEqual(output, target)
        output = CalHighFreq(3, 20)
        target = {'ECal': 45.96061371003099,
                  'PowerMeter': -13.911800205411883,
                  'Antenna': 316004}
        self.assertEqual(output, target)
        output = CalHighFreq(4, 20)
        target = {'ECal': 42.38782056919406,
                  'PowerMeter': -12.230870020283056,
                  'Antenna': 316005}
        self.assertEqual(output, target)
        output = CalHighFreq(6, 20)
        target = {"ECal": 46.663374765230486,
                  "PowerMeter": -12.472206228094976,
                  "Antenna": 316006}
        self.assertEqual(output, target)
        output = CalHighFreq(10, 20)
        target = {"ECal": 51.54205325357694,
                  "PowerMeter": -11.029488663700533,
                  "Antenna": 316007}
        self.assertEqual(output, target)
        output = CalHighFreq(18, 20)
        target = {"ECal": 58.42012200855186,
                  "PowerMeter": -9.946042279691973,
                  "Antenna": 316008}
        self.assertEqual(output, target)

    def testLowFreqCouple(self):
        "Test the low freq couple calculate function."
        pass


if __name__ == "__main__":
    unittest.main()
