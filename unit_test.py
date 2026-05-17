from utility import *

# Beast not missing colleges
beast = load_beast(defunct_colleges = False)
beast_missing_colleges = beast[beast['College'] == 'DNP']
if len(beast_missing_colleges):
    print(f"FAIL: Beast is missing colleges:")
    print(beast_missing_colleges)
else:
    print(f"PASS")

# Beast not missing divisions
beast = load_beast(defunct_colleges = False)
beast_missing_colleges = beast[beast['Division'] == 'DNP']
if len(beast_missing_colleges):
    print(f"FAIL: Beast is missing divisions:")
    print(beast_missing_colleges)
else:
    print(f"PASS")

# Beast not missing conferences
beast = load_beast(defunct_colleges = False)
beast_missing_colleges = beast[beast['Conference'] == 'DNP']
if len(beast_missing_colleges):
    print(f"FAIL: Beast is missing conferences:")
    print(beast_missing_colleges)
else:
    print(f"PASS")

colleges = load_college()
fbs = colleges[colleges['Division'] == 'FBS']
for conference in fbs['Conference'].unique():
    print(f"Conference: {conference}")
    teams = list(fbs[fbs['Conference'] == conference]['College'])
    for team in teams:
        print(f"\t{team}")