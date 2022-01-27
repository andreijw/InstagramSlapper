'''
Code to open up my instagram, pull the list of all my followers, and those whom I followers
And remove anyone that does not follow me back
'''

# Standard Imports
import itertools
import json
import os
import requests
import shutil
import sys

from bs4 import BeautifulSoup as bs
from explicit import waiter, XPATH
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from time import sleep

# Custom imports
from Common import Constants
from Common import StringResources
from Library import Validation

# Initialize a chrome browser using the latest chromium driver
# For now the chromedriver.exe must be in the same dir as the python script
def initialize_browser():
     browser = webdriver.Chrome(executable_path=Constants.CHORMIUM_DRIVER_PATH)
     browser.implicitly_wait(5)     
     return browser

# Login to the website using the provided credentials username and password
def login(username, password, browser): 
    browser.get("https://www.instagram.com/accounts/login/")
    sleep(3)

    # Login with my credentials
    browser.find_element_by_name("username").send_keys(username)
    browser.find_element_by_name("password").send_keys(password)
    submit = browser.find_element_by_tag_name('form')
    submit.submit()
    
    # Sleep needed to put in the 2 factor code
    print("Put in 2 fact authentication code if needed")
    sleep(8)
    
    # Click both not now buttons
    browser.find_elements_by_xpath("//button[contains(text(), 'Not Now')]")[0].click()    
    browser.find_elements_by_xpath("//button[contains(text(), 'Not Now')]")[0].click()
    
    # Wait for the user dashboard page to load
    WebDriverWait(browser, 15).until(
        EC.presence_of_element_located((By.LINK_TEXT, "See All")))
        
# Function to either get the number of followers / following for an account        
def get_count_number(account, browser, link, listXPath):
    # Click the Following / Followers link
    browser.find_element_by_partial_link_text(link).click()    
    # Wait for the modal to load    
    waiter.find_element(browser, "//div[@role='dialog']", by=XPATH)    
    totalCount = int((browser.find_element_by_xpath(listXPath).text).replace(',',''))
    
    return totalCount
 
# Scrape the followers/people that follow you for a given account
# 2 Modes -> 1 To get the people that follow you
#         -> 2 To get the people you follow
def scrape_followers(account, browser, mode):
    #Load the page for the account
    print("Loading the account {0}".format(account))
    browser.get("https://www.instagram.com/{0}/".format(account))
    
    link = ""
    listXPath = ""
    
    # If mode == 1 get the people that follow you, else the people you follow
    if mode == 1:
        print("\tLoading the people that I follow")
        link = "following"
        listXPath = "//li[3]/a/span"
        print("\tFollowing found -> ")
    else:
        print("\tLoading the people that follow me")
        link = "followers"    
        listXPath= "//li[2]/a/span"
        print("\tFollowers found ->")
    
    totalCount = get_count_number(account, browser, link, listXPath)
    print("\t{0}".format(totalCount))
    
    # Use CSS to get the nth children
    followerCss = "ul div li:nth-child({}) a.notranslate" 
    peopleSet = set()

    # Create and return a set of all the following/followers
    # We need to scroll the modal in order for the next few followers to load
    try:
        for followerIndex in range(1, totalCount):
            follower = waiter.find_element(browser, followerCss.format(followerIndex))
            followerName = follower.text
            peopleSet.add(followerName)
            print("follower {0} is - {1}".format(followerIndex, followerName))

            browser.execute_script("arguments[0].scrollIntoView();", follower)

    except Exception as e:
        # Sometimes instagram lies, and the follower count is wrong
        print("Insta lied to me {0}".format(type(e).__name__))
    finally:
        return peopleSet
    
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
    
    print("Wrote the content to the file - {0}".format(outputFile))
    sleep(1)

# Function to download an image from the source path    
def download_image(urlPath, destPath):
    img_content = requests.get(urlPath).content
    with open(destPath, 'wb') as handler:
        handler.write(img_content)

# Function to get the profile pic and the first 4 human posts
def get_images(browser, account):
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
    
# Runner function for the insta-thot-remover
def main():
    try:
        print(StringResources.INTRO_TEXT)
        
        username = ''
        password = ''
        mode = 1
        browser = None
        follwing, followers, badFollowers, removeList, cleanList = set(), set(), set(), set(), set()

        # Basic Usage, provide the username, password, and mode to run (0,1)
        if not Validation.validate_login(sys.argv):
            print(StringResources.INVALID_USAGE_MODE)
            return
        
        username = sys.argv[1]
        password = sys.argv[2]
        mode = int(sys.argv[3])
        print(StringResources.VALID_INPUT_DATA)
        return
        
        # Initialize the chrome browser object
        browser = initialize_browser()       
        
        # Login to insta with the input username and password
        login(username, password, browser)
        sleep(1)
        print("Logged in into the account {0} | password {1} | mode {2}"\
        .format(username, password, mode))
        
        # Use bitwise operator on the mode to perform the following functionality
        # &1 -> Get Followers of the account
        # &2 -> Get People the account follows
        # &3 -> Get Bad Followers (People that don't follow you back) + &1 & &2 obv
        # &4 -> Read in from local files Followers.txt, Following.txt and BadFollowers.txt
 
        if mode&1:
            # Use mode 2 in the scrape func to get a list of people that follow an account
            followers = scrape_followers(username, browser, 2)     
            print("The total account followers are: ", len(followers))
            write_output_to_file(followers, followersFile)
            
            if (mode ^ 1) == 0:
                print("Mode is set to 1. Only obtaining the followers set")
                return
        
        if mode&2:
            # Get the people that the account follows
            following = scrape_followers(username, browser, 1)
            print("Number of people the account follows", len(following))
            write_output_to_file(following, followingFile)
            
            if (mode ^ 2) == 0:
                print("Mode is set to 2. Only obtaining the following set")
                return

        if mode&3:
            # Set A is my followers, set B is the people I follow
            # A bad follower is defined by me as someone that I follow but does not follow me back
            # We can easily find this with Set Theory. Set Difference B - A
            # which will be all the elements in Set B (I follow) and are not in Set A (follow me)
            print("Getting people that don't follow me back")
            badFollowers = following - followers
            print("Number of people not following me", len(badFollowers))
            write_output_to_file(badFollowers, badFollowersFile)
            
            if (mode ^ 3) == 0:
                print("Mode is set to 3. Only obtaining the badFollowers set")
                return
        
        # Read in the clean list of people not to unfollow
        cleanList = set(line.strip() for line in open(cleanListFile))
        
        if mode&4:
            print("Mode set to 4, reading in from the files")
            followers = set(line.strip() for line in open(followersFile))
            print("Length of followers set - {0}".format(len(followers)))
            following = set(line.strip() for line in open(followingFile))
            print("Length of following set - {0}".format(len(following)))
            badFollowers = set(line.strip() for line in open(badFollowersFile))
            print("Length of badFollowers set - {0}".format(len(badFollowers)))
        
        print("Logging in into the account {0} | password {1} | running with mode {2}"\
        .format(username, password, mode))
            
        removeList = badFollowers - cleanList
        print("Filtered out the clean list followers about to remove {0}".format(len(removeList)))
        
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
        print("An error ocurred while running the bot | {0}".format(e))
    finally:
        if browser is not None:
            exit(browser)

# Exit and cleanup 
def exit(browser):
    print("Closing the instagram bot")
    browser.quit()
    
if __name__ == "__main__":
    main()