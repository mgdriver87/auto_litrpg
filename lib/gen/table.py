from lib.RPG import titles
from bs4 import BeautifulSoup as bs
import os
import re
import html

title_bonus_stats_colour_string = """<span style="color: #ecf0f1;">(</span><strong><span style="color: rgba(208, 139, 0, 1);">BONUS_TITLE_PLACEHOLDER</span></strong><span style="color: #ecf0f1;">)</span>"""
equipment_bonus_stats_colour_string = """<span style="color: #ecf0f1;">(</span><strong><span style="color: rgba(22, 145, 121, 1);"><span style="color: rgba(236, 240, 241, 1);"><span style="color: rgba(45, 194, 107, 1);">BONUS_EQUIPMENT_PLACEHOLDER</span></span></span></strong><span style="color: #ecf0f1;">)</span>"""
status_effect_stats_colour_string = """<span style="color: #ecf0f1;">(</span><strong><span style="color: rgba(120, 139, 0, 1);">BONUS_STATUS_EFFECT_PLACEHOLDER</span></strong><span style="color: #ecf0f1;">)</span>"""
stats_colour_string = """<span style="color: #ecf0f1;">TOTAL_STATS_PLACEHOLDER</span>"""


title_bonus_stats_string = """(BONUS_TITLE_PLACEHOLDER)"""
equipment_bonus_stats_string = """(BONUS_EQUIPMENT_PLACEHOLDER)"""
status_effect_stats_string = """(BONUS_STATUS_EFFECT_PLACEHOLDER)"""
stats_string = """TOTAL_STATS_PLACEHOLDER"""
base=os.path.dirname(os.path.abspath(__file__))

def generate_text_table(stat_class):
    resulting_html_string = open(os.path.join(base, "templates/html/stat_table_text/text_test.html")).read()

    resulting_html_string = re.sub("LEVEL_PLACEHOLDER", str(stat_class.level), resulting_html_string)

    known_placeholders = ["MAX_HP_PLACEHOLDER", "MAX_MP_PLACEHOLDER", "MAX_STA_PLACEHOLDER"]

    for i in range(len(known_placeholders)):
        if stat_class.bonus_title_stats[i+5] < 0:
            title_bonus_string = re.sub("BONUS_TITLE_PLACEHOLDER", "-" + str(stat_class.bonus_title_stats[i+5]), title_bonus_stats_string)
        else:
            title_bonus_string = re.sub("BONUS_TITLE_PLACEHOLDER", "+" + str(stat_class.bonus_title_stats[i+5]), title_bonus_stats_string)

        if stat_class.bonus_equipment_stats[i+5] < 0:
            equipment_bonus_string = re.sub("BONUS_EQUIPMENT_PLACEHOLDER", "-" + str(stat_class.bonus_equipment_stats[i+5]), equipment_bonus_stats_string)
        else:
            equipment_bonus_string = re.sub("BONUS_EQUIPMENT_PLACEHOLDER", "+" + str(stat_class.bonus_equipment_stats[i+5]), equipment_bonus_stats_string)
        
        if stat_class.status_effects_stats[i+5] < 0:
            status_effect_bonus_string = re.sub("BONUS_STATUS_EFFECT_PLACEHOLDER", "-" + str(stat_class.status_effects_stats[i+5]), status_effect_stats_string)
        else:
            status_effect_bonus_string = re.sub("BONUS_STATUS_EFFECT_PLACEHOLDER", "+" + str(stat_class.status_effects_stats[i+5]), status_effect_stats_string)
        
        total_stats_string = re.sub("TOTAL_STATS_PLACEHOLDER", ": "+ str(stat_class.total_stats[i+5]), stats_string)
        resulting_html_string = re.sub(
            known_placeholders[i],
            total_stats_string + title_bonus_string + equipment_bonus_string + status_effect_bonus_string,
            resulting_html_string)
    
    resulting_html_string = re.sub("RACE_PLACEHOLDER", stat_class.race, resulting_html_string)

    resulting_html_string = re.sub("CLASS_PLACEHOLDER", stat_class.gameclass, resulting_html_string)

    resulting_html_string = re.sub("SUB_PLACEHOLDER", stat_class.gamesubclass, resulting_html_string)

    
    known_placeholders = ["STR_PLACEHOLDER", "DEX_PLACEHOLDER", "INT_PLACEHOLDER", "VIT_PLACEHOLDER", "CHA_PLACEHOLDER"]

    for i in range(len(known_placeholders)):
        if stat_class.bonus_title_stats[i] < 0:
            title_bonus_string = re.sub("BONUS_TITLE_PLACEHOLDER", "-" + str(stat_class.bonus_title_stats[i]), title_bonus_stats_string)
        else:
            title_bonus_string = re.sub("BONUS_TITLE_PLACEHOLDER", "+" + str(stat_class.bonus_title_stats[i]), title_bonus_stats_string)

        if stat_class.bonus_equipment_stats[i] < 0:
            equipment_bonus_string = re.sub("BONUS_EQUIPMENT_PLACEHOLDER", "-" + str(stat_class.bonus_equipment_stats[i]), equipment_bonus_stats_string)
        else:
            equipment_bonus_string = re.sub("BONUS_EQUIPMENT_PLACEHOLDER", "+" + str(stat_class.bonus_equipment_stats[i]), equipment_bonus_stats_string)
        
        if stat_class.status_effects_stats[i] < 0:
            status_effect_bonus_string = re.sub("BONUS_STATUS_EFFECT_PLACEHOLDER", "-" + str(stat_class.status_effects_stats[i]), status_effect_stats_string)
        else:
            status_effect_bonus_string = re.sub("BONUS_STATUS_EFFECT_PLACEHOLDER", "+" + str(stat_class.status_effects_stats[i]), status_effect_stats_string)
        
        total_stats_string = re.sub("TOTAL_STATS_PLACEHOLDER", str(stat_class.total_stats[i]), stats_string)
        resulting_html_string = re.sub(
            known_placeholders[i],
            total_stats_string + title_bonus_string + equipment_bonus_string + status_effect_bonus_string,
            resulting_html_string)
    
    # finally add free points
    resulting_html_string = re.sub("FREE_POINTS_PLACEHOLDER", str(stat_class.free_points), resulting_html_string)

    effect_placeholder_string =  open(os.path.join(base, "templates/html/stat_table_text/generic_entry.html")).read()

    if len(stat_class.status_effects) == 0:
        # means no status effects
        effect_placeholder_string = """<p style="text-align: center; font-style: italic; font-weight: bold;">NONE</p>"""
    else:
        for status_effect in stat_class.status_effects:
            new_effect_string = ""
            new_effect_string = re.sub("NAME_PLACEHOLDER", str(status_effect.name), effect_placeholder_string)
            if str(status_effect.description)[-1] != "." and str(status_effect.description)[-1] != "?":
                new_string =  re.sub("DESCRIPTION_PLACEHOLDER", str(status_effect.description) + ".", new_string)
            else:
                new_string =  re.sub("DESCRIPTION_PLACEHOLDER", str(status_effect.description), new_string)
            new_effect_string = re.sub("STATMESSAGE_PLACEHOLDER", str(status_effect.stat_increase_message), new_effect_string)
            print("###############################")
            print(status_effect.stat_increase_message)
            print("###############################")
            effect_placeholder_string += new_effect_string
    
    resulting_html_string = re.sub("STATUS_ENTRY", effect_placeholder_string, resulting_html_string)

    template_string =  open(os.path.join(base, "templates/html/stat_table_text/generic_entry.html")).read()
    html_string = ""
    if len(stat_class.equipment) == 0:
        html_string = """<p style="text-align: center; font-style: italic; font-weight: bold;">NONE</p>"""
    else:
        for element in stat_class.equipment:
            new_string = ""
            new_string = re.sub("NAME_PLACEHOLDER", str(element.name), template_string)
            if str(element.description)[-1] != "." and str(element.description)[-1] != "?":
                new_string =  re.sub("DESCRIPTION_PLACEHOLDER", str(element.description) + ".", new_string)
            else:
                new_string =  re.sub("DESCRIPTION_PLACEHOLDER", str(element.description), new_string)
            new_string =  re.sub("DESCRIPTION_PLACEHOLDER", str(element.description), new_string)
            new_string = re.sub("STATMESSAGE_PLACEHOLDER", str(element.stat_message), new_string)
            html_string += new_string

    resulting_html_string = re.sub("EQUIPMENT_ENTRY", html_string, resulting_html_string)

    template_string =  open(os.path.join(base, "templates/html/stat_table_text/generic_entry.html")).read()
    html_string = ""
    if len(stat_class.skills) == 0:
        html_string = """<p style="text-align: center; font-style: italic; font-weight: bold;">NONE</p>"""
    else:
        for element in stat_class.skills:
            new_string = ""
            new_string = re.sub("NAME_PLACEHOLDER", str(element.name), template_string)
            if str(element.description)[-1] != "." and str(element.description)[-1] != "?":
                new_string =  re.sub("DESCRIPTION_PLACEHOLDER", str(element.description) + ".", new_string)
            else:
                new_string =  re.sub("DESCRIPTION_PLACEHOLDER", str(element.description), new_string)
            new_string = re.sub("STATMESSAGE_PLACEHOLDER", str(element.stat_increase_message), new_string)
            html_string += new_string

    resulting_html_string = re.sub("SKILLS_ENTRY", html_string, resulting_html_string)

    template_string =  open(os.path.join(base, "templates/html/stat_table_text/generic_entry.html")).read()
    html_string = ""
    if len(stat_class.titles) == 0:
        html_string = """<p style="text-align: center; font-style: italic; font-weight: bold;">NONE</p>"""
    else:
        for element in stat_class.titles:
            new_string = ""
            new_string = re.sub("NAME_PLACEHOLDER", str(element.name), template_string)
            if str(element.description)[-1] != "." and str(element.description)[-1] != "?":
                new_string =  re.sub("DESCRIPTION_PLACEHOLDER", str(element.description) + ".", new_string)
            else:
                new_string =  re.sub("DESCRIPTION_PLACEHOLDER", str(element.description), new_string)
            new_string = re.sub("STATMESSAGE_PLACEHOLDER", str(element.stat_message), new_string)
            html_string += new_string

    resulting_html_string = re.sub("TITLES_ENTRY", html_string, resulting_html_string)

    return resulting_html_string
    


def generate_overall_table(stat_class, text=False):
    # the objective is to combine all HTML strings into a continous html string.
    # e.g instead of insert, we just readd everything in.

    # start with head_part
    resulting_html_string = open(os.path.join(base, "templates/html/stat_table/parts/base.html")).read()

    resulting_html_string += open(os.path.join(base, "templates/html/stat_table/parts/border.html")).read()

    # next is top_stats. 
    resulting_html_string += generate_top_stats_string(stat_class)

    resulting_html_string += open(os.path.join(base, "templates/html/stat_table/parts/border.html")).read()

    # next is status_effects
    resulting_html_string += generate_status_effects_string(stat_class)

    resulting_html_string += open(os.path.join(base, "templates/html/stat_table/parts/border.html")).read()

    # next is the stats
    resulting_html_string += generate_stats_string(stat_class)

    resulting_html_string += open(os.path.join(base, "templates/html/stat_table/parts/border.html")).read()
    
    resulting_html_string += generate_equipment_string(stat_class)

    resulting_html_string += open(os.path.join(base, "templates/html/stat_table/parts/border.html")).read()

    resulting_html_string += generate_skills_string(stat_class)

    resulting_html_string += open(os.path.join(base, "templates/html/stat_table/parts/border.html")).read()

    resulting_html_string += generate_titles_string(stat_class)

    resulting_html_string += open(os.path.join(base, "templates/html/stat_table/parts/tail.html")).read()

    #print(resulting_html_string)

    #new_title = titles.Title(system_message="MG404: [ Title Obtained | Usurper(Basic) | So, climbing the ranks huh? | +5 STR, + 3 AGI, + 10% damage to those of higher authority]")

    
    return resulting_html_string

def generate_top_stats_string(stat_class):
    # assumed that recalculation of stats is done before this function. All stats should be accurate by here.
    top_stats_html_string = open(os.path.join(base, "templates/html/stat_table/parts/HPMPSTA.html")).read()
    # replace all placeholders
    top_stats_html_string = re.sub("LEVEL_PLACEHOLDER", str(stat_class.level), top_stats_html_string)

    known_placeholders = ["MAX_HP_PLACEHOLDER", "MAX_MP_PLACEHOLDER", "MAX_STA_PLACEHOLDER"]

    for i in range(len(known_placeholders)):
        if stat_class.bonus_title_stats[i+5] < 0:
            title_bonus_string = re.sub("BONUS_TITLE_PLACEHOLDER", "-" + str(stat_class.bonus_title_stats[i+5]), title_bonus_stats_colour_string)
        else:
            title_bonus_string = re.sub("BONUS_TITLE_PLACEHOLDER", "+" + str(stat_class.bonus_title_stats[i+5]), title_bonus_stats_colour_string)

        if stat_class.bonus_equipment_stats[i+5] < 0:
            equipment_bonus_string = re.sub("BONUS_EQUIPMENT_PLACEHOLDER", "-" + str(stat_class.bonus_equipment_stats[i+5]), equipment_bonus_stats_colour_string)
        else:
            equipment_bonus_string = re.sub("BONUS_EQUIPMENT_PLACEHOLDER", "+" + str(stat_class.bonus_equipment_stats[i+5]), equipment_bonus_stats_colour_string)
        
        if stat_class.status_effects_stats[i+5] < 0:
            status_effect_bonus_string = re.sub("BONUS_STATUS_EFFECT_PLACEHOLDER", "-" + str(stat_class.status_effects_stats[i+5]), status_effect_stats_colour_string)
        else:
            status_effect_bonus_string = re.sub("BONUS_STATUS_EFFECT_PLACEHOLDER", "+" + str(stat_class.status_effects_stats[i+5]), status_effect_stats_colour_string)
        
        total_stats_string = re.sub("TOTAL_STATS_PLACEHOLDER", ": "+ str(stat_class.total_stats[i+5]), stats_colour_string)
        top_stats_html_string = re.sub(
            known_placeholders[i],
            total_stats_string + title_bonus_string + equipment_bonus_string + status_effect_bonus_string,
            top_stats_html_string)
    
    return top_stats_html_string

def generate_status_effects_string(stat_class):
    effect_placeholder_string = open(os.path.join(base, "templates/html/stat_table/parts/placeholder.html")).read()
    status_effect_html_string = open(os.path.join(base, "templates/html/stat_table/parts/header.html")).read()
    status_effect_html_string = re.sub("HEADER_TITLE", "STATUS EFFECTS", status_effect_html_string)
    if len(stat_class.status_effects) == 0:
        # means no status effects
        status_effect_html_string += """<tr><td style="text-align: center;" colspan="4">NONE</td></tr>"""
    else:
        for status_effect in stat_class.status_effects:
            new_effect_string = ""
            new_effect_string = re.sub("NAME_PLACEHOLDER", str(status_effect.name), effect_placeholder_string)
            new_effect_string =re.sub("DESCRIPTION_PLACEHOLDER", str(status_effect.description), new_effect_string)
            new_effect_string = re.sub("STATMESSAGE_PLACEHOLDER", str(status_effect.stat_increase_message), new_effect_string)
            print("###############################")
            print(status_effect.stat_increase_message)
            print("###############################")
            status_effect_html_string += new_effect_string
    
    return status_effect_html_string

def generate_stats_string(stat_class):
    # assumed that recalculation of stats is done before this function. All stats should be accurate by here.
    stats_html_string = open(os.path.join(base, "templates/html/stat_table/parts/main_stats.html")).read()
    # replace all placeholders

    stats_html_string = re.sub("RACE_PLACEHOLDER", stat_class.race, stats_html_string)

    stats_html_string = re.sub("CLASS_PLACEHOLDER", stat_class.gameclass, stats_html_string)

    stats_html_string = re.sub("SUB_PLACEHOLDER", stat_class.gamesubclass, stats_html_string)

    
    known_placeholders = ["STR_PLACEHOLDER", "DEX_PLACEHOLDER", "INT_PLACEHOLDER", "VIT_PLACEHOLDER", "CHA_PLACEHOLDER"]

    for i in range(len(known_placeholders)):
        if stat_class.bonus_title_stats[i] < 0:
            title_bonus_string = re.sub("BONUS_TITLE_PLACEHOLDER", "-" + str(stat_class.bonus_title_stats[i]), title_bonus_stats_colour_string)
        else:
            title_bonus_string = re.sub("BONUS_TITLE_PLACEHOLDER", "+" + str(stat_class.bonus_title_stats[i]), title_bonus_stats_colour_string)

        if stat_class.bonus_equipment_stats[i] < 0:
            equipment_bonus_string = re.sub("BONUS_EQUIPMENT_PLACEHOLDER", "-" + str(stat_class.bonus_equipment_stats[i]), equipment_bonus_stats_colour_string)
        else:
            equipment_bonus_string = re.sub("BONUS_EQUIPMENT_PLACEHOLDER", "+" + str(stat_class.bonus_equipment_stats[i]), equipment_bonus_stats_colour_string)
        
        if stat_class.status_effects_stats[i] < 0:
            status_effect_bonus_string = re.sub("BONUS_STATUS_EFFECT_PLACEHOLDER", "-" + str(stat_class.status_effects_stats[i]), status_effect_stats_colour_string)
        else:
            status_effect_bonus_string = re.sub("BONUS_STATUS_EFFECT_PLACEHOLDER", "+" + str(stat_class.status_effects_stats[i]), status_effect_stats_colour_string)
        
        total_stats_string = re.sub("TOTAL_STATS_PLACEHOLDER", str(stat_class.total_stats[i]), stats_colour_string)
        stats_html_string = re.sub(
            known_placeholders[i],
            total_stats_string + title_bonus_string + equipment_bonus_string + status_effect_bonus_string,
            stats_html_string)
    
    # finally add free points
    stats_html_string = re.sub("FREE_POINTS_PLACEHOLDER", str(stat_class.free_points), stats_html_string)
    
    return stats_html_string

def generate_equipment_string(stat_class):
    template_string = open(os.path.join(base, "templates/html/stat_table/parts/placeholder.html")).read()
    html_string = open(os.path.join(base, "templates/html/stat_table/parts/header.html")).read()
    html_string = re.sub("HEADER_TITLE", "EQUIPMENT", html_string)
    if len(stat_class.equipment) == 0:
        html_string += """<tr><td style="text-align: center;" colspan="4">NONE</td></tr>"""
        return html_string
    else:
        for element in stat_class.equipment:
            new_string = ""
            new_string = re.sub("NAME_PLACEHOLDER", str(element.name), template_string)
            new_string =  re.sub("DESCRIPTION_PLACEHOLDER", str(element.description), new_string)
            new_string = re.sub("STATMESSAGE_PLACEHOLDER", str(element.stat_message), new_string)
            html_string += new_string

    return html_string

def generate_skills_string(stat_class):
    template_string = open(os.path.join(base, "templates/html/stat_table/parts/placeholder.html")).read()
    html_string = open(os.path.join(base, "templates/html/stat_table/parts/header.html")).read()
    html_string = re.sub("HEADER_TITLE", "SKILLS", html_string)

    if len(stat_class.skills) == 0:
        html_string += """<tr><td style="text-align: center;" colspan="4">NONE</td></tr>"""
        return html_string
    else:
        for element in stat_class.skills:
            new_string = ""
            new_string = re.sub("NAME_PLACEHOLDER", str(element.name), template_string)
            new_string =  re.sub("DESCRIPTION_PLACEHOLDER", str(element.description), new_string)
            new_string = re.sub("STATMESSAGE_PLACEHOLDER", str(element.stat_increase_message), new_string)
            html_string += new_string

    html_string += "</td></tr>"

    return html_string

def generate_titles_string(stat_class):
    template_string = open(os.path.join(base, "templates/html/stat_table/parts/placeholder.html")).read()
    html_string = open(os.path.join(base, "templates/html/stat_table/parts/header.html")).read()
    html_string = re.sub("HEADER_TITLE", "TITLES", html_string)
    print("THE LENGTH OF TITLES IS " + str(len(stat_class.titles)))
    print(template_string)
    if len(stat_class.titles) == 0:
        html_string += """<tr><td style="text-align: center;" colspan="4">NONE</td></tr>"""
        return html_string
    else:
        for element in stat_class.titles:
            new_string = ""
            new_string = re.sub("NAME_PLACEHOLDER", str(element.name), template_string)
            new_string =  re.sub("DESCRIPTION_PLACEHOLDER", str(element.description), new_string)
            new_string = re.sub("STATMESSAGE_PLACEHOLDER", str(element.stat_message), new_string)
            html_string += new_string
    
    return html_string

def convert_to_raw_text(output_string, stat=False):
    soup = bs(output_string)
    result = soup.get_text()
    if not stat:
        result = result.replace("\n", "")
        result = result.replace("]", "] ")
        result = result.replace("[", " [")

        result = "<p>" + html.unescape(result) + "</p>"
    else:

        result = list(result.replace("\n", "@"))
        replace = True
        swap = 0
        for index in range(len(result)):
            if result[index] == "@":
                if replace:
                    if swap % 2 == 0:
                        result[index] = "<p>"
                    else:
                        result[index] = "</p>"
                    replace = False
                    swap += 1
                else:
                    result[index] = ""
                    replace = False
            else:
                replace = True
        result = ''.join(result)
        result = result.replace("]", "] ")
        result = result.replace("[", " [")

    return result
