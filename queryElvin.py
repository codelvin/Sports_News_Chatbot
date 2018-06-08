from selenium import webdriver
from bs4 import BeautifulSoup
import re
import os
import pandas as pd


def date_convert(date):
    # change from 03-28-18 to 20180328
    return '20' + date[-2:] + date[0:2] + date[3:5]


def get_query(list):
    # list generated from parser need to be formatted into http://www.espn.com/search/results?q=lonzo%20ball
    #                                                     www.espn.com/search/results?q=carl%20anthony%20towns
    search = 'http://www.espn.com/search/results?q='
    for each in list:
        search += each + '%20'
    search = search[:-3]
    return search


def get_url(query):
    driver.get(query)
    src = driver.page_source
    pretty_src = BeautifulSoup(src, 'lxml')
    section_we_need = pretty_src.find_all(class_='gsc-table-result')

    # after we have the section, extract all urls inside
    urls = []
    for each in section_we_need:
        each = str(each)
        url = re.findall('href=\"(.*?)\"', each)
        for every in url:
            urls.append(every)

    # uniqify
    uni_urls = []
    for each in urls:
        if each not in uni_urls:
            uni_urls.append(each)

    # get story
    story = []
    for a in uni_urls:
        if a.find('story') != -1 and a.find('feature') == -1:
            story.append(a)
    return story


def get_header_article_per_url(url):
    driver.get(url)
    src = driver.page_source  # source html
    pretty_src = BeautifulSoup(src, 'lxml')
    b = pretty_src.find('header', class_='article-header')
    header = re.sub('<.*?>', '', str(b.h1))

    a = pretty_src.find('div', class_='article-body')  # all div with class="article-body"
    if len(a.find_all('p')) != 0:
        temp = a.find_all('p')
        temp = list(temp)
        temp = [str(i) for i in temp]
        content = "".join(temp)
        article = re.sub('<.*?>', '', content)
    return header, article


def retrieve_articles(url):
    header, article = get_header_article_per_url(url)
    article = article.split('\n')[0:2]
    article = "\n".join(article)
    return article


def get_articles(keyword_list):
    query = get_query(keyword_list)
    url = get_url(query)[0]
    article = retrieve_articles(url)
    print(type(article))
    return article 


def get_player_game_stats(player, date):
    # need the player's name, the game date. Since we're doing one sport, we don't need the sport name.
    # This provides the results.
    # get player's website
    players_website = pd.read_csv('playerDictionaries/players_website.csv')
    website = players_website[players_website['Player Name'] == player]['Player Website'].iloc[0]
    website = website[0:30] + '/gamelog' + website[30:]
    driver.get(website)
    src = driver.page_source  # source html
    pretty_src = BeautifulSoup(src, "lxml")

    # suppose the date is like 20180402, 8-digit number
    date = date[1:] if date[0] == '0' else date
    date0 = date[4:6]
    date0 = date0 if date0[0]!='0' else date0[1]
    date1 = date[6:]
    date1 = date1 if date1[0]!='0' else date1[1]
    date = date0+'/'+date1
    
    pretty_src = pretty_src.find('div', class_='mod-container mod-table mod-player-stats')
    games = pretty_src.findAll('tr', attrs={"class": re.compile(r".*team.*")})

    msg = ''
    for each in games:
        if each.td.string.find(date) == -1:
            # did not found the game!
            continue
        else:
            stats = {'MIN': None, 'FGM-FGA': None, 'FG%': None, '3PM-3PA': None, '3P%': None, 'FTM-FTA': None,
                     'FT%': None, 'REB': None, 'AST': None, 'BLK': None, 'STL': None, 'PF': None, 'TO': None,
                     'PTS': None, 'WIN': None, 'OPPO': None}
            tmp = each.findAll('td')
            stats['MIN'] = tmp[3].string
            stats['REB'] = tmp[10].string
            stats['AST'] = tmp[11].string
            stats['BLK'] = tmp[12].string
            stats['STL'] = tmp[13].string
            stats['PTS'] = tmp[-1].string
            stats['OPPO'] = tmp[1].find('li', class_='team-name').string
            stats['WIN'] = 'won' if tmp[2].span.string == 'W' else 'lost'
            msg = '{} played {} minutes, scored {} points, got {} rebounds and {} assists, {} the game against {}'.format(
                player, stats['MIN'], stats['PTS'], stats['REB'], stats['AST'], stats['WIN'], stats['OPPO'])
    if msg == '':
        msg = 'He didn\'t play on that day, try another one.'
    return msg


def get_player_season_stats(player, *args):
    # season is like 2017-2018
    season = '\'17-\'18' if len(args) == 0 else '\'' + args[0][2:4] + '-' + '\'' + args[0][-2:]
    players_website = pd.read_csv('playerDictionaries/players_website.csv')
    website = players_website[players_website['Player Name'] == player]['Player Website'].iloc[0]
    website = website[0:30] + '/stats' + website[30:]
    driver.get(website)
    src = driver.page_source  # source html
    pretty_src = BeautifulSoup(src, "lxml")

    average_table = pretty_src.find('div', class_='mod-container mod-table mod-player-stats').div.tbody

    cols = average_table.find('tr', class_='colhead')
    cols = cols.findAll('td')
    cols = [each.string for each in cols]
    stats = dict.fromkeys(cols, None)

    rows = average_table.findAll('tr', attrs={'class': re.compile(r'.*row.*')})
    msg = ''
    for each in rows:
        if each.td.string == season:
            data = each.findAll('td')
            stats['TEAM'] = data[1].find('li', class_='team-name').a.string
            stats['MIN'] = data[4].string
            stats['FG%'] = data[6].string
            stats['3P%'] = data[8].string
            stats['FT%'] = data[10].string
            stats['REB'] = data[13].string
            stats['AST'] = data[14].string
            stats['BLK'] = data[15].string
            stats['STL'] = data[16].string
            stats['PTS'] = data[-1].string
            msg = '{} in {} got an average of {} pts with {} field goal percentage and {} 3-pointer percentage, {} rebounds, {} assists, {} blocks, {} steals.'.format(
                player, stats['TEAM'], stats['PTS'], stats['FG%'], stats['3P%'], stats['REB'], stats['AST'],
                stats['BLK'], stats['STL'])

    if msg != '':
        return msg
    else:
        return 'Sorry I cannot find the stats you are asking.'


def get_team_game_result(team, date):
    date = date[6:] + '.' + date[4:6]
    page = 'https://www.scoreboard.com/en/nba/results/'
    driver.get(page)
    src = driver.page_source  # source html
    pretty_src = BeautifulSoup(src, "lxml")
    info = pretty_src.tbody
    games = info.find_all('tr')
    time = []
    home = []
    away = []
    score = []
    for each in games:
        if each.find('td', class_='cell_ad') != None:  # time
            time.append(each.find('td', class_='cell_ad').string)
        if each.find('td', class_='cell_ab') != None:  # home team
            home.append(each.find('td', class_='cell_ab').span.string)
        if each.find('td', class_='cell_ac') != None:  # away team
            away.append(each.find('td', class_='cell_ac').span.string)
        if each.find('td', class_='cell_sa') != None:  # score
            score.append(each.find('td', class_='cell_sa').string)

    msg = ''
    # we have team and date to put in!
    for i in range(len(home)):
        print(2, time[i], time[i].find(date) != -1)
        if (team == home[i] or team == away[i]) and time[i].find(date) != -1:
            homescore = int(score[i].split(':')[0])
            awayscore = int(score[i].split(':')[1])
            print(home[i], away[i])
            if team == home[i]:
                if homescore > awayscore:
                    msg = '{} won with a score of: {}:{}!'.format(team, homescore, awayscore)
                else:
                    msg = '{} lost with a score of: {}:{}!'.format(team, awayscore, homescore)
            else:
                if homescore > awayscore:
                    msg = '{} lost with a score of: {}:{}!'.format(team, awayscore, homescore)
                else:
                    msg = '{} won with a score of: {}:{}!'.format(team, homescore, awayscore)
            break
    if msg == '':
        return 'They didn\'t play on that day.'
    return msg


def get_team_season_stats(team, season):
    team_website = pd.read_excel('teamDictionaries/Basketball Dictionary.xlsx')
    website = team_website[team_website['Team Name'] == team]['ESPN url'].iloc[0]
    driver.get(website)
    src = driver.page_source  # source html
    pretty_src = BeautifulSoup(src, "lxml")

    team_stats_table = pretty_src.find('article', class_='sub-module rankings').div
    data = team_stats_table.findAll('div')

    PPG = data[0].findAll('span')[1].string
    PPGth = data[0].findAll('span')[2].text

    RPG = data[1].findAll('span')[1].string
    RPGth = data[1].findAll('span')[2].text

    APG = data[2].findAll('span')[1].string
    APGth = data[2].findAll('span')[2].text

    PA = data[3].findAll('span')[1].string
    PAth = data[3].findAll('span')[2].text

    msg = "{} season stats: {}-{}-{}, {}-{}-{}, {}-{}-{}, {}-{}-{}".format(team, 'Points Per Game', PPG, PPGth,
                                                                           'Rebounds Per Game', RPG, RPGth,
                                                                           'Assists Per Game', APG, APGth,
                                                                           'Points Allowed', PA, PAth)

    return msg


# given contextframe and number of type of question
def queryHere(question, ContextFrame):
    try:
        if (question == '1'):  # player general stats
            msg = get_player_season_stats(ContextFrame.player, '2017-2018')
        elif (question == '2'):  # player game stats
            msg = get_player_game_stats(ContextFrame.player, date_convert(ContextFrame.date))
        elif (question == '3'):  # player general performance
            msg = get_articles([ContextFrame.player, '2017-2018'])
        elif (question == '4'):  # player game performance
            msg = get_articles([ContextFrame.player, date_convert(ContextFrame.date)])
        elif (question == '5'):  # team general stats
            msg = get_team_season_stats(ContextFrame.team1, '2017-2018')
        elif (question == '6'):  # team game stats
            msg = get_team_game_result(ContextFrame.team1, date_convert(ContextFrame.date))
        elif (question == '7'):  # team general performance
            msg = get_articles([ContextFrame.team1, '2017-2018'])
        elif (question == '8'):  # team game performance
            msg = get_articles([ContextFrame.team1, date_convert(ContextFrame.date)])
    except:
        msg = 'Sorry I can\'t ask that question, try another one:) .'

    return msg


# abspath = os.path.abspath(r"C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe")
# driver = webdriver.Chrome(abspath)

# msg1 = get_player_game_stats('Marcus Morris', '20180523')

# headers, articles = get_articles(['lakers', 'trade'])

# # msg2 = get_team_game_result(team = 'Toronto Raptors', date = '20180505')

if __name__ == '__main__':
    abspath = os.path.abspath(r"C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe")
    driver = webdriver.Chrome(abspath)

    print(get_player_game_stats('Stephen Curry', date_convert('06-03-18')))