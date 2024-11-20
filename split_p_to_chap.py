import os

chapter_folder = "/home/uberchio/Documents/auto_litrpg/input/"
print("hello")
#os.listdir(chapter_folder)
text = ""
counter = 1
part_counter = 1
for path in sorted(os.listdir(chapter_folder)):
    print(path)
    with open(chapter_folder + path, "r") as f:
        inter_html = f.read() 
        inter_html = inter_html.split("Chapter")
        for i in range(len(inter_html)):
            print("*********************************8")
            title = "Chapter " + inter_html[i].split("</p>")[0].split("<")[0].replace(":", " - ")
            inter_html[i] = "<p>Chapter " + inter_html[i]
            with open(chapter_folder + "output/" + title + ".html", 'w') as l:
                l.write(inter_html[i])
#pypandoc.convert_file("inter.md", to='docx', outputfile='result.docx')

    
