from .util_LoadData import *
import numpy as np

#- Calculation Utils -#
#_ Height Conversions _#
#  Converts standard 4 digit combine height to readable FT'IN" format
def combine_height_to_inches(height_list):
    height_list = [str(h) for h in height_list]
    return [float((int(h[0]) * 12) + (int(h[1:3])) + (int(h[3]) / 8)) if h != 'nan' else 'nan' for h in height_list]

#  Converts readable FT'IN" height to standard 4 digit combine format
def inches_to_combine_height(height_list):
    height_list = [float(h) for h in height_list]
    return [int(float(str(int(h) // 12) + str(int(h) % 12).zfill(2) + str((h - int(h)) * 8))) if str(h) != 'nan' else np.nan for h in height_list]

#_ List Operations _#
# Makes sure a list of weights equals one
def weights_to_one(weights_list, addition_position : int = -1):
    weights_list[addition_position] += 1 - sum(weights_list)
    return weights_list

#- Data Corrections -#
#_ Working With Randoms _#
# Returns a bottom bounds for a random number with a default artificial bounds of +- 0.3
def min_rand(i, bounds = 0.7):
    return int(i * bounds)

# Returns a top bounds for a random number with a default artificial bounds of +- 0.3
def max_rand(i, bounds = 1.3):
    return int(i * bounds)

# Makes sure random will not return a negative value
def min_no_neg(i):
    if i < 0:
        return 0
    else:
        return i
    
# Makes sure random will not return a value greater than 1
def max_no_one(i):
    if i > 1:
        return 1
    else:
        return i

# Remove and merges duplicate columns
def merge_and_remove_x_y_cols(df):
    cols = [str(s) for s in df.columns.tolist()]
    x = [str(x) for x in cols if x[-2:] == '_x']
    y = [str(y) for y in cols if y[-2:] == '_y']
    base = [base[:-2] for base in x]

    for i in range(0, len(base)):
        df = df.rename(columns = {x[i] : base[i]})
        df[base[i]] = df[base[i]].fillna(df[y[i]])
        df = df.drop(y[i], axis = 1)

    return df.copy()

#- Intermediate Table Mapping -#
#_ Colleges _#
# Mapping college names
def map_college(df, df_col, col_to_keep, col_on, Nickname = False, City = False, State = False, Conference = False, Division = False):
    colleges = load_college()
    if (col_to_keep not in colleges.columns) or (col_on not in colleges.columns):
        return df

    keep = df.columns.to_list()
    df = df.merge(colleges, left_on = df_col, right_on = col_on, how = 'left')
    df = df.merge(colleges, left_on = df_col, right_on = 'Other', how = 'left', suffixes = ('', '_y'))
    df[col_to_keep] = df[col_to_keep].fillna(df['Other_y'])
    
    keep.append(col_to_keep)
    if Nickname:
        keep.append('Nickname')
        df['Nickname'] = df['Nickname'].fillna(df['Nickname_y'])
    if City:
        keep.append('City')
        df['City'] = df['City'].fillna(df['City_y'])
    if State:
        keep.append('State')
        df['State'] = df['State'].fillna(df['State_y'])
    if Conference:
        keep.append('Conference')
        df['Conference'] = df['Conference'].fillna(df['Conference_y'])
    if Division:
        keep.append('Division')
        df['Division'] = df['Division'].fillna(df['Division_y'])

    return df[keep].dropna()