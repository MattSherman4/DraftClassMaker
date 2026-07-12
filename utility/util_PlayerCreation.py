
#< Noteable functions:
#< get_name(draft_size, draft_data) - Generateds a draft_size sized list of names based on dataset draft_data
#< get_college

import sys

from .util_Data import *
import random
import heapq
from operator import itemgetter
import ast
    
# Returns a dictionary of prestige counts given a list
# def list_to_dict_prestige(grades_list):
#     prestige_dict = {}
#     prestige_dict['Top'] = grades_list.count(1)
#     prestige_dict['Middle'] = grades_list.count(2)
#     prestige_dict['Bottom'] = grades_list.count(3)
#     prestige_dict['FA'] = grades_list.count(4)
#     prestige_dict['RMC'] = grades_list.count(5)
#     return prestige_dict

def get_name(size):
    name_data = load_cfg("player Names")
    history_draft = load_draft_all()
    history_draft = history_draft[history_draft['Year'] >= MODERN_ERA].copy()

    #  Will re-spin the name if there is more than one hyphen
    def check_hyphenated_grammar(arr, i, first_count, last_count, suffix_count):
        ret = []
        #  Avoid using any more than one hyphen
        for name in arr:
            while "-" in name:
                name = random_name(i, first_count, last_count, suffix_count)
            ret.append(name)
        # Avoid using names that end in an apostrophe as teh first numae in a hyphenated name
        if ret[0][-1] == "'":
            ret[0] = ret[0][:-1]
        return ret

    #  Returns a random first name with argument n = 0, last name with argument n = 1, and suffix with argument n = 2
    def random_name(n:int, first_count, last_count, suffix_count):
        if n == 0:
            return random.choices(list(first_count.keys()), weights = list(first_count.values()), k = 1)[0]
        elif n == 1:
            return random.choices(list(last_count.keys()), weights = list(last_count.values()), k = 1)[0]
        elif n == 2:
            return random.choices(list(suffix_count.keys()), weights = list(suffix_count.values()), k = 1)[0]
        return 'ERROR_NAME'

    first_count = ast.literal_eval(name_data['Names']['first_count'])
    first_hyphen_percentage = float(name_data['Percentages']['first_hyphen_percentage'])
    last_count = ast.literal_eval(name_data['Names']['last_count'])
    last_hyphen_percentage = float(name_data['Percentages']['last_hyphen_percentage'])
    suffix_count = ast.literal_eval(name_data['Names']['suffix_count'])
    suffix_percentage = float(name_data['Percentages']['suffix_percentage'])
    names_list = []

    for _ in range(0, size):
        name = ''
        app = []

        #^ -- Get First Name -- ^#
        #TODO: Add a small chance of making a first name a last name???
        #  If the name is hyphenated, run the first name randomizer twice
        if (random.randrange(100000) / 1000.0) < first_hyphen_percentage:
            name = []
            hyphenated = []
            hyphenated.append(random_name(0, first_count, last_count, suffix_count))
            hyphenated.append(random_name(0, first_count, last_count, suffix_count))
            #  Rerun if more than one hyphen
            hyphenated = check_hyphenated_grammar(hyphenated, 0, first_count, last_count, suffix_count)
            #  Check for grammar adjustments and form name in name array
            for t in hyphenated:
                if t in Upper:
                    name.append(t.upper())
                else:
                    name.append(t)
            name = '-'.join(name)
        #  If no hyphen is needed, run the first name randomizer once
        else:
            name = random_name(0, first_count, last_count, suffix_count)
            #  Check for grammar adjustments
            if name in Upper:
                name = name.upper()
        # Append the first name to the append variable and clear the name variable for the last name
        app.append(name)
        name = []
        hyphenated = []

        #^ -- Get Last Name -- ^#
        #  If the name is hyphenated, run the last name randomizer twice
        if (random.randrange(100000) / 1000.0) < last_hyphen_percentage:
            hyphenated.append(random_name(1, first_count, last_count, suffix_count))
            hyphenated.append(random_name(1, first_count, last_count, suffix_count))
            #  Rerun if more than one hyphen
            hyphenated = check_hyphenated_grammar(hyphenated, 1, first_count, last_count, suffix_count)
            #  Check for grammar adjustments and form name in name array
            for t in hyphenated:
                if t in Upper:
                    name.append(t.upper())
                else:
                    name.append(t)
            name = '-'.join(name)
        #  If no hyphen is needed, run the last name randomizer once
        else:
            name = random_name(1, first_count, last_count, suffix_count)
            if name in Upper:
                name = name.upper()
        # Append the last name to the append variable and clear the name variable for the last name
        app.append(name)
        name = []

        #^ -- Get Suffix -- ^#
        #  If the name has a suffix, run the suffix randomizer once
        if (random.randrange(100000) / 1000.0) < suffix_percentage:
            name = random_name(2, first_count, last_count, suffix_count)
            if name in Upper:
                name = name.upper()
            app.append(name)

        #  Return final name joined by spaces
        # print(app)
        names_list.append(' '.join(app))
    return names_list

#_ College _#
# Find top 10 drafted + PFA colleges by position
# Spin specifically for those colleges
#? Select a Division?
#? Select a Conference?
## Select a School
# Gets a list of colleges ordered by rank for a draft class
def get_college(size, position, prestige):
    def get_temp_prestige(prestige_list, num):
        try:
            temp = prestige_list[num]
            return temp
        except:
            return 2 # 'Middle' is default value for prestige
        
    def get_division(prestige = 1):
        if prestige == 2:
            return random.choices(list(mid_freq.keys()), weights = list(mid_freq.values()), k = 1)[0]
        if prestige == 3:
            return random.choices(list(bot_freq.keys()), weights = list(bot_freq.values()), k = 1)[0]
        elif prestige == 4:
            return random.choices(list(FA_freq.keys()), weights = list(FA_freq.values()), k = 1)[0]
        elif prestige == 5:
            return random.choices(list(RMC_freq.keys()), weights = list(RMC_freq.values()), k = 1)[0]
        else:
            return random.choices(list(top_freq.keys()), weights = list(top_freq.values()), k = 1)[0]
        
    def college_spin(rnk = 'div'):
        while True:
            if rnk == 'top_10':
                college = random.choices(list(top_10.keys()), weights = list(top_10.values()), k = 1)[0] # Top 10 spin
            elif rnk == 'conf':
                conf = get_division(temp_prestige)
                if conf != conf:
                    conf = DEFAUL_CONF # Default if error
                college = random.choice(list(all_colleges[all_colleges['Conference'] == conf]['College'])) # Conf spin
            elif rnk == 'div':
                div = get_division(temp_prestige)
                if div != div:
                    div = DEFAULT_DIV # Default if error
                college = random.choice(list(all_colleges[all_colleges['Division'] == div]['College'])) # Div spin

            # If the top 10 spin fails:
            if college == 'Random':
                if temp_prestige == 1:
                    college = college_spin('conf')
                else:
                    college = college_spin()
                break
            if college_list_total.count(college) < max_pos_draft_eligable[position]:
                break
            elif temp_prestige <= 13:
                if college_list_draftable.count(college) < max_pos_draftable[position]:
                    break
        return college
        
    beast = load_beast(defunct_colleges = False)
    beast = beast[beast['POS'] == position]
    history_draft = load_draft_history()
    history_draft = history_draft[history_draft['Year'] >= PASSING_ERA]
    all_colleges = load_college()

    # Get positional draft frequencies
    history_draft_pos = history_draft[history_draft['POS'] == position]
    pos_freq = add_missing_divisions((history_draft_pos['College'].value_counts(normalize = True)).to_dict())
    
    # Get top rounds frequencies. Use Conf instead of Div to narrow the field more in early rounds
    history_draft_data_top = history_draft_pos[history_draft_pos['Rnd'] <= draft_grades_round_cutoff['Top']]
    top_freq = history_draft_data_top['Conference'].value_counts(normalize = True).to_dict()
    if len(top_freq):
        top_freq = weights_to_one_dict(top_freq, max(top_freq, key = top_freq.get))
    else:
        top_freq = POWER_CONF

    # Get Middle rounds frequencies
    history_draft_data_mid = history_draft_pos[history_draft_pos['Rnd'] > draft_grades_round_cutoff['Top']]
    history_draft_data_mid = history_draft_data_mid[history_draft_data_mid['Rnd'] <= draft_grades_round_cutoff['Middle']]
    if len(history_draft_data_mid):
        mid_freq = add_missing_divisions((history_draft_data_mid['Division'].value_counts(normalize = True)).to_dict())
    else:
        mid_freq = POWER_DIV

    # Get Bottom rounds frequencies
    history_draft_data_bot = history_draft_pos[history_draft_pos['Rnd'] > draft_grades_round_cutoff['Middle']]
    if len(history_draft_data_bot):
        bot_freq = add_missing_divisions((history_draft_data_bot['Division'].value_counts(normalize = True)).to_dict())
    else:
        bot_freq = POWER_DIV

    # Get FA rounds frequencies
    #TODO: Get actual UDFA Data?
    history_draft_data_FA = beast[beast['Grade'] == 'FA']
    if len(history_draft_data_FA):
        FA_freq = add_missing_divisions((history_draft_data_FA['Division'].value_counts(normalize = True)).to_dict())
    else:
        FA_freq = POWER_DIV

    # Get RMC rounds frequencies
    history_draft_data_RMC = beast[beast['Grade'] == 'RMC']
    if len(history_draft_data_RMC):
        RMC_freq = add_missing_divisions((history_draft_data_RMC['Division'].value_counts(normalize = True)).to_dict())
    else:
        RMC_freq = POWER_DIV

    # Spin top 10 + 'Random'
    top_10 = weights_to_one_dict(dict(heapq.nlargest(10, pos_freq.items(), key = itemgetter(1))))
    
    college_list_return = []
    college_list_total = []
    college_list_draftable = []
    for i in range(0, size):
        temp_prestige = get_temp_prestige(prestige, i)
        college = college_spin('top_10') # Spin first of a top 10 university. The function will handle the rest

        if temp_prestige <= 13:
            college_list_draftable.append(college)
        college_list_total.append(college)
        college_list_return.append((college, temp_prestige))
        
    return college_list_return