from lib.RPG import titles, items, skills, status_effects



class Stats:
    def __init__(self):
        # set up starting stats TODO link to config.ini
        self.race = "Human"
        self.gameclass = "Unassigned"
        self.gamesubclass = "Unassigned"
        self.level = 1
        self.base_strength = 10
        self.base_dexerity = 10
        self.base_intelligence = 10
        self.base_vitality = 14
        self.base_charisma = 10
        self.free_points = 0
        self.base_max_hp = 10
        self.base_max_mp = 0
        self.base_max_sta = 10

        # str, dex, int, vit, cha, hp, mp, sta are what can have bonus points.
        self.bonus_title_stats = [0,0,0,0,0,0,0,0]
        self.bonus_equipment_stats = [0,0,0,0,0,0,0,0]
        self.status_effects_stats = [0,0,0,0,0,0,0,0]

        self.titles = []
        self.skills = []
        self.equipment = []
        self.status_effects = []

        self.stat_level_increment = 2
        self.hp_level_increment = 3
        self.mp_level_increment = 3
        self.sta_level_increment = 3
        self.free_points_increment = 5

        self.total_strength = self.base_strength + self.bonus_title_stats[0] + self.bonus_equipment_stats[0]
        self.total_dexerity = self.base_dexerity + self.bonus_title_stats[1] + self.bonus_equipment_stats[1]
        self.total_intelligence = self.base_intelligence + self.bonus_title_stats[2] + self.bonus_equipment_stats[2]
        self.total_vitality = self.base_vitality + self.bonus_title_stats[3] + self.bonus_equipment_stats[3]
        self.total_charisma = self.base_charisma + self.bonus_title_stats[4] + self.bonus_equipment_stats[4]
        self.free_points = self.free_points
        self.total_max_hp = self.base_max_hp + self.bonus_title_stats[5] + self.bonus_equipment_stats[5]
        self.total_max_mp = self.base_max_mp + self.bonus_title_stats[6] + self.bonus_equipment_stats[6]
        self.total_max_sta = self.base_max_sta + self.bonus_title_stats[7] + self.bonus_equipment_stats[7]

        self.total_stats = [self.total_strength, self.total_dexerity, self.total_intelligence, self.total_vitality, self.total_charisma, self.total_max_hp, self.total_max_mp, self.total_max_sta]


    def update_stats_level_up(self, system_message):
        '''
        the incoming system_message should look something like that. It will be a string.

        MG404: [Your level has increased from level 1 to level 2! | All stats increased | Bonus free points granted]
        '''
        if system_message.find('Your level has increased') == -1:
            return -1

        original_level = system_message.split("|")[0].split("to")[0].split("level")[-1].strip()
        new_level = system_message.split("|")[0].split("to")[-1].split("level")[-1].strip().replace("!", "")
        level_list = [original_level, new_level]
        #level_list = system_message.split(":")[2].split("|")[0].split("-")
        print(level_list)
        level_change = int(level_list[1]) - int(level_list[0])
        print(level_change)
    
        self.level = int(level_list[1])
        self.base_strength += self.stat_level_increment *level_change
        self.base_dexerity += self.stat_level_increment *level_change
        self.base_intelligence += self.stat_level_increment *level_change
        self.base_vitality += self.stat_level_increment *level_change
        self.base_charisma = self.base_charisma
        self.free_points += self.free_points_increment * level_change
        self.base_max_hp += self.hp_level_increment * level_change
        if (self.total_max_mp != 0):
            self.base_max_mp += self.mp_level_increment * level_change
        self.base_max_sta += self.sta_level_increment * level_change

        return 0
    def update_stats_free_points(self, system_message):
        '''
        MG404: [Information | Free Points Allocated | +35 STR, +35 DEX]
        '''
        print('Free Points allocated!')
        if system_message.find('Free Points Allocated') == -1:
            print('Did not find!')
            print(system_message)
            raise Exception

        name = system_message.split("|")[1].strip()
        description = system_message.split("|")[2].strip()
        stats_increase_message = system_message.split("|")[-1].replace("]", "")
        
        added_stats = self.calculate_stats_based_on_message(stats_increase_message)
        print(added_stats)
        #list_of_stats = ["STR", "DEX", "INT", "VIT", "CHA"]
        self.base_strength += added_stats[0]
        self.base_dexerity += added_stats[1]
        self.base_intelligence += added_stats[2]
        self.base_vitality += added_stats[3]
        self.base_charisma += added_stats[4]

        self.free_points -= sum(added_stats)

        return 0


    def update_based_on_message(self, system_message):
        '''
        the incoming system_message should look something like that. It will be a string.

        MG404: [ Title Obtained | Usurper(Basic) | So, climbing the ranks huh? | +5 STR, + 3 AGI, + 10% damage to those of higher authority]
        '''
        if system_message.find('Your level has increased') != -1:
            self.update_stats_level_up(system_message)
            return 0
        if system_message.find('Class Obtained') != -1:
            if system_message.find('Sub-Class Obtained') != -1:
                self.gamesubclass = system_message.split("|")[1].strip()
                return 0
            else:
                self.gameclass = system_message.split("|")[1].strip()
                return 0
        if system_message.find('Free Points Allocated') != -1:
            print('Free Points allocated!')
            self.update_stats_free_points(system_message)
            return 0
        
        if system_message.find('Title Obtained') != -1:
            name = system_message.split("|")[1].strip()
            description = system_message.split("|")[2].strip()
            stats_increase_message = system_message.split("|")[-1].replace("]", "")
            bonus_stats = self.calculate_stats_based_on_message(stats_increase_message)
        # check if the title_name already exists, and it is an upgrade. 
            main_name = name.split("(")[0]
            for title in self.titles:
                if title.name.find(main_name) != -1:
                    # means it already exists.
                    title.name = name
                    if str(description)[-1] != "." or str(description)[-1] != "?": 
                        title.description = str(description) + "."
                    else:
                        title.description = description
                    title.stat_message = stats_increase_message
                    # update the bonus_stats
                    title.bonus_stats = self.calculate_stats_based_on_message(stats_increase_message)
                    return 0

            # now we insert it all into the dictionary
            new_title = titles.Title(name, description, stats_increase_message, bonus_stats)
            self.titles.append(new_title)
            return 0

        elif system_message.find('Equipment Equipped') != -1:
            name = system_message.split("|")[1].strip()
            description = system_message.split("|")[2].strip()
            stats_increase_message = system_message.split("|")[-1].replace("]", "")
            bonus_stats = self.calculate_stats_based_on_message(stats_increase_message)
            # check if the title_name already exists, and it is an upgrade. 
            main_name = name.split("(")[0]
            for equipment in self.equipment:
                if equipment.name.find(main_name) != -1:
                    # means it already exists.
                    equipment.name = name
                    equipment.description = description
                    equipment.stat_message = stats_increase_message
                    # update the bonus_stats
                    equipment.bonus_stats = self.calculate_stats_based_on_message(stats_increase_message)
                    return 0

            # now we insert it all into the dictionary
            new_equipment = items.Equipment(name, description, stats_increase_message, bonus_stats)
            self.equipment.append(new_equipment)
            return 0
        elif system_message.find('Skill Obtained') != -1:
            name = system_message.split("|")[1].strip()
            description = system_message.split("|")[2].strip()
            stats_increase_message = system_message.split("|")[-1].replace("]", "")
            #print(stats_increase_message)
            bonus_stats = self.calculate_stats_based_on_message(stats_increase_message)
            main_name = name.split("(")[0]
            for skill in self.skills:
                if skill.name.find(main_name) != -1:
                    # means it already exists.
                    skill.name = name
                    skill.description = description
                    skill.stat_increase_message = stats_increase_message
                    skill.bonus_stats = bonus_stats
                    return 0

            # now we insert it all into the dictionary
            new_skill = skills.Skill(name, description, stats_increase_message, bonus_stats)
            self.skills.append(new_skill)
            return 0
        elif system_message.find('Status Effect') != -1:
            name = system_message.split("|")[1].strip()
            description = system_message.split("|")[2].strip()
            stats_increase_message = system_message.split("|")[-1].replace("]", "")
            #print(stats_increase_message)
            bonus_stats = self.calculate_stats_based_on_message(stats_increase_message)
            main_name = name
            for effect in self.status_effects:
                if effect.name.find(main_name) != -1:
                    if system_message.find('Status Effect Removed') != -1:
                        del(effect)
                    # means it already exists.
                    effect.name = name
                    effect.description = description
                    effect.stat_increase_message = stats_increase_message
                    effect.bonus_stats = bonus_stats
                    return 0

            # now we insert it all into the dictionary
            new_effect = status_effects.StatusEffects(name, description, stats_increase_message, bonus_stats)
            self.status_effects.append(new_effect)
            #print(self.status_effects)
            return 0
        else:
            #print("Unknwon Message detected!")
            #print("system_message")
            return -1
    def recalculate_bonus_stats(self):
        stats = [0,0,0,0,0,0,0,0]
        for title in self.titles:
            for i in range(len(title.bonus_stats)):
                stats[i] += title.bonus_stats[i]
        self.bonus_title_stats = stats
        stats = [0,0,0,0,0,0,0,0]
        for equipment in self.equipment:
            for i in range(len(equipment.bonus_stats)):
                stats[i] += equipment.bonus_stats[i]
        self.bonus_equipment_stats = stats
        return 0

        return 0
    def recalculate_stats(self):
        # this assumes its the end of the chapter, and we're done.
        # by this point, all level up stats are done.
        self.recalculate_bonus_stats()

        # so now we have base stats + bonus stats.
        # update the total stats right now.
        self.total_strength = self.base_strength + self.bonus_title_stats[0] + self.bonus_equipment_stats[0]
        self.total_dexerity = self.base_dexerity + self.bonus_title_stats[1] + self.bonus_equipment_stats[1]
        self.total_intelligence = self.base_intelligence + self.bonus_title_stats[2] + self.bonus_equipment_stats[2]
        self.total_vitality = self.base_vitality + self.bonus_title_stats[3] + self.bonus_equipment_stats[3]
        self.total_charisma = self.base_charisma + self.bonus_title_stats[4] + self.bonus_equipment_stats[4]
        self.free_points = self.free_points
        self.total_max_hp = self.base_max_hp + self.bonus_title_stats[5] + self.bonus_equipment_stats[5]
        self.total_max_mp = self.base_max_mp + self.bonus_title_stats[6] + self.bonus_equipment_stats[6]
        self.total_max_sta = self.base_max_sta + self.bonus_title_stats[7] + self.bonus_equipment_stats[7]
        self.total_stats = [self.total_strength, self.total_dexerity, self.total_intelligence, self.total_vitality, self.total_charisma, self.total_max_hp, self.total_max_mp, self.total_max_sta]

        return 0
    def save_file(self, chapter_counter):
        file_name = "%s_stats.txt" % chapter_counter
        with open(file_name, 'wb') as file:
            pickle.dump(self, file)

    def output_stats(self):
        return 0
    
    def calculate_stats_based_on_message(self, stat_message):
        print(stat_message)
        stats = [0,0,0,0,0,0,0,0]

        list_of_stat_increases = stat_message.split(",")
        for i in list_of_stat_increases:
            stat_string = i
            stat_string = stat_string.strip(" ")
            print(stat_string)
            if len(stat_string) == 0:
                continue
            #print(stat_string)
            if stat_string.find("STR") != -1:
                if stat_string.find("-") != -1:
                    stats[0] -= int(stat_string.split("-")[-1].split(" ")[0])
                else:
                    stats[0] += int(stat_string.split("+")[-1].split(" ")[0])
                continue
            if stat_string.find("DEX") != -1:
                if stat_string.find("-") != -1:
                    stats[1] -= int(stat_string.split("-")[-1].split(" ")[0])
                else:
                    stats[1] += int(stat_string.split("+")[-1].split(" ")[0])
                continue
            if stat_string.find("INT") != -1:
                if stat_string.find("-") != -1:
                    stats[2] -= int(stat_string.split("-")[-1].split(" ")[0])
                else:
                    stats[2] += int(stat_string.split("+")[-1].split(" ")[0])
                continue
            if stat_string.find("VIT") != -1:
                if stat_string.find("-") != -1:
                    stats[3] -= int(stat_string.split("-")[-1].split(" ")[0])
                else:
                    stats[3] += int(stat_string.split("+")[-1].split(" ")[0])
                continue
            if stat_string.find("CHA") != -1:
                if stat_string.find("-") != -1:
                    stats[4] -= int(stat_string.split("-")[-1].split(" ")[0])
                else:
                    stats[4] += int(stat_string.split("+")[-1].split(" ")[0])
                continue
            if stat_string.find("MAX HP") != -1:
                if stat_string.find("-") != -1:
                    stats[5] -= int(stat_string.split("-")[-1].split(" ")[0])
                else:
                    stats[5] += int(stat_string.split("+")[-1].split(" ")[0])
                continue
            if stat_string.find("MAX MP") != -1:
                if stat_string.find("-") != -1:
                    stats[6] -= int(stat_string.split("-")[-1].split(" ")[0])
                else:
                    stats[6] += int(stat_string.split("+")[-1].split(" ")[0])
                continue
            if stat_string.find("MAX STA") != -1:
                if stat_string.find("-") != -1:
                    stats[7] -= int(stat_string.split("-")[-1].split(" ")[0])
                else:
                    stats[7] += int(stat_string.split("+")[-1].split(" ")[0])
                continue
        
        return stats
