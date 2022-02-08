"""
test_validation.py

Unit Tests class for the Validation functions
"""

from nose.tools import assert_equal
from parameterized import parameterized, parameterized_class
from Library import Validation

import unittest

class TestValidation(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.inputValidator = Validation.Validation()

    @parameterized.expand([
        ("a","andrei_jw", True),
        ("b","andrei.jw", True),
        ("c","andrei.jw_", True),
        ("d","anddard", True),
        ("e","andrei_jw-", False),
        ("f","", False),
        ("g","aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa", False)
    ])
    def test_validate_username(self, name, username, expected):
        print("Validating the username  {0} - should be {1}".format(username, expected))
        assert_equal(self.inputValidator.validate_username(username), expected)
    
    @parameterized.expand([
        ("a","123456789", True),
        ("b","123456897#1", True),
        ("c","123456897#1?!.", True),
        ("d","123456897#1?!.,'", True),
        ("e","12345", False),
        ("f","123456789123456789123456789123456789", False),
        ("g","12354]", False)
    ])
    def test_validate_password(self, name, password, expected):
        print("Validating the password  {0} - should be {1}".format(password, expected))
        assert_equal(self.inputValidator.validate_password(password), expected)

    @parameterized.expand([
        ("a","0", True),
        ("a","1", True),
        ("b","andrei", False),
        ("c","-1", False),
        ("d","", False),
    ])
    def test_validate_mode(self, name, mode, expected):
        print("Validating the mode  {0} - should be {1}".format(mode, expected))
        assert_equal(self.inputValidator.validate_mode(mode), expected)    

    @parameterized.expand([
        ("a", ("andrei", "123456789", "0"), True),
        ("b", ("andreijw_.", "123456897#1?!.,'", "2"), True),
        ("c", ("andrei-", "123456789", "0"), False),
        ("d", ("andrei", "12345", "0"), False),
        ("e", ("andrei", "123456789", "-1"), False),
        ("e", ("","",""), False)
        ])
    def test_validate_login(self, name, arguments, expected):
        print("Validating the login items  U: {0} | P: {1} | M: {2} - should be {3}".format(*arguments, expected))
        assert_equal(self.inputValidator.validate_login(arguments), expected)
    
if __name__ == '__main__':
    unittest.main()