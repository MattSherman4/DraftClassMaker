from .util_Data import *
from .variables import *
import random

#_ Removing Duplicates for combine and proday data _#
#  Gets only a single instance of every player. Keep determines which Type take precedence.
#  Avoids combine_first to make sure data is linked to correct row.
def remove_dups_combine_proday(df, keep = 'combine'):
    if keep == 'combine':
        to_delete = '_p'
        suffixes = (None , to_delete)
    elif keep == 'proday':
        to_delete = '_c'
        suffixes = (to_delete , None)
    elif keep == 'both':
        to_delete = ''
        suffixes = ('_c' , '_p')
    else:
        with open("error_log.txt", "w") as file:
            file.write("ERROR - Invalid remove_dups keep type. Defaulting to combine.\n")
        remove_dups_combine_proday(df)

    p = df[df['Type'] == 'p'].copy()
    c = df[df['Type'] == 'c'].copy()

    df = c.merge(p, on = ['RK', 'Name', 'POS', 'SCHOOL', 'Grade', 'Year', 'AGE'], suffixes = suffixes)
    if to_delete != '':
        dup_cols =  [x for x in df.columns if x[-2:] == to_delete]

        for col in dup_cols:
            col_to_keep  = col[:-2]
            df[col_to_keep] = df[col_to_keep].fillna(df[col])

        df = df.drop(columns = (dup_cols + ['Type']))
    return df.copy()

#- Class Creation Utils -#
#_ Determines draft grades for positions _#
# size = number of draft-grade players, pos = position
def random_grades(size, pos): 
    #! More efficient way to load this data in? !#
    draft_data = load_draft_history()
    draft_data = draft_data[(draft_data['Year'] >= PASSING_ERA)]
    draft_data['POS'] = draft_data['POS'].map(normalize_pos).fillna(draft_data['POS'])

    draft_data = draft_data[draft_data['POS'] == pos].copy()
    pos_len = len(draft_data)
    weight_1 =  len(draft_data[draft_data['Pick'] <= 17]) / pos_len
    weight_12 =  len(draft_data[((draft_data['Pick'] > 17) & (draft_data['Pick'] <= 34))]) / pos_len
    weight_2 =  len(draft_data[((draft_data['Pick'] > 34) & (draft_data['Pick'] <= 51))]) / pos_len
    weight_23 =  len(draft_data[(draft_data['Pick'] > 51) & (draft_data['Pick'] <= 68)]) / pos_len
    weight_3 =  len(draft_data[(draft_data['Pick'] > 68) & (draft_data['Pick'] <= 89)]) / pos_len
    weight_34 =  len(draft_data[(draft_data['Pick'] > 89) & (draft_data['Pick'] <= 110)]) / pos_len
    weight_4 =  len(draft_data[(draft_data['Pick'] > 110) & (draft_data['Pick'] <= 131)]) / pos_len
    weight_45 =  len(draft_data[(draft_data['Pick'] > 131) & (draft_data['Pick'] <= 152)]) / pos_len
    weight_5 =  len(draft_data[(draft_data['Pick'] > 152) & (draft_data['Pick'] <= 173)]) / pos_len
    weight_56 =  len(draft_data[(draft_data['Pick'] > 173) & (draft_data['Pick'] <= 194)]) / pos_len
    weight_6 =  len(draft_data[(draft_data['Pick'] > 194) & (draft_data['Pick'] <= 215)]) / pos_len
    weight_67 =  len(draft_data[(draft_data['Pick'] > 215) & (draft_data['Pick'] <= 236)]) / pos_len
    weight_7 =  len(draft_data[(draft_data['Pick'] > 236) & (draft_data['Pick'] <= 257)]) / pos_len
    
    weights = [weight_1, weight_12, weight_2, weight_23, weight_3, weight_34, weight_4, weight_45, weight_5, weight_56, weight_6, weight_67, weight_7]
    weights = weights_to_one(weights)
    
    draft_grades_to_numeric_reversed = {value: key for key, value in draft_grades_to_numeric.items()} 
    grades = random.choices(np.arange(1, 14), weights = weights, k = size)
    grades = [draft_grades_to_numeric_reversed[grade] for grade in grades]
    return grades
