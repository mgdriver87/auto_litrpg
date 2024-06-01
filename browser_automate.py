
from selenium.webdriver import Firefox, FirefoxProfile
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
import time
import random
import configparser
import os
from pathlib import WindowsPath
from lib.misc.helper_functions import find_chapter_number, load_file

config = configparser.ConfigParser()
config.read('config.ini')

texthtml_folder = WindowsPath(config['OUTPUT']['TEXTHTMLFOLDER'].replace('"', ''))
imagehtml_folder = WindowsPath(config['OUTPUT']['IMAGEHTMLFOLDER'].replace('"', ''))
firefoxprofilefolder = WindowsPath(config['INPUT']['FIREFOXPROFILEFOLDER'].replace('"', ''))
scribblelink = config['INPUT']['SCRIBBLEHUBLINK']

semi_auto = False

options = Options()

options.add_argument('-profile')
options.add_argument(str(firefoxprofilefolder))

options.set_preference('dom.webdriver.enabled', True)
options.set_preference('useAutomationExtension', False)

browser = Firefox(options=options)
found = False
#time.sleep(3600)
# first we post scribblehub.
for path in sorted(os.listdir(imagehtml_folder), key=find_chapter_number):
    if '65' not in path:
        if found is False:
            continue
        else:
            0
    else:
        found = True
    
    if '66' in path:
        raise Exception
    print(path)
    chapter_title  = path.replace('.html', '')
    browser.get("https://www.scribblehub.com/addchapter/1047104/")

    # then we add chapter title. 
    title_input = browser.find_element(By.ID, "chapter-title")
    title_input.send_keys(chapter_title)

    # then we modify the inner html of the chapter itself to put image html in. 
    browser.switch_to.frame("edit_mycontent_chapter_ifr")
    text_editor = browser.find_element(By.CSS_SELECTOR, "body")
    filename = str(imagehtml_folder) + "\\" + path
    html_string = str(open(filename, encoding="utf-8").read())

    browser.execute_script("arguments[0].innerHTML = String.raw`%s`" % html_string, text_editor)

    # then switch back to default content
    browser.switch_to.default_content()

    if semi_auto:
        0
    else:
        # back in the default view, we click Publish!
        publish_button = browser.find_element(By.ID, "pub_chp_btn")
        publish_button.click()
    time.sleep(3600)


# next is 
