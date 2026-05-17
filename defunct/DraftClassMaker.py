import pandas as pd
import random
from utility import *

import sys

#  List of names that need to be grammar-corrected
generational_suffixes = ['Jr.', 'Sr.', 'I', 'Ii', 'Iii', 'Iv', 'V', 'Vi', 'Vii', 'Viii', 'Ix', 'X']
special = ['J', 'K', 'Lequint', 'Mc', 'Rock']
double_name = ['Le', 'St.']
Upper = ['Aj', 'At', 'Bj', 'Cj', 'Dj', 'Dk', 'Ej', 'Jb', 'Jj', 'Jp', 'Jr', 'Jt', 'Kd', 'Kj', 'Kt', 'Ld', 'Lv', 'Mj', 'Oc', 'Pj', 'Rj', 'Tj']
Upper.extend(generational_suffixes)
Upper.remove('Jr.')
Upper.remove('Sr.')

first_count = {}
first_hyphen_total = 0
last_count = {}
last_hyphen_total = 0
suffix_count = {}
suffix_total = 0

#  Fills the first_count and first_hyphen_total variables, calculating statistical weights for first names
def first_name(s, first_count, first_hyphen_total):
    if '-' not in s:
        # Non-hyphenated names default to a weight of 2 to lessen the chance of a non-unique hyphenated name
        first_count[s] = first_count.get(s, 99) + 1
    else:
        first_hyphen_total += 1
        #  Seperate hyphenated names since they are not last names
        s = s.split('-')
        first_count[s[0]] = first_count.get(s[0], 0) + 1
        first_count[s[-1]] = first_count.get(s[-1], 0) + 1
    return first_count, first_hyphen_total

#  Fills the last_count and last_hyphen_total variables, calculating statistical weights for last names
def last_name(s, last_count, last_hyphen_total):
    if '-' not in s:
        # Non-hyphenated names default to a weight of 2 to lessen the chance of a non-unique hyphenated name
        last_count[s] = last_count.get(s, 99) + 1
    else:
        last_hyphen_total += 1
        #  Keep hyphenated names together for story line puropses
        last_count[s] = last_count.get(s, 0) + 1
        #  Also split the name and use both halves independantly in the dictionary 
        s = s.split('-')
        for name in s:
            last_count, last_hyphen_total = last_name(name, last_count, last_hyphen_total)
    return last_count, last_hyphen_total

#  Fills the suffix_count and suffix_total variables, calculating statistical weights for suffixes
def suffix(s, generational_suffixes, suffix_count, suffix_total, last_count, last_hyphen_total):
    if s not in generational_suffixes:
        last_count, last_hyphen_total = last_name(s, last_count, last_hyphen_total)
        return generational_suffixes, suffix_count, suffix_total, last_count, last_hyphen_total
    suffix_total += 1
    suffix_count[s] = suffix_count.get(s, 0) + 1
    return generational_suffixes, suffix_count, suffix_total, last_count, last_hyphen_total

#  Special title to fix str.title()'s apostrophe problem
def special_title(s:str):
    s = s.title()
    return s

#  Changes special names
def check_special(s:str):
    if len(s) > 2 and s[-2] == "'":
        s = s[:-1] + s[-1].lower()
    if s[:2] == 'Mc':
        return 'Mc' + s[2:].title()
    if s in special:
        if s == 'J':
            return random_name(0)
        elif s == 'K':
            return random_name(0)
        elif s == 'Lequint':
            return 'LeQuint'
        elif s == 'Rock':
            return random_name(0)
    return s        

#  Will re-spin the name if there is more than one hyphen
def check_hyphenated_grammar(arr, i):
    ret = []
    #  Avoid using any more than one hyphen
    for name in arr:
        while "-" in name:
            name = random_name(i)
        ret.append(name)
    # Avoid using names that end in an apostrophe as teh first numae in a hyphenated name
    if ret[0][-1] == "'":
        ret[0] = ret[0][:-1]
    return ret

#  Returns a random first name with argument 0, last name with argument 1, and suffix with argument 2
def random_name(n:int = -1):
    if n == 0:
        return check_special(random.choices(list(first_count.keys()), weights = list(first_count.values()), k = 1)[0])
    elif n == 1:
        return check_special(random.choices(list(last_count.keys()), weights = list(last_count.values()), k = 1)[0])
    elif n == 2:
        return check_special(random.choices(list(suffix_count.keys()), weights = list(suffix_count.values()), k = 1)[0])
    return 'ERROR_NAME'

def get_name(total):
    name = ''
    ret = []
    total = float(total)
    first_hyphen_percentage = (first_hyphen_total / total) * 10.0
    last_hyphen_percentage = (last_hyphen_total / total) * 10.0
    suffix_hyphen_percentage = (suffix_total / total) * 10.0

    #^ -- Get First Name -- ^#
    #TODO: Add a small chance of making a first name a last name???
    #  If the name is hyphenated, run the first name randomizer twice
    if (random.randrange(100000) / 1000.0) < first_hyphen_percentage:
        name = []
        hyphenated = []
        hyphenated.append(random_name(0))
        hyphenated.append(random_name(0))
        #  Rerun if more than one hyphen
        hyphenated = check_hyphenated_grammar(hyphenated, 0)
        #  Check for grammar adjustments and form name in name array
        for t in hyphenated:
            if t in Upper:
                name.append(t.upper())
            else:
                name.append(t)
        name = '-'.join(name)
    #  If no hyphen is needed, run the first name randomizer once
    else:
        name = random_name(0)
        #  Check for grammar adjustments
        if name in Upper:
            name = name.upper()
    # Append the first name to the return variable and clear the name variable for the last name
    ret.append(name)
    name = []
    hyphenated = []

    #^ -- Get Last Name -- ^#
    #  If the name is hyphenated, run the last name randomizer twice
    if (random.randrange(100000) / 1000.0) < last_hyphen_percentage:
        hyphenated.append(random_name(1))
        hyphenated.append(random_name(1))
        #  Rerun if more than one hyphen
        hyphenated = check_hyphenated_grammar(hyphenated, 1)
        #  Check for grammar adjustments and form name in name array
        for t in hyphenated:
            if t in Upper:
                name.append(t.upper())
            else:
                name.append(t)
        name = '-'.join(name)
    #  If no hyphen is needed, run the last name randomizer once
    else:
        name = random_name(1)
        if name in Upper:
            name = name.upper()
    # Append the last name to the return variable and clear the name variable for the last name
    ret.append(name)
    name = []

    #^ -- Get Suffix -- ^#
    #  If the name has a suffix, run the suffix randomizer once
    if (random.randrange(100000) / 1000.0) < suffix_hyphen_percentage:
        name = random_name(2)
        if name in Upper:
            name = name.upper()
        ret.append(name)

    #  Return final name joined by spaces
    return ' '.join(ret)

#---- MAKING THE DRAFT CLASS ----#
draft_class = pd.DataFrame()

#  Loading the data
draft_data = load_beast()

#_ Collecting DATA _#
# Get the historical draft rankings
grade_count_total = draft_data['Grade'].value_counts().to_dict()
grade_count_pos = {}
FA_count_pos = {}
RMC_count_pos = {}
total_count_pos = {}
for pos in draft_data['POS'].unique():
    temp = draft_data[draft_data['POS'] == pos].copy()
    grade_count_pos[pos] = temp[(temp['Grade'] != 'FA') & (temp['Grade'] != 'RMC')]['Grade'].count()
    FA_count_pos[pos] = temp[temp['Grade'] == 'FA']['Grade'].count()
    RMC_count_pos[pos] = temp[temp['Grade'] == 'RMC']['Grade'].count()
    total_count_pos[pos] = temp['Grade'].count()

# Get college and conference data
college = load_college()
draft_data = pd.merge(draft_data, college[['Beast', 'Nickname', 'City', 'State', 'Conference', 'Division', 'Other', 'Team_Name']], how = 'left', left_on = 'SCHOOL', right_on = "Beast")
draft_data = pd.merge(draft_data, college[['Beast', 'Nickname', 'City', 'State', 'Conference', 'Division', 'Other', 'Team_Name']], how = 'left', left_on = 'SCHOOL', right_on = "Other")
draft_data = merge_and_remove_x_y_cols(draft_data)
draft_data = draft_data.dropna(subset = 'Beast')
draft_data = draft_data.dropna(subset = 'Division')

#_ Building New Class _#
# Get random new draft class size
draft_class_size = {}
for pos in current_positions:
    temp = draft_data[draft_data['POS'] == pos].copy()
    pos_size = 0

    for year in DRAFT_FULL_DATA:
        temp = temp[temp['Year'] == year]
        pos_size += len(temp)
    pos_size = pos_size / len(DRAFT_FULL_DATA)
    draft_class_size[pos] = random.randint(min_rand(pos_size), max_rand(pos_size))

pos_list = []
for key, value in draft_class_size.items():
    for i in range(0, value + 1):
        pos_list.append(key)
draft_class['POS'] = pos_list

# Grading players
grades_total = []
for pos in current_positions:
    graded = grade_count_pos[pos] / total_count_pos[pos]
    udfa = FA_count_pos[pos] / total_count_pos[pos]
    pos_len = len(draft_class[draft_class['POS'] == pos])
    #TODO - Wrap into UTIL function?
    min_pos = (graded - 0.05)
    max_pos = (graded + 0.05)
    graded_pos = random.randrange(int(min_no_neg(min_pos) * pos_len), int(max_no_one(max_pos) * pos_len))
    grades = random_grades(graded_pos, pos)
    grades_total =  grades_total + grades

    min_pos = (udfa - 0.10)
    max_pos = (udfa + 0.10)
    udfa_pos = random.randrange(int(min_no_neg(min_pos) * pos_len), int(max_no_one(max_pos) * pos_len))
    grades_total =  grades_total + ['FA'] * udfa_pos
    grades_total =  grades_total + ['RMC'] * (pos_len - (graded_pos + udfa_pos))
draft_class['Grades'] = grades_total
draft_class['Grades_Numeric'] = draft_class['Grades'].map(draft_grades_to_numeric)

# Assigning Colleges
print(draft_class)
sys.exit()
#TODO: How should i do this with both positional and talent trends



#_ Names _#
draft_data['Name'] = draft_data['Name'].str.title()
nameCol = draft_data['Name'].str.split(' ')

#  Does the math to get the weighted name dictionaries
for i in nameCol:
    if len(i) == 2:
        first_count, first_hyphen_total = first_name(i[0], first_count, first_hyphen_total)
        last_count, last_hyphen_total = last_name(i[1], last_count, last_hyphen_total)
    elif len(i) == 3:
        first_count, first_hyphen_total = first_name(i[0], first_count, first_hyphen_total)
        #TODO: Does this work?
        if i[1] in double_name:
            last_count, last_hyphen_total = last_name(' '.join(i[1:3]), last_count, last_hyphen_total)
        else:
            last_count, last_hyphen_total = last_name(i[1], last_count, last_hyphen_total)
            generational_suffixes, suffix_count, suffix_total,last_count, last_hyphen_total = suffix(i[2], generational_suffixes, suffix_count, suffix_total, last_count, last_hyphen_total)

#  Creates all the names
names_list = []
for i in range(0, len(draft_class)):
    names_list.append(get_name(len(nameCol)))
draft_class['Name'] = names_list

# Sort
draft_class['Rnd_Pick'] = np.random.rand(len(draft_class))
draft_class.sort_values(by = ['Grades_Numeric', 'Rnd_Pick'], inplace = True)
draft_class.reset_index(drop = True, inplace = True)
draft_class['Rnd_Pick'] = draft_class.index + 1
draft_class = draft_class[['Name', 'POS', 'Grades', 'Rnd_Pick']]

print(draft_class)
# print(grade_count_pos)
# print(FA_count_pos)
# print(RMC_count_pos)
# print(total_count_pos)


