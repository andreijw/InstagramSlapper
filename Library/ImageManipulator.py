"""
ImageManipulator.py

This file will serve to manipulate instagram images
"""

import os
import requests
import shutil

from Common import StringResources

class ImageManipulator:

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
    Obtain the metadata for the input account
    '''
    def get_images_metadata(self, account):
        return (set(), set(), 0)
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