import unittest
import main
import sys
import argparse
import logging
import time


def run():
    unittest.TextTestRunner(verbosity=2).run(suite())


def suite():
    return unittest.TestLoader().loadTestsFromTestCase(TestSetup)


class TestSetup(unittest.TestCase):
    def setUp(self):
        self.main = main.Main()

    def tearDown(self):
        self.main = None

    def test_config(self):
        self.assertIsInstance(self.main.timer, float)
        self.assertIsInstance(self.main.config, argparse.Namespace)
        self.assertIsInstance(self.main.logger, logging.Logger)

    def test_timer(self):
        self.main.start_timer()
        time.sleep(0.1)
        time_taken = self.main.stop_timer()
        self.assertTrue(time_taken > 0.05)
        self.assertTrue(self.main.stop_timer() < 0.05)


if __name__ == "__main__":
    run()
