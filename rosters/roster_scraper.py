import pandas as pd
import urllib.request
import re
from bs4 import BeautifulSoup
import csv



#football = pd.ExcelFile('Football Dictionary.xlsx')
#df = football.parse(football.sheet_names[0])
#file = csv.writer(open('football_rosters', 'w'))
#league = 'nfl'

#baseball = pd.ExcelFile('Baseball Dictionary.xlsx')
#df = baseball.parse(baseball.sheet_names[0])
#file = csv.writer(open('baseball_rosters', 'w'))
#league = 'mlb'

basketball = pd.ExcelFile('Basketball Dictionary.xlsx')
df = basketball.parse(basketball.sheet_names[0])
file = csv.writer(open('basketball_rosters', 'w'))
league = 'nba'

team_dict = {}
for index, row in df.iterrows():
    team_name = row['Team Name']
    team_url = row['ESPN url']
    i = team_url.find('_/name/')
    roster_url = team_url[:i] + 'roster/' + team_url[i:]
    content = urllib.request.urlopen(roster_url)
    content = BeautifulSoup(content, 'lxml')
    names = []
    for tagged in content.find_all('a', {'href': re.compile('espn\.com\/'+ league + '\/player\/')}):
        names.append(tagged.getText())

    team_dict[team_name] = names

for key, val in team_dict.items():
    file.writerow([key, val])
