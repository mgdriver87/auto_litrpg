
from selenium.webdriver import Firefox, FirefoxProfile
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
from lib.misc.helper_functions import find_chapter_number
import time
import random
import configparser
import os
import re
from pathlib import WindowsPath

config = configparser.ConfigParser()
config.read('config.ini')

semi_auto = False

options = Options()
#options.add_argument('--headless')
options.add_argument('-profile')
options.add_argument("/home/uberchio/.mozilla/firefox/t9ahc2ik.default-release")

options.set_preference('dom.webdriver.enabled', True)
options.set_preference('useAutomationExtension', False)

browser = Firefox(options=options)

first_chapter_url = "https://www.scribblehub.com/addchapter/1217468/"
chapter_folder = "/home/uberchio/Documents/auto_litrpg/input/output"
found = False
for path in sorted(os.listdir(chapter_folder), key=find_chapter_number):
    print(path)
    browser.get(first_chapter_url)
    html_string = str(open(str(chapter_folder) + "/" + path, encoding='utf-8').read())
    input_title = browser.find_element(By.ID, "chapter-title")
    input_title.click()
    input_title.send_keys(path.split(".")[0])
    browser.switch_to.frame("edit_mycontent_chapter_ifr")
    text_editor = browser.find_element(By.ID, "tinymce") 

    browser.execute_script("arguments[0].innerHTML = String.raw`%s`" % html_string, text_editor)
    text_editor.click()
    #text_editor = browser.find_element(By., "tinymce") 
    browser.switch_to.default_content()
    pub_btn = browser.find_element(By.XPATH, "/html[1]/body[1]/div[3]/div[1]/div[1]/div[2]/div[1]/div[2]/div[2]/span[1]")
    pub_btn.click()
    time.sleep(10)
# next is 
