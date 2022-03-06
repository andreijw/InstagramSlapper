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
            print("Initializing the browser")
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
        
        return self.webDriver.find_element_by_name(elementNname)
        
    '''
    Find the element by it's tag name
    '''
    def find_element_by_tag(self, tagName):
        self.initialize_browser()
        
        return self.webDriver.find_element_by_tag_name(tagName)
        
    '''
    Finds the first n element thats contains the input xpath
    '''
    def find_elements_by_x_path(self, xpath, elements):
        self.initialize_browser()
        
        # Unwrap the element if we only want 1
        if elements == 1:
            return self.webDriver.find_elements_by_xpath(xpath)[0]
            
        return self.webDriver.find_elements_by_xpath(xpath)[0: elements]
    
    '''
    Finds the first element that contains the input partial link
    '''
    def find_element_by_link(self, linkText):
        self.initialize_browser()
        
        return self.webDriver.find_element_by_partial_link_text(linkText)
        
    '''
    Wait for the driver to load the elment with the input xpath
    '''
    def web_driver_wait_xpath(self, waitTime, text):
        self.initialize_browser()
        
        return WebDriverWait(self.webDriver, waitTime).until(
            EC.presence_of_element_located((By.XPATH, text)))

    '''
    Wait for the driver to load the input page using the mode
    '''
    def web_driver_wait_link_text(self, waitTime, text):
        self.initialize_browser()
        
        WebDriverWait(self.webDriver, waitTime).until(
            EC.presence_of_element_located((By.LINK_TEXT, text)))
    
    '''
    Execute the input script
    '''
    def execute_input_script(self, inputScript, additionalText):
        self.initialize_browser()
        
        self.webDriver.execute_script(inputScript, additionalText)
        
        