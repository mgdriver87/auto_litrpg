from lib.misc.helper_functions import find_chapter_number_alt
from pathlib import WindowsPath
import os
chapter_folder = WindowsPath(r"C:\\Users\\Hubert Khoo\\Documents\\GitHub\\auto_litrpg\\chapters")
for path in sorted(os.listdir(chapter_folder), key=find_chapter_number_alt):

    print(path)
    try:
        html_string = str(open(str(chapter_folder) + "\\" + path, 'r', encoding='utf-8').read())
    except:
        html_string = str(open(str(chapter_folder) + "\\" + path, 'r').read())
    html_list = html_string.split("</p>")
    new_html_list = []
    found = False
    for i in range(len(html_list)):
        if ('from Royal Road' in html_list[i]) | ('on Royal Road' in html_list[i]):
            print(html_list[i])
            found = True
            continue
        elif 'on Amazon' in html_list[i]:
            print(html_list[i])
            found = True
            continue
        elif 'Stolen Novel' in html_list[i]:
            print(html_list[i])
            found = True
            continue
        elif 'Stolen story' in html_list[i]:
            print(html_list[i])
            found = True
            continue
        elif 'Stolen novel; please report.' in html_list[i]:
            print(html_list[i])
            found = True
            continue
        elif 'The narrative has been taken without permission.' in html_list[i]:
            print(html_list[i])
            found = True
            continue
        elif 'This story has been taken without authorization.' in html_list[i]:
            print(html_list[i])
            found = True
            continue
        elif 'Unauthorized reproduction:' in html_list[i]:
            print(html_list[i])
            found = True
            continue
        elif 'Unauthorized duplication:' in html_list[i]:
            print(html_list[i])
            found = True
            continue
        else:
            new_html_list.append(html_list[i])
        
    if found is not True:
        print("Chapter with no anti-scrap detected!:" + path)
    
    if len(new_html_list) == 0:
        html_string = '</p>'.join(html_list)
    else:
        html_string = '</p>'.join(new_html_list)

    with open(str(chapter_folder) + "\\" + path, 'wb') as file:
        file.write(html_string.encode('utf-8'))


