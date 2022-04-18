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
REFOLLOW_FILE_PATH = "./Output/Refollow.txt"

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
INSTAGRAM_FOLLOWERS_LINK_NAME = "followers"
INSTAGRAM_FOLLOWING_LINK_NAME = "following"
INSTAGRAM_FOLLOWERS_X_PATH = "//li[2]/a/div/span"
INSTAGRAM_FOLLOWING_X_PATH = "//li[3]/a/div/span"
INSTAGRAM_PEOPLE_COUNT_DIV = "//div[@role='dialog']"
INSTAGRAM_PEOPLE_CSS = "ul div li:nth-child({}) a.notranslate"
INSTAGRAM_MODAL_SCOLL_TEXT = "arguments[0].scrollIntoView();"
INSTAGRAM_PERSON_MODAL_XPATH = "//div[@role='dialog']"
INSTAGRAM_UNFOLLOW_XPATH = "//button[contains(text(), 'Unfollow')]"
INSTAGRAM_UNFOLLOW_LOAD_XPATH = "//*[contains(@aria-label, 'Following')]"
INSTAGRAM_UNFOLLOW_WAIT_SECONDS = 2

# Browser
INSTAGRAM_SEE_ALL_NAME = "See All"

# Image Manipulator
IMAGE_TEMP_DIRECTORY = "./images"
IMAGE_SOURCE_XPATH = "//img[contains(@class,'_6q-tv')]"
IMAGE_SOURCE_ATTRIBUTE = "src"
IMAGE_DOWNLOAD_PROFILE_NAME = "{0}/profile.png"
POSTED_IMAGES_XPATH = "//img[contains(@class,'FFVAD')]"
DOWNLOADABLE_POST_PICTURE = "{0}/image{1}.png"