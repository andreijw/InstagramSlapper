'''
This script can get the insta followers for an account.
The people that the account follows.
The bad followers for an account.
Unfollow bad followers for an account.
Get an account's thot score.
'''

# Standard Imports
import sys
import random
from os.path import exists
from time import sleep

# Custom imports
from Common import Constants, StringResources
from Library import Validation, InstagramController

# Write the input peopleSet into the output text file
def write_output_to_file(peopleSet, outputFile):
    with open(outputFile, 'w') as f:
        for follower in peopleSet:
            f.write("%s\n" % follower)
    
    print(StringResources.INSTAGRAM_TEXT_OUTPUT_MESSAGE.format(outputFile))
    sleep(1)
    
# Read Input file into a set. Returns an empty set on error
def read_input_file_to_set(inputFile):
    try:
        if not exists(inputFile):
            return set()
        
        return set(line.strip() for line in open(inputFile))
    except Exception as e:
        print(Strings.INSTAGRAM_FILE_READ_ERROR, e)
        return set()
    
# Main entry point for the tool. Can add / remove instagram thots
def main():
    try:
        print(StringResources.INTRO_TEXT)
        
        username, password = '', ''
        mode = 1
        controller = InstagramController.InstagramController()
        follwing, followers, badFollowers, removeList, cleanList = set(), set(), set(), set(), set()

        inputValidator = Validation.Validation()
        # Basic Usage, provide the username, password, and mode to run (0,1)
        if not inputValidator.validate_login(sys.argv[1:]):
            print(StringResources.INVALID_USAGE_MODE)
            return
        
        username = sys.argv[1]
        password = sys.argv[2]
        mode = int(sys.argv[3])
        print(StringResources.VALID_INPUT_DATA)
        
        # Initialize the chrome browser object             
        controller.initialize_controller()

        # Login to insta with the input username and password
        if not controller.do_login(username, password):
            print(StringResources.FAILED_LOGIN_MESSAGE.format(username, password))
            return

        print(StringResources.SUCCESFUL_LOGIN_MESSAGE.format(username, password, mode))

        # Modes -
        # 1 -> Get Followers of the account
        # 2 -> Get People the account follows
        # 3 -> Get Bad Followers (People that don't follow you back) + &1 & &2 obv
        # 4 -> Read in from local files Followers.txt, Following.txt and BadFollowers.txt
        # 8 ->
        if mode&1:
            followers = controller.scrape_account_people(username, 1)     
            print(StringResources.INSTAGRAM_TOTAL_FOLLOWERS_TEXT.format(len(followers)))
            write_output_to_file(followers, Constants.FOLLOWERS_FILE_PATH)
            
            if (mode ^ 1) == 0:
                print(StringResources.INSTAGRAM_MODE_ONE_MESSAGE)
                return

        if mode&2:
            # Get the people that the account follows
            following = controller.scrape_account_people(username, 2)
            print(StringResources.INSTAGRAM_TOTAL_FOLLOWING_TEXT.format(len(following)))
            write_output_to_file(following, Constants.FOLLOWING_FILE_PATH)
            
            if (mode ^ 2) == 0:
                print(StringResources.INSTAGRAM_MODE_TWO_MESSAGE)
                return

        if mode&3:
            # A bad follower is defined by me as someone followed by the account that
            # does not follow the account back
            # We can easily find this with Set Theory. Set Difference Following - Followers
            print(StringResources.INSTAGRAM_BAD_FOLLOWERS_MESSAGE)
            badFollowers = following - followers
            print(StringResources.INSTAGRAM_TOTAL_BAD_FOLLOWERS_TEXT.format(len(badFollowers)))
            write_output_to_file(badFollowers, Constants.BAD_FOLLOWERS_FILE_PATH)
            
            refollowList = read_input_file_to_set(Constants.REFOLLOW_FILE_PATH)
            refollowList = refollowList.union(badFollowers)
            write_output_to_file(refollowList, Constants.REFOLLOW_FILE_PATH)
            
            if (mode ^ 3) == 0:
                print(StringResources.INSTAGRAM_MODE_THREE_MESSAGE)
                return

        if mode&4:
            print(StringResources.INSTAGRAM_MODE_FOUR_MESSAGE_START)
            followers = read_input_file_to_set(Constants.FOLLOWERS_FILE_PATH)
            print(StringResources.INSTAGRAM_FOLLOWER_SET_SIZE.format(len(followers)))
            following = read_input_file_to_set(Constants.FOLLOWING_FILE_PATH)
            print(StringResources.INSTAGRAM_FOLLOWING_SET_SIZE.format(len(following)))
            badFollowers = read_input_file_to_set(Constants.BAD_FOLLOWERS_FILE_PATH)
            print(StringResources.INSTAGRAM_BAD_FOLLOWER_SET_SIZE.format(len(badFollowers)))
            cleanList = read_input_file_to_set(Constants.CLEAN_LIST_FILE_PATH)
            print(StringResources.INSTAGRAM_CLEAN_LIST_SET_SIZE.format(len(cleanList)))

        removeList = badFollowers - cleanList
        print(StringResources.INSTAGRAM_REMOVE_LIST_SIZE.format(len(removeList)))

        # I think insta will action lock the account if we remove more than 600 people
        for person in removeList:
            controller.unfollow_person(person)

            sleep_time = 2 + random.gauss(3,2)
            if (sleep_time < 0):
                sleep_time = 2.2
                
            sleep(sleep_time)
        
        if (mode ^ 4) == 0:
            print(StringResources.INSTAGRAM_MODE_FOUR_MESSAGE)
            return

        if mode&8:
            # Mode 8 will look at actually computing the thot score for the input account

            # For now we will only look at 1 random profile from the badFollowers list
            badList = list(line.strip() for line in open(Constants.BAD_FOLLOWERS_FILE_PATH))
            inspectedAccount = badList[random.randint(0, len(badList) - 1)] 
            print(StringResources.INSTAGRAM_INSPECT_ACCOUNT.format(inspectedAccount))

            thot_rating = controller.get_thot_rating(inspectedAccount)
            print("thot rating for the account - {0} is {1}".format(inspectedAccount, thot_rating))

    except Exception as e:
        print(StringResources.EXCEPTION_MESSAGE.format(e))
    finally:
            print(StringResources.CLOSING_MESSAGE)
            controller.stop_controller()

if __name__ == "__main__":
    main()