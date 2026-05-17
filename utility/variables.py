import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap

# FINAL variables
MODERN_ERA = 1970
PASSING_ERA = 2004
DRAFT_FULL_DATA = [2025]
DEFAULT_DIV = 'FBS'
DEFAUL_CONF = 'SEC'
POWER_CONF = {'SEC' : 0.25, 'Big Ten' : 0.25, 'ACC' : 0.25, 'Big 12' : 0.25}
POWER_DIV = {'FBS' : 0.90, 'FCS' : 0.09, 'DII' : 0.01}

# Naming conventions
generational_suffixes = ['Jr.', 'Sr.', 'I', 'Ii', 'Iii', 'Iv', 'V', 'Vi', 'Vii', 'Viii', 'Ix', 'X']
special = ['J', 'K', 'Lequint', 'Mc', 'Rock']
double_name = ['Le', 'St.']
Upper = ['Aj', 'At', 'Bj', 'Cj', 'Dj', 'Dk', 'Ej', 'Jb', 'Jj', 'Jp', 'Jr', 'Jt', 'Kc', 'Kd', 'Kj', 'Kt', 'Ld', 'Lv', 'Mj', 'Oc', 'Pj', 'Rj', 'Tj']
Upper.extend(generational_suffixes)
Upper.remove('Jr.')
Upper.remove('Sr.')

# Currently available positions. Could be changed with storylines later on
current_positions = ['QB', 'HB', 'WR', 'TE', 'OT', 'OG', 'C', 'EDGE', 'DT', 'MLB', 'CB', 'S', 'K', 'P', 'LS']

# Converts position abbreviations to full names
pos_abr_to_full = {'QB' : 'Quarterback', 'HB' : 'Runningback',
                'WR' : 'Wide Receiver', 'TE' : 'Tight End',
                'OT' : 'Offensive Tackle', 'OG' : 'Offensive Guard',
                'C' : 'Center', 'EDGE' : 'Edge Rusher',
                'DT' : 'Defensive Tackle', 'MLB' : 'Middle Linebacker',
                'CB' : 'Cornerback', 'S' : 'Safety',
                'K' : 'Kicker', 'P' : 'Punter', 'LS' : 'Long Snapper',
                'ALL' : 'All Positions'}

# Converts position abbreviations to side of ball
pos_abr_to_side = {'QB' : 'OFF', 'HB' : 'OFF',
                'WR' : 'OFF', 'TE' : 'OFF',
                'OT' : 'OFF', 'OG' : 'OFF',
                'C' : 'OFF', 'EDGE' : 'DEF',
                'DT' : 'DEF', 'MLB' : 'DEF',
                'CB' : 'DEF', 'S' : 'DEF',
                'K' : 'ST', 'P' : 'ST', 'LS' : 'ST'}

# Maximum players in a draft with a draftable grade (prestige <= 13)
max_pos_draftable = {'QB' : 1, 'HB' : 2, 'WR' : 3, 'TE' : 2,
                'OT' : 2, 'OG' : 2, 'C' : 2, 'EDGE' : 3,
                'DT' : 2, 'MLB' : 3, 'CB' : 3, 'S' : 3,
                'K' : 1, 'P' : 1, 'LS' : 1}

# Maximum players in a draft with a draft eligable grade (prestige > 13)
max_pos_draft_eligable = {'QB' : 4, 'HB' : 5, 'WR' : 10, 'TE' : 5,
                'OT' : 6, 'OG' : 6, 'C' : 4, 'EDGE' : 8,
                'DT' : 8, 'MLB' : 6, 'CB' : 10, 'S' : 7,
                'K' : 2, 'P' : 2, 'LS' : 2}

# Converts side of ball abbreviation to full
pos_side_to_full = {'OFF' : 'Offense', 'DEF' : 'Defense',
                'ST' : 'Special Teams',}

# Arbetrary position rankings for sorting purposes
pos_abr_to_num = {'QB' : 1, 'HB' : 2, 'WR' : 3, 'TE' : 4,
                'OT' : 5, 'OG' : 6, 'C' : 7, 'EDGE' : 8,
                'DT' : 9, 'MLB' : 10, 'CB' : 11, 'S' : 12,
                'K' : 13, 'P' : 14, 'LS' : 15}

# Normalizes position names - removes unused positions
normalize_pos = {'RB' : 'HB', 'SAF' : 'S', 'ILB' : 'MLB', 'T' : 'OT', 'G' : 'OG', 'OLB' : 'EDGE', 'DE' : 'EDGE',
                 'FS' : 'S', 'NT' : 'DT', 'DL' : 'DT'}

# Converts combine stat abbreviations to full names
combine_stat_abr_to_full = {'HT_IN' : 'Height (Inches)', 'WT' : 'Weight',
               'BMI' : 'BMI', 'HAND' : 'Hand Measurement',
               'ARM' : 'Arm Length', 'WING' : 'Wing Span',
               '40' : '40 Yard Dash', '20' : '20 Yard Dash',
               '10' : '10 Yard Dash', 'VJ' : 'Vertical Jump',
               'SS' : '20-Yard Shuttle', '3C' : '3 Cone Drill',
               'BP' : 'Bench Press', 'AGE' : 'Age'}

# List of possible grades in Beast
beast_grades_all = ['1st', '1st-2nd', '2nd', '2nd-3rd', '3rd', '3rd-4th', '4th', '4th-5th', '5th', '5th-6th', '6th', '6th-7th', '7th', 'FA', 'RMC']

# Converts draft grades to numeric
draft_grades_to_numeric = {'1st' : 1, '1st-2nd' : 2, '2nd' : 3, '2nd-3rd' : 4,
                '3rd' : 5, '3rd-4th' : 6, '4th' : 7, '4th-5th' : 8,
                '5th' : 9, '5th-6th' : 10, '6th' : 11,
                '6th-7th' : 12, '7th' : 13, 'FA' : 14, 'RMC' : 15}

# Cutoffs for converting draft grade to prospect prestige
draft_grades_prestige_cutoff = {1 : 2, 2 : 6, 3 : 13, 4 : 14, 5 : 15}
draft_grades_round_cutoff = {'Top' : 1, 'Middle': 3, 'Bottom' : 7, 'FA' : 'FA', 'RMC' : 'RMC'}

# Number of players expected for each grade - analyzes the strength of each draft past and present
draft_expected_grades = {'1st' : 17, '1st-2nd' : 17, '2nd' : 17, '2nd-3rd' : 17,
                '3rd' : 21, '3rd-4th' : 21, '4th' : 21, '4th-5th' : 21,'5th' : 21, 
                '5th-6th' : 21, '6th' : 21, '6th-7th' : 21, '7th' : 21}

# Colormapping for plotting
cmap = plt.cm.turbo_r(np.linspace(0, 0.95))
cmap = LinearSegmentedColormap.from_list("turbo_cust", cmap)
cmap_r = plt.cm.turbo(np.linspace(0.05, 1))
cmap_r = LinearSegmentedColormap.from_list("turbo_cust_r", cmap_r)
cmap_red = plt.cm.turbo(np.linspace(0.5, 0.95))
cmap_red = LinearSegmentedColormap.from_list("turbo_red", cmap_red)
cmap_blue = plt.cm.turbo_r(np.linspace(0.5, 0.95))
cmap_blue = LinearSegmentedColormap.from_list("turbo_blue", cmap_blue)