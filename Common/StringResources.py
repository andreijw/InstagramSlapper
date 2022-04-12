"""
String Resources
Holds string resources used by the script
"""

# Intro String Resources
INTRO_TEXT = "Starting instagram bot.\n"
INVALID_USAGE_MODE = "Invalid Usage. - Please try again, usage: Username, Password, \
Mode (0-8). The modes are defined in the README.\n"
INVALID_USERNAME = "Invalid Username. Only Alpha-numeric, period and underscore \
characters are allowed.\n"
INVALID_PASSWORD = "Invalid Password. Only Alpha-numeric and punctuation characters \
are allowed.\n"
INVALID_MODE = "Invalid Mode. This option must be numeric and non negative.\n"
VALID_INPUT_DATA = "Input Data is valid.\n"
EXCEPTION_MESSAGE = "An error ocurred while running the bot | {0}.\n"
CLOSING_MESSAGE = "Closing the instagram bot.\n"
FAILED_LOGIN_MESSAGE = "Failed to log into instagram with the input username {0} \
and password {1}.\n"
SUCCESFUL_LOGIN_MESSAGE = "Logged in into the account {0} | password {1} | mode {2}.\n"
INSTAGRAM_TWO_FACTOR_AUTH_MESSAGE = "Please put in the two factor authentication \
code if needed.\n"
INSTAGRAM_FILE_READ_ERROR = "Error while reading the input file | "
INSTAGRAM_ACCOUNT_PAGE_MESSAGE = "Loading the account {0}."
INSTAGRAM_LOAD_FOLLOWERS_MESSAGE = "\tLoading the people that follow {0}."
INSTAGRAM_FOUND_FOLLOWERS_MESSAGE = "\tFollowers found ->"
INSAGRAM_LOAD_FOLLOWING_MESSAGE = "\tLoading the people that the account {0} follows."
INSTAGRAM_FOUND_FOLLOWING_MESSAGE = "\tFollowing found -> "
INSTAGRAM_BAD_FOLLOWERS_MESSAGE = "Obtaining bad followers for the account"
INSTAGRAM_PERSON_ITEM_TEXT = "follower {0} is - {1}"
INSTAGRAM_TOTAL_FOLLOWERS_TEXT = "The total account followers are: {0}"
INSTAGRAM_TOTAL_FOLLOWING_TEXT = "Total amount of people that the account follows: {0}"
INSTAGRAM_TOTAL_BAD_FOLLOWERS_TEXT = "Total amount of bad followers: {0}"
INSTAGRAM_TEXT_OUTPUT_MESSAGE = "Wrote the contents to the file - {0}"
INSTAGRAM_MODE_ONE_MESSAGE = "Mode is set to 1. Only obtaining the followers set."
INSTAGRAM_MODE_TWO_MESSAGE = "Mode is set to 2. Only obtaining the following set."
INSTAGRAM_MODE_THREE_MESSAGE = "Mode is set to 3. Only obtaining the badFollowers set."
INSTAGRAM_MODE_FOUR_MESSAGE_START = "Mode set to 4, reading in from the files."
INSTAGRAM_FOLLOWER_SET_SIZE = "Length of followers set - {0}."
INSTAGRAM_FOLLOWING_SET_SIZE = "Length of following set - {0}."
INSTAGRAM_BAD_FOLLOWER_SET_SIZE = "Length of badFollowers set - {0}."
INSTAGRAM_REMOVE_LIST_SIZE = "Filtered out the clean list followers about to remove {0}."
INSTAGRAM_CLEAN_LIST_SET_SIZE = "Length of cleanList set - {0}."
INSTAGRAM_UNFOLLOW_ACCOUNT_TEXT = "\tUnfollowing {0}"
INSTAGRAM_MODE_FOUR_MESSAGE = "Mode is set to 4. Unfollowed all the bad followers and exiting."
INSTAGRAM_UNFOLLOW_ERROR_MESSAGE = "Error unfollowing - {0} | {1}"