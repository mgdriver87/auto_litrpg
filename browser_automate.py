
from selenium.webdriver import Firefox, FirefoxProfile
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
import time
import random
import configparser
import os
from pathlib import WindowsPath

config = configparser.ConfigParser()
config.read('config.ini')

texthtml_folder = WindowsPath(config['OUTPUT']['TEXTHTMLFOLDER'].replace('"', ''))
imagehtml_folder = WindowsPath(config['OUTPUT']['IMAGEHTMLFOLDER'].replace('"', ''))

semi_auto = False

options = Options()

options.add_argument('-profile')
options.add_argument('/home/uberchio/.mozilla/firefox/t9ahc2ik.default-release')

options.set_preference('dom.webdriver.enabled', True)
options.set_preference('useAutomationExtension', False)

browser = Firefox(options=options)

# first we post scribblehub.
browser.get('https://scribblehub.com/addchapter/1047104')


# then we add chapter title. 
title_input = browser.find_element(By.ID, "chapter-title")
title_input.send_keys("Chapter Title")

# then we modify the inner html of the chapter itself to put image html in. 
browser.switch_to.frame("edit_mycontent_chapter_ifr")
text_editor = browser.find_element(By.CSS_SELECTOR, "body")
html_string = str(open("Chapter 23 - Industrialization.html").read())

browser.execute_script("arguments[0].innerHTML = '%s'" % html_string, text_editor)

# then switch back to default content
browser.switch_to.default_content()

if semi_auto:
    0 # do nothing and let author manual control
else:
    # back in the default view, we click Publish!
    publish_button = browser.find_element(By.ID, "pub_chp_btn")

browser.switch_to.new_window('tab')

browser.get('')


# next is 
