import os
from lib.misc.helper_functions import find_chapter_number_md
import pypandoc

chapter_folder = "/home/uberchio/Documents/Stories/Novels/Black Market/Book 2/Chapters"
print("hello")
#os.listdir(chapter_folder)
text = ""
counter = 1
part_counter = 1
for path in sorted(os.listdir(chapter_folder), key=find_chapter_number_md):

    filename = chapter_folder + "/" + path
    with open(filename, "r") as f:
        text += "# " + path.split(".")[0] + "\n\n"
        for line in f.readlines():
            if len(line) <= 0 or line == "\n":
                continue
            line = line.replace("<", "< ")
            line = line.replace(">", " >")
            text += line + "\n"
    counter += 1
    if counter % 15 == 0:
        with open("inter_%d.md" % part_counter, "w") as f:
            f.write(text)
            f.close()
            text = ""
        part_counter += 1
with open("inter_%d.md" % (part_counter+1), "w") as f:
    f.write(text)
    f.close()
    
#pypandoc.convert_file("inter.md", to='docx', outputfile='result.docx')

    
