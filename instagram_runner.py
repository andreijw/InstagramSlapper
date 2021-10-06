'''
Code to open up my instagram, pull the list of all my followers, and those whom I followers
And remove anyone that does not follow me back
'''
import itertools
import sys

from explicit import waiter, XPATH
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from time import sleep

# Initialize a chrome browser using the latest chromium driver
# For now the chromedriver.exe must be in the same dir as the python script
def initialize_browser():
     browser = webdriver.Chrome(executable_path=".\\chromedriver.exe")
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
    
    # Click both not now buttons
    browser.find_elements_by_xpath("//button[contains(text(), 'Not Now')]")[0].click()    
    browser.find_elements_by_xpath("//button[contains(text(), 'Not Now')]")[0].click()
    
    # Wait for the user dashboard page to load
    WebDriverWait(browser, 15).until(
        EC.presence_of_element_located((By.LINK_TEXT, "See All")))
 
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
    
    # Click the Following / Followers link
    browser.find_element_by_partial_link_text(link).click()    
    # Wait for the modal to load    
    waiter.find_element(browser, "//div[@role='dialog']", by=XPATH)    
    totalCount = int(browser.find_element_by_xpath(listXPath).text)
    print("\t{0}".format(totalCount))
    
    # Use the  CSS nth-child behavior to get n children
    follower_css = "ul div li:nth-child({}) a.notranslate" 
    peopleSet = set()
    
    # Create and return a set of all the following/followers
    # Insta loads the followers by groups
    # force the modal to scroll down to the next group
    stepSize = 6
    for instaGroup in itertools.count(start=1, step=stepSize):
        for followerIndex in range(instaGroup, instaGroup + stepSize):
            # Avoid index out of bounds
            if followerIndex > totalCount:
                return peopleSet
                
            followerName = waiter.find_element(browser, follower_css.format(followerIndex)).text
            peopleSet.add(followerName)
            print("follower {0} is - {1}".format(followerIndex, followerName))
            
        # We should scroll past the last follower we found
        lastFollower = waiter.find_element(browser, follower_css.format(instaGroup+stepSize-1))
        #print("last follower is - {0}".format(lastFollower.text))
        browser.execute_script("arguments[0].scrollIntoView();", lastFollower)
        sleep(1)
    
    # If there is no one in the set. Big F if no one follows you my dude
    return peopleSet
    
# Function to unfollow the given person
def unfollow_person(account, browser):
    #Load their page and unfollow them
    browser.get("https://www.instagram.com/{0}/".format(account))
    
    print("\tUnfollowing {0}".format(account))
    try:
        browser.find_elements_by_xpath("//button[contains(@class, '_5f5mN    -fzfL     _6VtSN     yZn4P   ')]")[0].click()
        browser.find_elements_by_xpath("//button[contains(text(), 'Unfollow')]")[0].click()
    except Exception as e:
        print("Error unfollowing - {0} | {1}".format(account, e))
        return
    
# Runner function
def main():
    try:
        print("Starting instagram bot")
        
        username = ''
        password = ''
        mode = 0
        browser = None
        instagram_url = "https://www.instagram.com/"
        
        # Basic Usage, provide the username, password, and mode to run (0,1)
        if len(sys.argv) != 4:
            print("Invalid Usage. - Please try again, usage: Username, Password, \
            Mode (0 - Get Bad Followers / 1 - Get and unfollow bad followers)")
            return
        
        username = sys.argv[1]
        password = sys.argv[2]
        mode = int(sys.argv[3])

        print("Logging in into the account {0} | password {1} | running with mode {2}"\
        .format(username, password, mode) )
        
        # Initialize the chrome browser object
        browser = initialize_browser()

        # Login to insta
        login(username, password, browser)
        sleep(1)
        print("Logged in into the account {0} | password {1}"\
        .format(username, password) )

        # Get a list of people that follow me. Mode 2 gets the people that follow me
        followers = scrape_followers(username, browser, 2)     
        print("My total followers: ", len(followers))
        sleep(2)        
        return
    
        # Get the people that I follow
        following = scrape_followers(username, browser, 1)
        print("Number of people following me", len(following))
        sleep(1)

        return
        # Set A is my followers, set B is the people I follow
        # A bad follower is defined by me as someone that I follow but does not follow me back
        # We can easily find this with Set Theory. Set Difference B - A
        # which will be all the elements in Set B (I follow) and are not in Set A (follow me)
        print("Getting people that don't follow me back")
        bad_followers = following - followers
        print("Number of people not following me", len(bad_followers))    
        
        # Print the list to an output file so that I can perform a holistic review 
        # For isntance if they are hot af, I might keep them :)
        outputFile = "BadFollowers.txt"
        
        with open(outputFile, 'w') as f:
            for follower in bad_followers:
                f.write("%s\n" % follower)
        
        print("Wrote the content to the file - {0}".format(outputFile))
        sleep(1)
        
        # Read in the clean list of people not to unfollow
        cleanList = set(line.strip() for line in open("WhiteList.txt"))
        
        removeList = bad_followers - cleanList
        print(len(removeList))
        print("Filtered out the clean list")
        
        for person in removeList:
            unfollow_person(person, browser)
            sleep(2)

    except Exception as e:
        print("An error ocurred while running the bot, exiting - ")
        print(e)
    finally:
        if browser is not None:
            exit(browser)

# Exit and cleanup 
def exit(browser):
    print("Closing the instagram bot")
    browser.quit()
    
if __name__ == "__main__":
    main()