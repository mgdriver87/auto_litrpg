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

# first convert all to md.

book1_chapter_folder = WindowsPath(config['INPUT']['BOOK_1_CH_FOLDER'].replace('"', ''))

combined_book1_ch_name = "BlackMarket Book 1 (TEXT).docx"
combined_doc = ""
persistant_stats = stats.Stats()

for path in sorted(os.listdir(book1_chapter_folder), key=find_chapter_number):
    # take all text inside and convert it into text form in a separate doc.
    print(path)
    # check if its a word document
    # TODO: fix to check for markdown too
    if path.find(".docx") == -1:
        continue

    # found a good chapter.
    filename = str(book1_chapter_folder) + "\\" + path

    # create a pickle filename for the binary stats to be saved.
    pickle_file_path = filename.split("\\")[-1].replace('.docx', '').replace('Chapter', '')

    #within the image folder, we try to make a specific chapter image folder

    # create the image folder
    chapter_image_folder_name = str(image_folder) + "\\" + path.split("-")[0].strip(" ")

    try:
        if ("$" not in filename):
            document = mammoth.convert_to_html(open(filename, 'rb'))
    except:
        print(filename)
        print("failure!!")
        raise Exception
        break

    #print(document.value)
    document = document.value.replace("""[Stats Table]""", "[Stats Table]<p></p>")
    document = document.replace("""<p>* * *</p>""", """<p style="text-align: center;">* * *</p>""")
    #document = document.value.replace("<br />", "<p></p>")
    #document = document.replace("""@@@""", "***")

    persistant_stats = create_html(document, path, texthtml_folder, chapter_image_folder_name, pickle_file_path, persistant_stats, text=True)

