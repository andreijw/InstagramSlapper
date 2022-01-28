"""
Validation.py

This file will server to validate user input, specifically the username, psw and mode
These are static instance methods. No need to create a class
"""

# Standard Imports
import re

# Custom Imports
from Common import Constants

class Validation:
    '''
    :param sysArguments - Console in input. Must have the username, password and mode
    :return: True if valid. Else false
    '''
    def validate_login(self, sysArguments):
        if len(sysArguments) != 4:
            return False
        
        if not self.__validate_username(sysArguments[1]):
            print(StringResources.INVALID_USERNAME)
            return False
        
        if not self.__validate_password(sysArguments[2]):
            print(StringResources.INVALID_PASSWORD)
            return False
            
        if not self.__validate_mode(sysArguments[3]):
            print(StringResources.INVALID_MODE)
            return False
        
        return True

    '''
    :param Instagram Username - Must only contain alpha numberic period & underscore characters
    :return: True if it's valid. Else false
    '''    
    def __validate_username(self, username):
        if not username or len(username) == 0:
            return False
            
        if len(username) > 30:
            return False
            
        match = re.search(Constants.INSTAGRAM_USERNAME_REGEX, username)    
        return not (match is None)
        

    '''
    :param Instagram password - Must be at least 6 characters comprised of letters, numbers and
    punctuation marks
    :return: True if the password is valid. Else false
    '''
    def __validate_password(self, password):
        if not password or len(password) == 0:
            return False
            
        if len(password) < 6 or len(password) > 30:
            return False
            
        match = re.search(Constants.INSTAGRAM_PASSWORD_REGEX, password)    
        return not (match is None)

    '''
    :param Mode - Must be numeric and non negative
    :return: True if the mode is valid. Else false'''
    def __validate_mode(self, mode):
        if not mode:
            return False
        
        if not mode.isnumeric():
            return False
            
        if int(mode) < 0:
            return False
        
        return True