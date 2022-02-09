"""
Validation.py

This file will serve to control the browser 
"""
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

from Common import Constants

class Browser:

    def __init__(self):
        self.webDriver = None
        
    ''' 
    Initialize a chrome browser using the latest chromium driver
    For now the chromedriver.exe must be in the same dir as the python script
    '''
    def initialize_browser(self):
         self.webDriver = webdriver.Chrome(executable_path=Constants.CHORMIUM_DRIVER_PATH)
         self.webDriver.implicitly_wait(5)
    
    ''' 
    Quit the webdriver browser
    '''
    def stop_browser(self):
        if self.webDriver is not None:
            self.webDriver.quit()
            self.webDriver = None