'''
Code to open up my instagram, pull the list of all my followers, and those whom I followers
And remove anyone that does not follow me back
'''

# Standard Imports
import sys

from time import sleep

# Custom imports
from Common import Constants, StringResources
from Library import Validation, Browser, InstagramController
    
# Function to unfollow the given person
def unfollow_person(account, browser):
    #Load their page and unfollow them
    browser.get("https://www.instagram.com/{0}/".format(account))
    
    print("\tUnfollowing {0}".format(account))
    try:
        WebDriverWait(browser, 2).until(EC.presence_of_element_located((By.XPATH, "//*[contains(@aria-label, 'Following')]"))).click()
        browser.find_element_by_xpath("//button[contains(text(), 'Unfollow')]").click()
    except Exception as e:
        print("Error unfollowing - {0} | {1}".format(account, e))
        return

# Write the input peopleSet into the output text file
def write_output_to_file(peopleSet, outputFile):
    with open(outputFile, 'w') as f:
        for follower in peopleSet:
            f.write("%s\n" % follower)
    
    print(StringResources.INSTAGRAM_TEXT_OUTPUT_MESSAGE.format(outputFile))
    sleep(1)

# Function to download an image from the source path    
def download_image(urlPath, destPath):
#import requests
    img_content = requests.get(urlPath).content
    with open(destPath, 'wb') as handler:
        handler.write(img_content)

# Function to get the profile pic and the first 4 human posts
def get_images(browser, account):
#import shutil
#import os
    account = "andrei_j_w"
    print("Getting images from the account {0}".format(account))
    tags = set()
    captions = set()
    post_frequency = 0
    
    try:
        # Create images dir
        images_dir_path = "./images"
        if os.path.isdir(images_dir_path):
            shutil.rmtree(images_dir_path)

        os.mkdir(images_dir_path)

        # Get the profile pic
        browser.get("https://www.instagram.com/{0}/".format(account))
        source_url = browser.find_element_by_xpath("//img[contains(@class,'_6q-tv')]").get_attribute("src")
        download_image(source_url, "{0}/profile.png".format(images_dir_path))
        
        images = browser.find_elements_by_xpath("//img[contains(@class,'FFVAD')]")
        stop_index = 4
        # Get the first images available up to the stop_index
        for count, image in enumerate(images):
            source_url = image.get_attribute("src")
            download_image(source_url, "{0}/image{1}.png".format(images_dir_path, count))
            
            if count >= stop_index:
                break
        
        print("Downloaded the profile pic and first 4 image potsts")
        
        return (tags, captions, post_frequency)

    except Exception as e:
        print("Error while getting the account images {0}".format(e))
    
    return (set(), set(), 0)

# Using tesnorlow, opencv-python, keras, imageAI
def get_thot_rating(browser, account):
    # Calculate a weighted average thot_rating score of the profile pic + 4 images
    # Get post frequency in last month, tags thot_ratinga and captions thot_rating
    tags, captions, post_frequency = get_images(browser, account)
    
    # Get follower / following ratio
    followerCount = get_count_number(account, browser, "followers", "//li[2]/a/span" )
    followingCount = get_count_number(account, browser, "following", "//li[3]/a/span")
    followerRatio = followerCount / followingCount
    
    # Compute thot rating. Will use this as features into a ml model
    thot_rating = followerRatio
    
    return thot_rating
    
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
            
            if (mode ^ 3) == 0:
                print(StringResources.INSTAGRAM_MODE_THREE_MESSAGE)
                return
        
        # Read in the clean list of people not to unfollow
        cleanList = set(line.strip() for line in open(Constants.CLEAN_LIST_FILE_PATH))
        
        if mode&4:
            print(Constants.INSTAGRAM_MODE_FOUR_MESSAGE)
            followers = set(line.strip() for line in open(followersFile))
            print(StringResources.INSTAGRAM_FOLLOWER_SET_SIZE.format(len(followers)))
            following = set(line.strip() for line in open(followingFile))
            print(StringResources.INSTAGRAM_FOLLOWING_SET_SIZE.format(len(following)))
            badFollowers = set(line.strip() for line in open(badFollowersFile))
            print(INSTAGRAM_BAD_FOLLOWER_SET_SIZE.format(len(badFollowers)))

        removeList = badFollowers - cleanList
        print(StringResources.INSTAGRAM_REMOVE_LIST_SIZE.format(len(removeList)))
        
        return
        # I think insta will action lock the account if we remove more than 600 people
        for person in removeList:
            unfollow_person(person, browser)
            sleep(10)
        
        if (mode ^ 4) == 0:
            print("Mode was set to 4. Exiting after removing the bad followers")
            return
            
        if mode&8:
            # Remove thots
            # For now we will only look at 1 profile
            # lolaloliitaaa
            # Look at the first 5 images and compute the thot score
            
            inspectedAccount = "lolaloliitaaa"
            thot_rating = get_thot_rating(browser, inspectedAccount)
            print("thot rating for the account - {0} is {1}".format(inspectedAccount, thot_rating))

    except Exception as e:
        print(StringResources.EXCEPTION_MESSAGE.format(e))
    finally:
            print(StringResources.CLOSING_MESSAGE)
            controller.stop_controller()

if __name__ == "__main__":
    main()