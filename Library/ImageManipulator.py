"""
ImageManipulator.py

This file will serve to manipulate instagram images
"""

import os
import requests
import shutil
from time import sleep

from Common import StringResources, Constants

class ImageManipulator:

    '''
    Safely delete the temp image directory and it's contents if it exists
    '''
    def delete_image_dir(self):
        try:
            if os.path.isdir(Constants.IMAGE_TEMP_DIRECTORY):
                shutil.rmtree(Constants.IMAGE_TEMP_DIRECTORY)
        except Exception as e:
            print(StringResources.INSTAGRAM_IMAGE_DIR_DELETION_ERROR.format(e))

    '''
    Create the temp image directory
    '''
    def create_image_dir(self):
        try:
            self.delete_image_dir()
            os.mkdir(Constants.IMAGE_TEMP_DIRECTORY)
        except Exception as e:
            print(StringResources.INSTAGRAM_IMAGE_DIR_CREATION_ERROR.format(e))
    
    '''
    Helper function to download an image from the source path into the dest path
    '''    
    def download_image(self, urlPath, destPath):
        try:
            img_content = requests.get(urlPath).content
            with open(destPath, 'wb') as handler:
                handler.write(img_content)
        except Exception as e:
            print(StringResources.INSTAGRAM_IMAGE_DOWNLOAD_ERROR.format(urlPath, e))
            
    '''
    Obtain the metadata for the input account. Tags, Captions, Post frequency.
    Also downloads the profile and last 5 images
    '''
    def get_images_metadata(self, account, browser):
        print(StringResources.INSTAGRAM_PROCESSING_METADATA_MESSAGE.format(account))
        tags, captions = set(), set()
        post_frequency = 0
        
        try:
            self.create_image_dir()

            # Get the profile pic
            browser.get_website(Constants.INSTAGRAM_FORMATTABLE_URL.format(account))
            source_url = browser.find_elements_by_x_path(Constants.IMAGE_SOURCE_XPATH, 1).get_attribute(Constants.IMAGE_SOURCE_ATTRIBUTE)
            self.download_image(source_url, Constants.IMAGE_DOWNLOAD_PROFILE_NAME.format(Constants.IMAGE_TEMP_DIRECTORY))
            
            sleep(3)
            return (set(), set(), 1) 
            images = browser.find_elements_by_xpath("//img[contains(@class,'FFVAD')]")
            stop_index = 4
            # Get the first images available up to the stop_index
            for count, image in enumerate(images):
                source_url = image.get_attribute("src")
                download_image(source_url, "{0}/image{1}.png".format(Constants.IMAGE_TEMP_DIRECTORY, count))
                
                if count >= stop_index:
                    break
            
            print("Downloaded the profile pic and first 4 image potsts")
            
            self.delete_image_dir()
            return (tags, captions, post_frequency)

        except Exception as e:
            print("Error while getting the account images {0}".format(e))
        
        self.delete_image_dir()
        return (set(), set(), 0)