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