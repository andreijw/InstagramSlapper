"""
Constants.py
Contains different constants used throughout the script
"""

# Main urls and paths
CHORMIUM_DRIVER_PATH = ".\\chromedriver.exe"
INSTAGRAM_URL = "https://www.instagram.com/"
INSTAGRAM_LOGIN_URL = "https://www.instagram.com/accounts/login/"
INSTAGRAM_FORMATTABLE_URL = "https://www.instagram.com/{0}/"

# output path constants
FOLLOWERS_FILE_PATH = "./Output/Followers.txt"
FOLLOWING_FILE_PATH = "./Output/Following.txt"
CLEAN_LIST_FILE_PATH = "./Output/CleanList.txt"
BAD_FOLLOWERS_FILE_PATH = "./Output/BadFollowers.txt"

# Validation
INSTAGRAM_USERNAME_REGEX = "^[A-Za-z0-9_\.]*$"
INSTAGRAM_PASSWORD_REGEX = "^[A-Za-z0-9\.\?!,'#]*$"

# Validation tests
TEST_INVALID_USERNAME = "andrei+jw"
TEST_VALID_USERNAME = "andreijw_.123"

# InstragramController
INSTAGRAM_USERNAME_FIELD = "username"
INSTAGRAM_PASSWORD_FIELD = "password"
INSTAGRAM_LOGIN_WAIT_SECONDS = 10
INSTAGRAM_IDDLE_WAIT_SECONDS = 3
INSTAGRAM_LOGIN_LOAD_WAIT_SECONDS = 15
INSTAGRAM_LOGIN_FORM_NAME = "form"
INSTAGRAM_NOT_NOW_BUTTON_XPATH = "//button[contains(text(), 'Not Now')]"

#Browser
INSTAGRAM_SEE_ALL_NAME = "See All"