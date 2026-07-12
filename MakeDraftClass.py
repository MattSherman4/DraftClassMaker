from utility import *

from collections import Counter

#---- MAKING THE DRAFT CLASS ----#
draft_class = pd.DataFrame()

#  Loading the data
beast = load_beast()
history_draft = load_draft_all()

#_ Collecting DATA _#
# Get the historical draft rankings by position
grade_count_total = beast['Grade'].value_counts().to_dict()
grade_count_pos = {}
FA_count_pos = {}
RMC_count_pos = {}
total_count_pos = {}
for pos in beast['POS'].unique():
    temp = beast[beast['POS'] == pos].copy()
    grade_count_pos[pos] = temp[(temp['Grade'] != 'FA') & (temp['Grade'] != 'RMC')]['Grade'].count()
    FA_count_pos[pos] = temp[temp['Grade'] == 'FA']['Grade'].count()
    RMC_count_pos[pos] = temp[temp['Grade'] == 'RMC']['Grade'].count()
    total_count_pos[pos] = temp['Grade'].count()

#_ Building New Class _#
# Get random new draft class size
draft_class_size = {}
for pos in current_positions:
    temp = beast[beast['POS'] == pos].copy()
    pos_size = 0

    for year in DRAFT_FULL_DATA:
        temp = temp[temp['Year'] == year]
        pos_size += len(temp)

    pos_size = pos_size / len(DRAFT_FULL_DATA)
    draft_class_size[pos] = random.randint(min_rand(pos_size), max_rand(pos_size))

# Converts the draft_class_size[pos] dictionary to a list
pos_list = []
for key, value in draft_class_size.items():
    for i in range(0, value + 1):
        pos_list.append(key)
        
# Add values into final draft class database 
draft_class['POS'] = pos_list

# Adding side of ball based on position mapping
draft_class["Side"] = draft_class["POS"].map(pos_abr_to_side)

# Adding position numeric (for sorting) based on position mapping
draft_class["POS_Numeric"] = draft_class["POS"].map(pos_abr_to_num)

#_ Creating Players _#
# Creating names
names = get_name(size = len(draft_class))

# Add values into final draft class database 
draft_class['Name'] = names

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

# Add values into final draft class database 
draft_class['Grade'] = grades_total
draft_class['Grades_Numeric'] = draft_class['Grade'].map(draft_grades_to_numeric)
draft_class['Prestige'] = get_prestige(draft_class)

# Adding colleges
draft_class = draft_class.assign(College = np.nan)
for pos in current_positions:
    temp_class = draft_class[draft_class['POS'] == pos].copy()
    college_list = get_college(size = len(temp_class),  position = pos, prestige = list(draft_class['Prestige']))
    college_list = [l[0] for l in sorted(college_list, key = lambda x: x[1])]
    temp_class = temp_class.sort_values(['Grades_Numeric'])
    temp_class['College'] = college_list
    draft_class = merge_and_remove_x_y_cols(draft_class.join(temp_class, on = list(temp_class.columns).remove('College'), how = 'left', lsuffix = "_x", rsuffix = "_y"))

print(draft_class.sort_values(['Grades_Numeric', 'POS_Numeric']).reset_index(drop = True).head(32)[['POS', 'Name', 'Grade', 'College']])
draft_class.sort_values(['Grades_Numeric', 'POS_Numeric']).reset_index(drop = True)[['POS', 'Name', 'Grade', 'College']].to_csv('output.csv')
