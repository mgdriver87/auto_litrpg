import mammoth
from pathlib import WindowsPath
from markdownify import markdownify as md
import re

filename = WindowsPath("PUT THE PATH TO YOUR DOCUMENT HERE") # PUT THE PATH TO YOUR DOCUMENT IN THE BRACKETS. IF YOU WANT MUTLIPLE U NEED TO DO A FOR LOOP

# THIS CONVERTS IT TO HTML.
document = mammoth.convert_to_html(open(filename, 'rb'))

# I WRITE TO A FOLDER SO I CAN CHECK IF IT CONVERTED CORRECTLY. IF YOU DONT HAVE A FOLDER CALLED OUTPUT IN THE SAME DIRECTORY IN WHICH U RUN THIS SCRIPT, THIS WILL FAIL
with open("output/inter.html", "w") as f:
    f.write(document.value)
    f.close()

# I WROTE THIS MOD BECAUSE BEE DIDN'T SET HIS CHAPTER HEADINGS AS #. NOTE THAT THIS MOD WILL REPLACE ALL MENTION OF THE WORD 'Chapter' with a '# Chapter'
document = document.value.replace("Chapter", "# Chapter")

# I WROTE THIS MOD BECAUSE BEE GAVE ME COMBINED, SO I SPLIT BY CHAPTER. I ADDED HASHTAG PREVIOUSLY, SO I USE THAT AS THE MARKER.
chapter_list = document.split("#")

# I GO THROUGH ALL CHAPTERS SPLIT ACCORDINGLY.
for i in range(len(chapter_list)):
    # I SKIP THE FIRST ONE, BECAUSE BEE HAS A INTRO PROLOGUE FOR BETA READERS
    if i == 0:
        continue
    else:
        # IF ITS NOT THE FIRST ONE, I CHECK WHATS THE STARTING.
        print(chapter_list[i][0:100])
    
    # NOW I WRITE TO THE MD FILE
    with open("output/MR_%d.md" % i, "w") as f:

        # WHEN I WRITE, BECAUSE I SPLITTED IT PREVIOUSLY, THEN I NEED TO PATCH UP WHAT WAS REMOVED. 
        f.write(md("<p> #" + chapter_list[i]))
        f.close()
    
    # DONE
    