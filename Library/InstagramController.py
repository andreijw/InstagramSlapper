"""
Validation.py

This file will serve to control the instagram website through the webDriver
"""

from Common import Constants
from Library import Browser

class InstagramController:
    def __init__(self):
        self.Browser = None

    ''' 
    Initialize the instagram controller, and webDriver and save the instance
    '''
    def initialize_controller(self):
         self.Browser = Browser.Browser()
         self.Browser.initialize_browser()

    '''
    Stop the controller and quit the webdriver browser
    '''
    def stop_controller(self):
        if self.Browser is not None:
            self.Browser.stop_browser()