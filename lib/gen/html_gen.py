from lib.gen.sysmsg import generate_sysmsg_line
from lib.gen import table
from lib.misc.helper_functions import crop, save_file
from lib.misc.imgbb import upload_image
import os
import re
from PIL import Image
from html2image import Html2Image


base=os.path.dirname(os.path.abspath(__file__))
def create_html(document, path, texthtml_folder, chapter_image_folder_name, pickle_file_path, persistant_stats, text=False):
    counter = 0
    with open(str(texthtml_folder) + "\\" + path.replace(".docx", ".html"), 'wb') as f:
        #print(document.value)
        for line in document.value.split("<p>"):
            #print(line)
            line = line.replace("</p>", "") 
            if line.find("MG404") != -1:
                counter += 1
                output, persistant_stats = parse_sys_msg(line, chapter_image_folder_name, counter, pickle_file_path, persistant_stats, text=text)
                f.write(output.encode('utf8'))
            elif line.find("***") != -1:
                #linebreak
                f.write("<hr />".encode('utf8'))
            else:
                f.write("<p>".encode('utf8'))
                #print(line.encode('utf8'))
                #print(type(line.encode('utf8')))
                f.write(bytes(line, 'utf8'))
                f.write("</p>".encode('utf8'))
    print("wrote to" + str(texthtml_folder) + "\\" + path.replace(".docx", ".html"))
    return persistant_stats

def parse_sys_msg(line, chapter_image_folder_name, counter, pickle_file_path, persistant_stats, text=False):
    # given an input of persistant stats, we now generate and update
    hti = Html2Image(output_path=chapter_image_folder_name)
    image_filename = 'image' + str(counter) + '.jpg'
    print(image_filename)
    if line.find("Stats Table") == -1:
        # update the stats
        persistant_stats.update_based_on_message(line)
        css = open(base + "\\templates\\css\\smythe.css", "r").read()
        # generate said html template
        html_output = generate_sysmsg_line(line, text=text)
        # take a screenshot
        if text:
            return html_output, persistant_stats
        else:
            hti.screenshot(html_str=html_output, css_str=css, save_as=image_filename)
            # crop the background out and save image
            crop(chapter_image_folder_name + "\\"+ image_filename)

            url = upload_image(chapter_image_folder_name + "\\"+ image_filename)
            
            html_output = open(base + "\\templates\\html\\img.html").read()
            html_output = re.sub("URL_PLACEHOLDER", url, html_output)
            return html_output, persistant_stats
    else:
        persistant_stats.recalculate_stats()
        save_file(persistant_stats, pickle_file_path)
        if text:
            output_string = table.generate_text_table(persistant_stats)
            return output_string, persistant_stats
        else:
            output_string = table.generate_overall_table(persistant_stats)
            css = open(base + "\\templates\\css\\smythe_stat.css", "r").read()
            hti.screenshot(html_str=output_string, css_str=css, save_as=image_filename, size=(1200, 16000))
            # crop the background out and save image
            crop(chapter_image_folder_name + "\\"+ image_filename)
            url = upload_image(chapter_image_folder_name + "\\"+ image_filename)
            html_output = open(base + "\\templates\\html\\img.html").read()
            html_output = re.sub("URL_PLACEHOLDER", url, html_output)
            return html_output, persistant_stats
    

        


