# step 1, import
import configparser
import mammoth
import os
import re
from pathlib import WindowsPath
from lib.misc.helper_functions import find_chapter_number, load_file
from lib.RPG import stats
from lib.gen.html_gen import create_html

# step 2, load config file

config = configparser.ConfigParser()
config.read('config.ini')

chapter_folder = WindowsPath(config['INPUT']['CHAPTERFOLDER'].replace('"', ''))
image_folder = WindowsPath(config['INTERMEDIATE']['IMAGEFOLDER'].replace('"', ''))
template_folder = WindowsPath(config['INTERMEDIATE']['TEMPLATEFOLDER'].replace('"', ''))
texthtml_folder = WindowsPath(config['OUTPUT']['TEXTHTMLFOLDER'].replace('"', ''))
imagehtml_folder = WindowsPath(config['OUTPUT']['IMAGEHTMLFOLDER'].replace('"', ''))

# step 3, walk (loop) through chapter folder designated by configfile
for path in sorted(os.listdir(imagehtml_folder), key=find_chapter_number):
    html_as_string = ''
    with open(str(imagehtml_folder) + "\\" + path, 'r', encoding='utf-8') as file:  # r to open file in READ mode
        html_as_string = file.read()
    
    html_as_string = re.sub("<br />", "</p><p>", html_as_string)

    with open(str(imagehtml_folder) + "\\" + path, 'w', encoding='utf-8') as file:
        file.write(html_as_string)
