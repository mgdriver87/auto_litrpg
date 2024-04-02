
import configparser
import re
import os

base=os.path.dirname(os.path.abspath(__file__))
config = configparser.ConfigParser()
config.read('config.ini')
template_folder = config['INTERMEDIATE']['TEMPLATEFOLDER']

def generate_sysmsg_line(system_message, text=False):
    #print("im here")
    message_id = system_message.split("|")[0].split("[")[-1].strip(" ")
    name = system_message.split("|")[1].strip().replace("]", " ")
    if system_message.find("Killed") == -1:
        if system_message.find("Level Up") == -1:
            name = system_message.split("|")[1].strip().replace("]", " ")
            description = system_message.split("|")[2].strip().replace("]", "")
            if system_message.find("Title") != -1:
                html_string = open(os.path.join(base, "templates\\html\\title.html")).read()
            elif system_message.find("Skill") != -1:
                if system_message.find("Item") == -1:
                    html_string = open(os.path.join(base, "templates\\html\\skill.html")).read()
                else:
                    html_string = open(os.path.join(base, "templates\\html\\item.html")).read()
            elif system_message.find("Item") != -1:
                html_string = open(os.path.join(base, "templates\\html\\item.html")).read()
            elif system_message.find("Effect") != -1:
                html_string = open(os.path.join(base, "templates\\html\\status_effect.html")).read()
            else:
                html_string = open(os.path.join(base, "templates\\html\\generic.html")).read()
            message_list =  system_message.split("|")[-1].strip("]").replace("</em>", "").replace("<em>", "").split(".")
            stat_message = ""
            for x in message_list:
                if x == '' or x == "]":
                    continue
                else:
                    if text:
                        stat_message += x
                    else:
                        stat_message += """<p style="color: #ecf0f1;">""" + x + "</p>"
            stat_message = stat_message.replace("]", " ")
            if text:
                html_string = open(os.path.join(base, "templates\\html\\generic_text.html")).read()
            html_string = re.sub("STATMESSAGE_PLACEHOLDER", str(stat_message), html_string)
        else:
            # its a level up message
            level_list = system_message.split(":")[2].split("|")[0].split("-")
            html_string = open(os.path.join(base, "templates\\html\\lvlup.html")).read()
            if text:
                html_string = open(os.path.join(base, "templates\\html\\lvlup_text.html")).read()
            html_string = re.sub("START_PLACEHOLDER", str(int(level_list[0])), html_string)
            html_string = re.sub("END_PLACEHOLDER", str(int(level_list[1])), html_string)
            return html_string
            
    else:
        name = system_message.split("|")[1].split("[")[-1].strip(" ").strip("]")
        description = system_message.split("|")[-1].strip("]").replace(".", ".\n").replace("]", "")
        print(description)
        
        html_string = open(os.path.join(base, "templates\\html\\kill.html")).read()
        if text:
            html_string = open(os.path.join(base, "templates\\html\\kill_text.html")).read()

    html_string  = re.sub("ID_PLACEHOLDER", str(message_id), html_string)
    html_string = re.sub("NAME_PLACEHOLDER", str(name), html_string)
    html_string = re.sub("DESCRIPTION_PLACEHOLDER", str(description), html_string)
    
    print("------------------------------")
    print(description)
    print(name)
    print(message_id)

    return html_string