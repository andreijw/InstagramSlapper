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
        if self.webDriver is None:
            self.webDriver = webdriver.Chrome(executable_path=Constants.CHORMIUM_DRIVER_PATH)
            self.webDriver.implicitly_wait(5)
    
    ''' 
    Quit the webdriver browser
    '''
    def stop_browser(self):
        if self.webDriver is not None:
            self.webDriver.quit()
            self.webDriver = None
    
    '''
    Go to the input website url on the browser driver
    '''
    def get_website(self, websiteUrl):
        self.initialize_browser()            
        self.webDriver.get(websiteUrl)
    
    '''
    Find the xml element by it's string name
    '''
    def find_element_by_name(self, elementNname):
        self.initialize_browser()
        
        element = self.webDriver.find_element_by_name(elementNname)
        return element
        
    '''
    Find the element by it's tag name
    '''
    def find_element_by_tag(self, tagName):
        self.initialize_browser()
        
        element = self.webDriver.find_element_by_tag_name(tagName)
        return element
        
    '''
    Finds the first element that contains the input xpath
    '''
    def find_element_by_xpath(self, xpath):
        self.initialize_browser()
            
        element = self.webDriver.find_elements_by_xpath(xpath)[0]
        return element
        
    '''
    Wait for the driver to load the input page
    '''
    def web_driver_wait(self, waitTime, text):
        self.initialize_browser()
        
        WebDriverWait(self.webDriver, waitTime).until(
            EC.presence_of_element_located((By.LINK_TEXT, text)))