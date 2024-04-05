from selenium.webdriver import Firefox, FirefoxProfile
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options

import time
import configparser
import os
from pathlib import WindowsPath

html_string = open('content.html').read().split("<p>")

new_string_list = []
links_to_edit = []


for i in range(len(html_string)):
    if 'Chapter' not in html_string[i]:
        continue
    elif 'Birth' in html_string[i]:
        continue

    previous_string = html_string[i-1].replace("</p>", "")
    if i == len(html_string) - 1:
        next_string = "To be continued!"
    else:
        next_string = html_string[i+1].replace("</p>", "")
    table_content_string = """<a href="https://www.patreon.com/posts/table-of-101482128">Table of Contents</a>"""
    link = html_string[i].split("\"")[1]
    links_to_edit.append(link)
    new_string_list.append("<p><---" + previous_string + "|" +  table_content_string + "|" + next_string + "---></p>")

with open('output.html', 'w') as f:
    for j in new_string_list:
        f.write(j)
config = configparser.ConfigParser()
config.read('config.ini')

firefoxprofilefolder = WindowsPath(config['INPUT']['FIREFOXPROFILEFOLDER'].replace('"', ''))
options = Options()

options.add_argument('-profile')
options.add_argument(str(firefoxprofilefolder))

options.set_preference('dom.webdriver.enabled', True)
options.set_preference('useAutomationExtension', False)

browser = Firefox(options=options)

for k in range(len(new_string_list)):
    if k < 46:
        continue
    browser.get(links_to_edit[k] + "/edit")
    print("iteration: " + str(k) + links_to_edit[k])
    time.sleep(3)
    #print(browser.page_source)
    patreon_editor = browser.find_element(By.CLASS_NAME, "ProseMirror")
    #print(browser.page_source)
    inner_string = patreon_editor.get_attribute("innerHTML")
    
    # check if table of contents exist.
    inner_string_split = inner_string.split("<p>")
    if 'patreon.com' in inner_string_split[1]:
        #print('already have top!')
        addon_top_string = '<p></p>'
    else:
        addon_top_string = new_string_list[k] + '<p></p>'
    
    if 'patreon.com' in inner_string_split[-1]:
        #print('already have btm!')
        addon_btm_string = '<p></p>'
    else:
        addon_btm_string = new_string_list[k] + '<p></p>'

    html_string = addon_top_string + inner_string + addon_btm_string
    browser.execute_script("""arguments[0].innerHTML = String.raw`%s`""" % html_string, patreon_editor)
    patreon_editor.click()

    btns = browser.find_elements(By.CSS_SELECTOR, ".sc-iCfMLu.cRkIlM")
    for e in btns:
        if 'Next' in e.text:
            e.click()
            time.sleep(2)
            e.click()

    time.sleep(3)

    
    