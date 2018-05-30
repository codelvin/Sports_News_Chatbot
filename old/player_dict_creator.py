def get_player_id(team):
    #player is player's name, team is HIS team, date is the date when the game happens
    team_info = pd.read_excel('../teamDictionaries/Basketball Dictionary.xlsx')
    abbrev = team_info[team_info['Team Name'] == team]['ESPN url'].iloc[0]
    abbrev = abbrev.split(r'/')[7]
    
    page = "http://www.espn.com/nba/team/stats/_/name/"+abbrev
    driver.get(page)
    src = driver.page_source             # source html
    pretty_src = BeautifulSoup(src,"lxml")
#     string = str(pretty_src).split('\n')
#     for each in string:
#         if each.find('player')!=-1
    pretty_src = pretty_src.find('div', class_ = 'mod-container mod-table')
    table = pretty_src.find('div', class_ = 'mod-content')
    players = table.findAll(name = 'tr', attrs = {"class":re.compile(r".*player.*")})
    for each in players:
        player_site[each.td.a.string] = each.td.a.get('href')
    
    
player_site = {}
team_dict = pd.read_excel('../teamDictionaries/Basketball Dictionary.xlsx')
teams = team_dict['Team Name']
for each in teams:
    get_player_id(each)


df = pd.DataFrame(list(player_site.items()), columns = ['Player Name','Player Website'])
df.to_csv('../playerDictionaries/players_website.csv', index=False)