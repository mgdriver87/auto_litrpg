from lib.misc.helper_functions import calculate_stats_based_on_message
import os
import re
base=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

class Title:
    def __init__(self, name=None, description=None, stat_message=None, bonus_stats=None, system_message=None):
        if system_message is not None:
            self.name = system_message.split("|")[1].strip()
            self.description = system_message.split("|")[2].strip()
            self.stat_message = system_message.split("|")[-1].strip("]")
            self.bonus_stats = calculate_stats_based_on_message(self.stat_message)
        else:
            self.name = name
            self.description = description
            self.stat_message = stat_message
            self.bonus_stats = bonus_stats
        #print(self.name)
        self.html_string = self.generate_html_string()
    
    def generate_html_string(self):        
        with open(os.path.join(base, "gen/templates/html/stat_table/parts/placeholder.html")) as f:
            contents = f.read()
        # replace name
        contents = re.sub("NAME_PLACEHOLDER", str(self.name), contents)
        contents = re.sub("DESCRIPTION_PLACEHOLDER", str(self.description), contents)
        contents = re.sub("STATMESSAGE_PLACEHOLDER", str(self.stat_message), contents)

        return 0
        