
import sys
import configparser
from .variables import *
import pandas as pd
import numpy as np
import json
from pathlib import Path

#-  _        _______  _______  ______     ______   _______ _________ _______   
#- ( \      (  ___  )(  ___  )(  __  \   (  __  \ (  ___  )\__   __/(  ___  )  
#- | (      | (   ) || (   ) || (  \  )  | (  \  )| (   ) |   ) (   | (   ) |  
#- | |      | |   | || (___) || |   ) |  | |   ) || (___) |   | |   | (___) |  
#- | |      | |   | ||  ___  || |   | |  | |   | ||  ___  |   | |   |  ___  |  
#- | |      | |   | || (   ) || |   ) |  | |   ) || (   ) |   | |   | (   ) |  
#- | (____/\| (___) || )   ( || (__/  )  | (__/  )| )   ( |   | |   | )   ( |  
#- (_______/(_______)|/     \|(______/   (______/ |/     \|   )_(   |/     \|  
                
                                                                            
#_ Load Data _#
#  Load a config file
def load_cfg(name:str = ""):
    if name == "":
        print("ERROR - Inalid 'name' variable in util_Data.load_cfg()")
        sys.exit()

    parent_dir = Path(__file__).resolve().parent.parent
    name = name.replace(" ", "_")
    name = name.lower()
    name = parent_dir / f"Data/{name}.cfg"
    cfg = configparser.ConfigParser()
    try:
        cfg.read(name, encoding = 'utf-8')
    except:
        cfg.read(name)
    return cfg

#  Load Beast data for specific year(s), blank or all for all data
def load_beast(years = '', defunct_colleges = True):
    if years == '' or years.lower() == 'all':
        years = DRAFT_FULL_DATA
    
    # Importing Combine stats
    if isinstance(years, int):
        beast_Combine = pd.read_excel(f'C:/Users/pensh/Desktop/VSCode/DataBase/Data/Draft/Beast{years}.xlsx', sheet_name = 'Combine')
        beast_Combine['Year'] = years
    else:
        beast_Combine = []
        for year in years:
            temp = pd.read_excel(f'C:/Users/pensh/Desktop/VSCode/DataBase/Data/Draft/Beast{year}.xlsx', sheet_name = 'Combine')
            temp['Year'] = year
            beast_Combine.append(temp)
        beast_Combine = pd.concat(beast_Combine)
        beast_Combine.reset_index(inplace = True)

    # Importing ProDay stats
    if isinstance(years, int):
        beast_ProDay = pd.read_excel(f'C:/Users/pensh/Desktop/VSCode/DataBase/Data/Draft/Beast{years}.xlsx', sheet_name = 'ProDay')
        beast_ProDay['Year'] = years
    else:
        beast_ProDay = []
        for year in years:
            temp = pd.read_excel(f'C:/Users/pensh/Desktop/VSCode/DataBase/Data/Draft/Beast{year}.xlsx', sheet_name = 'ProDay')
            temp['Year'] = year
            beast_ProDay.append(temp)
        beast_ProDay = pd.concat(beast_ProDay)
        beast_ProDay.reset_index(inplace = True)

    # Merge combine and proday, prioritizing combine
    beast = merge_and_remove_x_y_cols(pd.merge(beast_Combine, beast_ProDay, on = ['RK', 'Name', 'POS', 'SCHOOL', 'Year']).replace('DNP', np.nan))

    # Remove defunct colleges is needed
    if not defunct_colleges:
        beast = beast.rename(columns = {'SCHOOL' : 'College'})
        beast = remove_defunct_colleges(beast)
        beast = beast.rename(columns = {'College' : 'SCHOOL'})

    # Normalizing data
    beast['Name'] = check_name_grammar(name = list(beast['Name']))
    beast['POS'] = beast['POS'].map(normalize_pos).fillna(beast['POS'])
    beast = map_college(beast, 'SCHOOL', 'Beast', 'College')

    # Remove unwanted data
    beast = beast.drop(columns = ['index', 'SCHOOL']).fillna('DNP')

    return beast

#  Load draft history data
def load_draft_history(stats = False):
    sports_ref = pd.read_csv('C:/Users/pensh/Desktop/VSCode/DataBase/Data/Draft/Sports_Ref_Draft.csv')

    # Normalizing data
    sports_ref = sports_ref.rename(columns = {'College' : 'SCHOOL', 'Pos' : 'POS'})
    sports_ref['POS'] = sports_ref['POS'].map(normalize_pos).fillna(sports_ref['POS'])
    sports_ref = map_college(sports_ref, 'SCHOOL', 'Sports_Reference', 'College')
    sports_ref = sports_ref.rename(columns = {'College' : 'College_x', 'Nickname' : 'Nickname_x', 'City' : 'City_x', 'State' : 'State_x', 'Conference' : 'Conference_x', 'Division' : 'Division_x'})
    sports_ref = map_college(sports_ref, 'SCHOOL', 'Torvik', 'College')
    sports_ref = sports_ref.rename(columns = {'College' : 'College_y', 'Nickname' : 'Nickname_y', 'City' : 'City_y', 'State' : 'State_y', 'Conference' : 'Conference_y', 'Division' : 'Division_y'})
    sports_ref = merge_and_remove_x_y_cols(sports_ref)
    sports_ref = sports_ref.rename(columns = {'Player' : 'Name'})

    # Remove unwanted data
    if not stats:
        sports_ref = sports_ref[['Year', 'Rnd', 'Pick', 'Rnd_Pick', 'Team', 'Name', 'POS', 'Age', 'College', 'Conference', 'Division']]
    return sports_ref

# Loads all players in draft/Beast databases
def load_draft_all(clean_names = True):
    # Load data
    sf = load_draft_history()
    beast = load_beast()[['Year', 'Name', 'POS', 'College', 'Grade']]
    #TODO: Find a way to drop 'Grade'? 

    # Merge Data
    df = sf.merge(beast, how = 'outer', on = ['Year', 'Name', 'POS', 'College'])
    
    # Remove "  HOF" from names
    if clean_names:
        df['Name'] = df['Name'].str.replace(r" \(.*\)", "", regex = True).str.replace(r"  HOF", "")

    return df

#  Load collge data
def load_college(defunct = False):
    df = pd.read_csv('C:/Users/pensh/Desktop/VSCode/DataBase/Data/Teams/College_Teams.csv')
    if not defunct:
        df = remove_defunct_colleges(df)
    return df

#  Load college to division json data
def load_conference_to_division():
    with open('C:/Users/pensh/Desktop/VSCode/DataBase/Data/Leagues/Conference_To_Division.json', 'r') as f:
        conference_to_division = json.load(f)
    return conference_to_division





#- _______  _______  _                 _______  _______ __________________ _______  _        _______ 
#- (  ____ \(  ___  )( (    /||\     /|(  ____ \(  ____ )\__   __/\__   __/(  ___  )( (    /|(  ____ \
#- | (    \/| (   ) ||  \  ( || )   ( || (    \/| (    )|   ) (      ) (   | (   ) ||  \  ( || (    \/
#- | |      | |   | ||   \ | || |   | || (__    | (____)|   | |      | |   | |   | ||   \ | || (_____ 
#- | |      | |   | || (\ \) |( (   ) )|  __)   |     __)   | |      | |   | |   | || (\ \) |(_____  )
#- | |      | |   | || | \   | \ \_/ / | (      | (\ (      | |      | |   | |   | || | \   |      ) |
#- | (____/\| (___) || )  \  |  \   /  | (____/\| ) \ \__   | |   ___) (___| (___) || )  \  |/\____) |
#- (_______/(_______)|/    )_)   \_/   (_______/|/   \__/   )_(   \_______/(_______)|/    )_)\_______)

# Convert name to proper grammar
#TODO: Combine this with util_Player Creation
def check_name_grammar(name:list):
    ret = []
    for n in name:
        n = n.title()
        if n in Upper:
            name = name.upper()
        if len(n) > 2 and n[-2] == "'":
            n = n[:-1] + n[-1].lower()
        if n[:2] == 'Mc':
            return 'Mc' + n[2:].title()
        if n in special:
            if n == 'Lequint':
                n = 'LeQuint'
        ret.append(n)

    return ret   

# Returns prestige given a draft grade(s)
def get_prestige(prestige):
    try:
        prestige = list(prestige['Grades_Numeric'])
    except:
        pass
    
    if isinstance(prestige, int):
        prestige = [prestige]
    
    prestige_list = []
    for val in prestige:
        if val <= draft_grades_prestige_cutoff[1]:
            prestige_list.append(1)
        elif val <= draft_grades_prestige_cutoff[2]:
            prestige_list.append(2)
        elif val <= draft_grades_prestige_cutoff[3]:
            prestige_list.append(3)
        elif val == draft_grades_prestige_cutoff[4]:
            prestige_list.append(4)
        else:
            prestige_list.append(5)
    return prestige_list

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
def weights_to_one(weights_list, addition_position : int = -1, append = False):
    if append:
        weights_list.append(1 - sum(weights_list))
        return weights_list
    
    weights_list[addition_position] += 1 - sum(weights_list)
    return weights_list

# Adds up weights to 1 in dict
def weights_to_one_dict(weights_dict, key = 'Random'):
    total = sum(weights_dict.values())
    old_num = weights_dict.get(key, 0)
    weights_dict[key] = 1 - total + old_num
    return weights_dict

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

#_ DataBase Operations _#
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

# Removes rows from a DataFrame if the college no longer has a football program or I do not want to track
def remove_defunct_colleges(df):
    df = df[df['College'] != 'Limestone'] # Defunct
    df = df[df['College'] != 'Mississippi College'] # Defunct
    df = df[df['College'] != 'Iowa Western CC'] # Huntere Dekkers outlier
    df = df[df['College'] != 'Northwestern (Ia.)'] # Cannot get this disentangled with the good Northwestern

    return df.copy()


# Add missing divisions to dictionary
def add_missing_divisions(grades_dict):
    #TODO: Load in just teh division data to improve speed?
    college = load_college()
    for division in list(college['Division'].unique()):
        grades_dict.setdefault(division, 0.0)
    grades_dict = weights_to_one_dict(grades_dict, key = 'FBS')
    return grades_dict

#- Intermediate Table Mapping -#
#_ Colleges _#
# Mapping college names
def map_college(df, df_col, col_on, col_to_keep, Nickname = True, City = True, State = True, Conference = True, Division = True):
    colleges = load_college()
    if (col_to_keep not in colleges.columns) or (col_on not in colleges.columns):
        return df

    keep = df.columns.to_list()
    df = df.merge(colleges, left_on = df_col, right_on = col_on, how = 'left')
    df = df.dropna(subset = [df_col])
    df = df.merge(colleges, left_on = df_col, right_on = 'Other', how = 'left', suffixes = ('', '_y'))
    df = df.dropna(subset = [df_col])
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

    return df[keep]
                                                                                                                                         