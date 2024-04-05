
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

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

options = webdriver.ChromeOptions()
options.add_argument(r"--user-data-dir=C:\Users\Hubert Khoo\AppData\Local\Google\Chrome\User Data") #e.g. C:\Users\You\AppData\Local\Google\Chrome\User Data
options.add_argument(r'--profile-directory=Profile 1') #e.g. Profile 3
#options.add_argument('--headless')
options.add_argument("--remote-debugging-port=9222") 
options.add_argument("start-maximized") # open Browser in maximized mode
options.add_argument("disable-infobars") # disabling infobars
options.add_argument("--disable-extensions") # disabling extensions
options.add_argument("--disable-gpu") # applicable to windows os only
options.add_argument("--disable-dev-shm-usage") #overcome limited resource problems
options.add_argument("--no-sandbox") # Bypass OS security model
browser = webdriver.Chrome(options=options)
#browser.get("https://www.moonquillnovels.com/dashboard/books/1137/chapters/new")

found = False
for path in sorted(os.listdir(imagehtml_folder), key=find_chapter_number):
    if '3' not in path:
        if found is False:
            continue
        else:
            0
    else:
        found = True
    browser.get("https://www.moonquillnovels.com/dashboard/books/1137/chapters/new")
    time.sleep(2)

    print(path)
    chapter_title  = path.replace('.html', '')
    time.sleep(1)
    title_input = browser.find_element(By.ID, "ch_name")
    title_input.send_keys(chapter_title)

    #chap_num = chapter_title.split("-")[0].split(" ")[-1]
    #chap_num_input = browser.find_element(By.ID, "num")
    #chap_num_input.send_keys(chap_num)
    time.sleep(1)
    chapter_input = browser.find_element(By.CSS_SELECTOR, ".ql-editor")
    filename = str(imagehtml_folder) + "\\" + path
    html_string = str(open(filename, encoding="utf-8").read())

    # modify the string for linebreaks
    html_string = html_string.replace("</p>", "</p><p><br></p>")

    #print(html_string)

    browser.execute_script("arguments[0].innerHTML = String.raw`%s`" % html_string, chapter_input)

    print("Waiting to hit publish on MQ!\r\n")

    publish_button = browser.find_element(By.ID, "publish")
    publish_button.click()
    
    time.sleep(3600*5)