
import configparser
import re
import os

base=os.path.dirname(os.path.abspath(__file__))
config = configparser.ConfigParser()
config.read('config.ini')
template_folder = config['INTERMEDIATE']['TEMPLATEFOLDER']

def generate_sysmsg_line(system_message, text=False):
    print("in generate_sysmsg_line: " + system_message)
    message_id = system_message.split("|")[0].split("[")[-1].strip(" ")
    name = system_message.split("|")[1].strip().replace("]", " ")
    if "Equipment Equipped" in system_message == 1:
        print(system_message)
        return ""
    if system_message.find("You killed") == -1 and system_message.find("Killed") == -1 :
        if system_message.find("Your level has increased") == -1:
            name = system_message.split("|")[1].strip().replace("]", " ")
            try:
                description = system_message.split("|")[2].strip().replace("]", "")
            except IndexError:
                description = system_message.split("|")[1].strip().replace("]", "")
            if system_message.find("Title") != -1:
                if text:
                    html_string = open(os.path.join(base, "templates\\html\\generic_text.html")).read()
                else:
                    html_string = open(os.path.join(base, "templates\\html\\title.html")).read()
                    print("using title.html")
            elif system_message.find("Skill") != -1:
                if system_message.find("Item") == -1:
                    if text:
                        html_string = open(os.path.join(base, "templates\\html\\generic_text.html")).read()
                    else:
                        html_string = open(os.path.join(base, "templates\\html\\skill.html")).read()
                        print("using skill.html")
                else:
                    if text:
                        html_string = open(os.path.join(base, "templates\\html\\item_text.html")).read()
                    else:
                        html_string = open(os.path.join(base, "templates\\html\\item.html")).read()
                        print("using item.html")
            elif system_message.find("Item") != -1:
                if text:
                    html_string = open(os.path.join(base, "templates\\html\\item_text.html")).read()
                else:
                    html_string = open(os.path.join(base, "templates\\html\\item.html")).read()
                print("using item.html")
            elif system_message.find("Effect") != -1:
                if text:
                    html_string = open(os.path.join(base, "templates\\html\\generic_text.html")).read()
                else:
                    html_string = open(os.path.join(base, "templates\\html\\status_effect.html")).read()
                print("using status_effect.html")
            else:
                if text:
                    html_string = open(os.path.join(base, "templates\\html\\generic_text.html")).read()
                else:
                    html_string = open(os.path.join(base, "templates\\html\\generic.html")).read()
                print("using generic.html")
            message_list =  system_message.split("|")
            if len(message_list) > 4:
                addon_string =  message_list[-2]
                raw_stats = """<p style="text-align: center; font-style: italic;">"""+ message_list[-3] + "</p>"
                if "STR" not in raw_stats:
                    if "DEX" not in raw_stats:
                        if "INT" not in raw_stats:
                            if "CHA" not in raw_stats:
                                if "VIT" not in raw_stats:
                                    raw_stats = """<p style="text-align: center;">""" + message_list[3] + "</p>"
                print([raw_stats, addon_string])
                if message_list[-2] in message_list[3]:
                    # duplicate
                    addon_string = ""
            else:
                addon_string = ""
                raw_stats = ""
            message_list =  system_message.split("|")[-1].strip("]").replace("</em>", "").replace("<em>", "").split(",")
            stat_message = ""
            for x in message_list:
                if x == '' or x == "]":
                    continue
                else:
                    if text:
                        stat_message += x + ","
                    else:
                        stat_message += """<p>""" + x + "</p>"
            stat_message = stat_message.replace("]", " ")
            stat_message = stat_message.strip(",")
            if stat_message.strip() in description.strip():
                stat_message = ""
            print([description, stat_message])
            html_string = re.sub("STATMESSAGE_PLACEHOLDER", str(stat_message), html_string)
            html_string = re.sub("ADDON_PLACEHOLDER", str(addon_string), html_string)
            html_string = re.sub("RAW_STATS_PLACEHOLDER", str(raw_stats), html_string)
        else:
            # its a level up message
            original_level = system_message.split("|")[0].split("to")[0].split("level")[-1].strip()
            new_level = system_message.split("|")[0].split("to")[-1].split("level")[-1].strip().replace("!", "")
            level_list = [original_level, new_level]
                #print(int(level_list[0]))
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
    if message_id == "Item":
        html_string  = re.sub("ID_PLACEHOLDER", "", html_string)
    else:
        html_string  = re.sub("ID_PLACEHOLDER", str(message_id), html_string)
    
    if name.strip() in description.strip():
        if "You killed" not in name:
            name = ""
    print([name, description, message_id])
    html_string = re.sub("NAME_PLACEHOLDER", str(name), html_string)
    if str(description)[-1] != "." and str(description)[-1] != "?":
        html_string = re.sub("DESCRIPTION_PLACEHOLDER", str(description), html_string)
    else:
        html_string = re.sub("DESCRIPTION_PLACEHOLDER", str(description), html_string)

    if len(system_message) > 200:
        size = 2
    else:
        size = 3

    font_size_string = "font-size: " + str(size) + "em;"
    html_string = re.sub("FONT_PLACEHOLDER", font_size_string, html_string)

    if "Equipment Equipped" in message_id:
        return ""
    print("------------------------------")
    print(description)
    print([name])
    print(message_id)

    html_string = html_string + "<p></p>"
    return html_string