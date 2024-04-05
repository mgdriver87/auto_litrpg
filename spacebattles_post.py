
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

#texthtml_folder = WindowsPath(config['OUTPUT']['TEXTHTMLFOLDER'].replace('"', ''))
#imagehtml_folder = WindowsPath(config['OUTPUT']['IMAGEHTMLFOLDER'].replace('"', ''))

semi_auto = False

options = Options()
#options.add_argument('--headless')
options.add_argument('-profile')
options.add_argument('/home/uberchio/.mozilla/firefox/t9ahc2ik.default-release')

options.set_preference('dom.webdriver.enabled', True)
options.set_preference('useAutomationExtension', False)

browser = Firefox(options=options)

first_chapter_url = "https://forums.spacebattles.com/threads/dungeon-diver-stealing-a-monster's-power.1154614/"
#fiction_url

# first we post scribblehub.
for path in sorted(os.listdir("/home/uberchio/Documents/auto_litrpg/chapters"), key=find_chapter_number_alt):
    browser.get(first_chapter_url)

    threadmark_label = browser.find_element(By.XPATH, "/html[1]/body[1]/div[1]/div[2]/div[2]/div[5]/div[1]/div[3]/div[2]/div[1]/div[2]/form[1]/div[1]/div[1]/div[1]/div[1]/div[2]/dl[1]/dd[1]/input[1]")
    threadmark_label.send_keys(path.replace(".html", "").capitalize())

    text_editor = browser.find_element(By.XPATH, "/html[1]/body[1]/div[1]/div[2]/div[2]/div[5]/div[1]/div[3]/div[2]/div[1]/div[2]/form[1]/div[1]/div[1]/div[1]/div[1]/div[2]/div[1]/div[1]/div[2]/div[1]")
    html_string = str(open("/home/uberchio/Documents/auto_litrpg/chapters/" + path).read())

    html_string = html_string.replace("</p>", "</p><p><br></p>") + """<p><hr /></p><p><a href="https://www.patreon.com/KaeNovels" rel=" ugc nofollow">Click Here </a>To read <strong>20 Chapters </strong>ahead on Patreon!&nbsp;</p>"""

    browser.execute_script("arguments[0].innerHTML = String.raw`%s`" % html_string, text_editor)
    text_editor.click()

    submit_button = browser.find_element(By.CSS_SELECTOR, ".button--primary.button.button--icon.button--icon--reply")
    #submit_button.click()
    time.sleep(6000)
# next is 
