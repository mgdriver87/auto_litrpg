
from selenium.webdriver import Firefox, FirefoxProfile
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
from lib.misc.helper_functions import find_chapter_number_alt
import time
import random
import configparser
import os
import re
from pathlib import WindowsPath

config = configparser.ConfigParser()
config.read('config.ini')

texthtml_folder = WindowsPath(config['OUTPUT']['TEXTHTMLFOLDER'].replace('"', ''))
imagehtml_folder = WindowsPath(config['OUTPUT']['IMAGEHTMLFOLDER'].replace('"', ''))
firefoxprofilefolder = WindowsPath(config['INPUT']['FIREFOXPROFILEFOLDER'].replace('"', ''))
scribblelink = config['INPUT']['SCRIBBLEHUBLINK']

semi_auto = False

options = Options()
options.add_argument('--headless')
options.add_argument('-profile')
options.add_argument(str(firefoxprofilefolder))

options.set_preference('dom.webdriver.enabled', True)
options.set_preference('useAutomationExtension', False)

browser = Firefox(options=options)

first_chapter_url = "https://forums.spacebattles.com/threads/dungeon-diver-stealing-a-monster's-power.1154614/page-9"
chapter_folder = WindowsPath(r"C:\\Users\\Hubert Khoo\\Documents\\GitHub\\auto_litrpg\\chapters")
found = False
for path in sorted(os.listdir(chapter_folder), key=find_chapter_number_alt):
    if 'chapter-257.' not in path:
        if found is False:
            continue
    else:
        found = True
    browser.get(first_chapter_url)

    threadmark_label = browser.find_element(By.XPATH, '//input[@name="threadmark_label"]')
    threadmark_label.send_keys(path.replace(".html", "").capitalize())

    text_editor = browser.find_element(By.XPATH, '//div[@contenteditable="true"]')
    html_string = str(open(str(chapter_folder) + "\\" + path, encoding='utf-8').read())
    print(path)

    html_string = html_string.replace("</p>", "</p><p><br></p>") + """<p><hr /></p><p><a href="https://www.patreon.com/KaeNovels" rel=" ugc nofollow">Click Here </a>To read <strong>20 Chapters </strong>ahead on Patreon!&nbsp;</p>"""

    browser.execute_script("arguments[0].innerHTML = String.raw`%s`" % html_string, text_editor)
    text_editor.click()

    submit_button = browser.find_element(By.CSS_SELECTOR, ".button--primary.button.button--icon.button--icon--reply")
    submit_button.click()
    time.sleep(3600)
# next is 
