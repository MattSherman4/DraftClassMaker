from .variables import *
import pandas as pd
import json

#_ Load Data _#
#  Load Beast data for specific year(s), blank or all for all data
def load_beast(years = ''):
    if years == '' or years.lower() == 'all':
        years = DRAFT_AVAILABLE_DATA
    
    if not isinstance(years, list):
        draft_data = pd.read_excel(f'C:/Users/pensh/Desktop/VSCode/DataBase/Data/Draft/Beast{years}.xlsx', sheet_name = 'Combine')
        draft_data['Year'] = years
        return draft_data
    
    draft_data = []
    for year in years:
        temp = pd.read_excel(f'C:/Users/pensh/Desktop/VSCode/DataBase/Data/Draft/Beast{year}.xlsx', sheet_name = 'Combine')
        temp['Year'] = year
        draft_data.append(temp)
    draft_data = pd.concat(draft_data)
    draft_data.reset_index(inplace = True)
    return draft_data

#  Load draft history data
def load_draft_history():
    return pd.read_csv('C:/Users/pensh/Desktop/VSCode/DataBase/Data/Draft/Sports_Ref_Draft.csv')

# Loads all players in draft/Beast databases
def load_draft_all():
    beast = load_beast()[['Year', 'Name', 'POS', 'SCHOOL']]
    beast = beast.rename(columns = {'Name' : 'Player', 'POS' : 'Pos', 'SCHOOL' : 'College'})
    sf = load_draft_history()
    df = sf.merge(beast, how = 'outer', on = ['Year', 'Player'])
    df = df.drop_duplicates(subset = ['Year', 'Player'], keep = 'first')
    df['Rnd'] = df['Rnd'].fillna(-1.0)
    df['Pick'] = df['Pick'].fillna(-1.0)
    df['Rnd_Pick'] = df['Rnd_Pick'].fillna(-1.0)
    df = merge_and_remove_x_y_cols(df)

    return df

#  Load collge data
def load_college():
    return pd.read_csv('C:/Users/pensh/Desktop/VSCode/DataBase/Data/Teams/College_Teams.csv')

#  Load college to division json data
def load_conference_to_division():
    with open('C:/Users/pensh/Desktop/VSCode/DataBase/Data/Leagues/Conference_To_Division.json', 'r') as f:
        conference_to_division = json.load(f)
    return conference_to_division