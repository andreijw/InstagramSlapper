"""
Validation.py

This file will serve to control the instagram website through the webDriver
"""

from time import sleep

from Common import Constants, StringResources
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
    
    '''
    Log into instagram using the input username and password
    '''
    def do_login(self, username, password):
        try:
            self.Browser.get_website(Constants.INSTAGRAM_LOGIN_URL)
            sleep(Constants.INSTAGRAM_IDDLE_WAIT_SECONDS)

            # Login with the input credentials
            self.Browser.find_element_by_name(Constants.INSTAGRAM_USERNAME_FIELD).send_keys(username)
            self.Browser.find_element_by_name(Constants.INSTAGRAM_PASSWORD_FIELD).send_keys(password)
            
            self.Browser.find_element_by_tag(Constants.INSTAGRAM_LOGIN_FORM_NAME).submit()
        
            # Sleep needed to put in the 2 factor code
            print(StringResources.INSTAGRAM_TWO_FACTOR_AUTH_MESSAGE)
            sleep(Constants.INSTAGRAM_LOGIN_WAIT_SECONDS)
        
            # Click both not now buttons
            self.Browser.find_element_by_xpath(Constants.INSTAGRAM_NOT_NOW_BUTTON_XPATH).click()    
            self.Browser.find_element_by_xpath(Constants.INSTAGRAM_NOT_NOW_BUTTON_XPATH).click()
            
            # Wait for the user dashboard page to load
            self.Browser.web_driver_wait(Constants.INSTAGRAM_LOGIN_LOAD_WAIT_SECONDS, Constants.INSTAGRAM_SEE_ALL_NAME)
            
            return True

        except Exception as e:
            print(StringResources.EXCEPTION_MESSAGE.format(e))
            return False