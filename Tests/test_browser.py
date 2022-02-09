"""
test_browser.py

Unit Tests class for the Browser functions
"""

from nose.tools import assert_equal
from parameterized import parameterized, parameterized_class
from Library import Browser

import unittest
import time

class TestValidation(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.browser = Browser.Browser()

    def test_initialize_browser(self):
        print("Testing initializing the webDriver")
        assert_equal(self.browser.webDriver is None, True)         
        self.browser.initialize_browser()
        time.sleep(5)
        assert_equal(self.browser.webDriver is None, False)
        self.browser.webDriver.quit()

    def test_stop_browser(self):
        print("Testing stopping the webDriver")
        if self.browser.webDriver is not None:
            self.browser.stop_browser()

        assert_equal(self.browser.webDriver is None, True)

if __name__ == '__main__':
    unittest.main()