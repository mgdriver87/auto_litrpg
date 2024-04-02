# step 1, import
import configparser
import mammoth
import os
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

# step 2.5, define chapter number range

specific = False
specific_chapter = '154'

# step 2.6, setup stats class
persistant_stats = stats.Stats()

# step 3, walk (loop) through chapter folder designated by configfile
for path in sorted(os.listdir(chapter_folder), key=find_chapter_number):
    
    # check if its a word document
    # TODO: fix to check for markdown too
    if path.find(".docx") == -1:
        continue

    # found a good chapter.
    filename = str(chapter_folder) + "\\" + path

    # create a pickle filename for the binary stats to be saved.
    pickle_file_path = filename.split("\\")[-1].replace('.docx', '').replace('Chapter', '')

    #within the image folder, we try to make a specific chapter image folder

    # create the image folder
    chapter_image_folder_name = str(image_folder) + "\\" + path.split("-")[0].strip(" ")
    try:
        os.makedirs(chapter_image_folder_name)
    except FileExistsError:
        0
    
    #TODO: improve specific function
    if specific:
        # load pickle stats from previous chapter
        # find the closest pickle stats
        if (specific_chapter not in filename):
            continue
    
    if specific:
        # replace template stats
        persistant_stats = load_file(pickle_file_path)
        if persistant_stats == -1:
            raise Exception("loading failed!")
        print("hello")

    # convert the current word document into html
    
    try:
        if ("$" not in filename):
            document = mammoth.convert_to_html(open(filename, 'rb'))
    except:
        print(filename)
        print("failure!!")
        raise Exception
        break

    # create html
    
    create_html(document, path, imagehtml_folder, chapter_image_folder_name, pickle_file_path, persistant_stats, text=False)

    persistant_stats = create_html(document, path, texthtml_folder, chapter_image_folder_name, pickle_file_path, persistant_stats, text=True)
