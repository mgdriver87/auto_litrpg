
from selenium.webdriver import Firefox, FirefoxProfile
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
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
options.add_argument('--headless')
options.add_argument('-profile')
options.add_argument('/home/uberchio/.mozilla/firefox/t9ahc2ik.default-release')

options.set_preference('dom.webdriver.enabled', True)
options.set_preference('useAutomationExtension', False)

browser = Firefox(options=options)

first_chapter_url = 'https://www.royalroad.com/fiction/64223/dungeon-diver-stealing-a-monsters-power/chapter/1499551/chapter-377'
#fiction_url

# first we post scribblehub.
browser.get(first_chapter_url)
time.sleep(3)
page_content = browser.find_element(By.CLASS_NAME, "chapter-inner")
#print(page_content.get_attribute('innerHTML'))
portlet_content = browser.find_element(By.CLASS_NAME, "portlet-body").get_attribute('innerHTML')
link = re.findall(r"""(href=.+Next)""", portlet_content)
for i in link:
    if 'patreon.com' in i:
        continue
    else:
        next_link = i
print("https://www.royalroad.com"+next_link.split("\"")[1])
next_link = "https://www.royalroad.com"+next_link.split("\"")[1]
chapter_name = first_chapter_url.split("/")[-1]

with open("/home/uberchio/Documents/auto_litrpg/chapters/" + chapter_name + ".html", 'w') as f:
    f.write(page_content.get_attribute('innerHTML'))

while True:
    try:
        browser.get(next_link)
    except:
        time.sleep(60000)
    chapter_name = next_link.split("/")[-1]
    page_content = browser.find_element(By.CLASS_NAME, "chapter-inner").get_attribute('innerHTML')
    #print(page_content.get_attribute('innerHTML'))
    portlet_content = browser.find_element(By.CLASS_NAME, "portlet-body").get_attribute('innerHTML')
    link = re.findall(r"""(href=.+Next)""", portlet_content)
    for i in link:
        if 'patreon.com' in i:
            continue
        else:
            next_link = i
    print("https://www.royalroad.com"+next_link.split("\"")[1])
    next_link = "https://www.royalroad.com"+next_link.split("\"")[1]
    #chapter_name = next_link.split("/")[-1]

    with open("/home/uberchio/Documents/auto_litrpg/chapters/" + chapter_name + ".html", 'w') as f:
        f.write(page_content)


# next is 
