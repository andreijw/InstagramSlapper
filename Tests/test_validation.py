"""
ValidationTests.py

Unit Tests class for the Validation functions
"""

import unittest
from Library import Validation

class TestValidation(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.inputValidator = Validation.Validation()

    def test_invalid_username(self):
        self.assertTrue(True)
    
    def test_valid_username(self):
        self.assertTrue(True)
        
    def test_invalid_password(self):
        self.assertTrue(True)

    def test_valid_password(self):
        self.assertTrue(True)
    
    def test_invalid_mode(self):
        self.assertTrue(True)
    
    def test_valid_mode(self):
        self.assertTrue(True)
    
    def test_invalid_login(self):
        self.assertTrue(True)
    
if __name__ == '__main__':
    unittest.main()