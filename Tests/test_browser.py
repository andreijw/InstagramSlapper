"""
test_browser.py

Unit Tests class for the Browser functions
"""

from nose.tools import assert_equal
from parameterized import parameterized, parameterized_class
from Library import Browser

import unittest

class TestValidation(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.browser = Browser.Browser()

    def test_initialize_browser(self):
         assert_equal(self.browser.webDriver is None, True)         
         self.browser.initialize_browser()         
         assert_equal(self.browser.webDriver is None, False)

    def test_stop_browser(self):
        if self.browser.webDriver is not None:
            self.browser.stop_browser

        assert_equal(self.browser.webDriver is None, True)

if __name__ == '__main__':
    unittest.main()