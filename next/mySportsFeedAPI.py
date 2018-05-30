import urllib2
import csv
import json
import requests
import base64
from datetime import datetime, timedelta
import time
import random

seasons = {}
seasons['NFL'] = "2017-regular"
seasons['MLB'] = "2017-regular"
seasons['NBA'] = "2017-2018-regular"
seasons['NHL'] = "2017-2018-regular"

potKeys = {}
potKeys['NFL'] = ['Rec. TD','Rush TD','Pass Yards','Pass Completions','Rush Yards','Rec. Yards','Receptions','Tackle Total','Sacks','Interceptions']
potKeys['NBA'] = ['Pts','Ft. Made','Off. Reb','Def. Reb','Ast.']
potKeys['NHL'] = ['Points','Shots','Blocked Shots','Faceoffs']
potKeys['MLB'] = ['Homeruns','Runs','Hits','Errors','Total Bases']

months = {}
months['01'] = 'January'
months['02'] = 'February'
months['03'] = 'March'
months['04'] = 'April'
months['05'] = 'May'
months['06'] = 'June'
months['07'] = 'July'
months['08'] = 'August'
months['09'] = 'September'
months['10'] = 'October'
months['11'] = 'November'
months['12'] = 'December'

def lookupGame(league, city, team, date):
    key1 = 'PointsFor'
    key2 = 'PointsAgainst'
    if league == 'NHL':
        key1 = 'Points'
        key2 = 'GoalsAgainst'
    elif league == 'NBA':
        key1 = 'Pts'
        key2 = 'PtsAgainst'
    elif league == 'MLB':
        while date.month > 10:
            date = date - timedelta(days=30)
        key1 = 'Runs'
        key2 = 'RunsAllowed'
    
    toret = ''
    j = {}
    j['teamgamelogs'] = {}

    link = makeGameLink(league,city,team,date)

    counter = 0
    td = timedelta(days=5)

    while toret == '' and counter < 5:
        try:
            while 'gamelogs' not in j['teamgamelogs'] and counter < 10:
                counter += 1
                request = urllib2.Request(link)
                base64string = base64.encodestring('%s:%s' % ('danielt22', '622115')).replace('\n', '')
                request.add_header("Authorization", "Basic %s" % base64string)   
                result = urllib2.urlopen(request)
            
                j = json.loads(result.read())

                print link
                date = date - td
                link = makeGameLink(league,city,team,date)
                
            for index in j['teamgamelogs']['gamelogs']:
                game = index['game']
                execute = False
                if game['date'] >= makeDate(date + td):
                    execute = True
                elif index == j['teamgamelogs']['gamelogs'][-1]:
                    execute = True
                if execute:
                    if game['awayTeam']['City'].lower() == city.lower():
                        team = 'awayTeam'
                        other = 'homeTeam'
                    else:
                        team = 'homeTeam'
                        other = 'awayTeam'
                        
                    pf = int(index['stats'][key1]['#text'])
                    pa = int(index['stats'][key2]['#text'])
                    
                    if pf > pa:
                        action = ' won against the '
                    elif pf == pa:
                        action = ' drew with the '
                    else:
                        action = ' lost to the '
                    endgame = game
                    toret = "The " + endgame[team]['City'] + " " + endgame[team]['Name'] + action + endgame[other]['City'] + ' ' + endgame[other]['Name'] + ' '+str(pf)+'-'+str(pa)+' on ' + prettifyDate(endgame['date']) + '.' 
        except Exception as err:
            print str(err), link
            date = date - timedelta(days=20)
    return date, toret

def lookupPlayer(league, city, team, date, player):
    lastname = player.split(' ')[-1].lower()
    
    if league == 'MLB':
        while date.month > 10:
            date = date - timedelta(days=30)
    
    toret = ''
    j = {}
    j['playergamelogs'] = {}

    link = makePlayerLink(league,city,team,date,lastname)

    counter = 0
    td = timedelta(days=7)
    
    while toret == '' and counter < 5:
        try:
            while 'gamelogs' not in j['playergamelogs'] and counter < 5 and toret == '':
                counter += 1
                request = urllib2.Request(link)
                base64string = base64.encodestring('%s:%s' % ('danielt22', '622115')).replace('\n', '')
                request.add_header("Authorization", "Basic %s" % base64string)   
                result = urllib2.urlopen(request)
            
                j = json.loads(result.read())

                print link
                date = date - td
                link = makePlayerLink(league,city,team,date,lastname)
                if 'gamelogs' in j['playergamelogs']:
                    for index in j['playergamelogs']['gamelogs']:
                        game = index['game']
                        execute = False
                        if game['date'] >= makeDate(date + td):
                            execute = True
                        elif index == j['playergamelogs']['gamelogs'][-1]:
                            execute = True
                        if execute:
                            keys = potKeys[league]
                            for key1 in keys:
                                key = key1.replace(' ','').replace('.','')
                                if key in index['stats'].keys():
                                    count = index['stats'][key]['#text']
                                    if float(count) > 0 and random.random() > .65:
                                        toret = player + " got " + str(count) + ' ' + key1 + ' on ' + prettifyDate(game['date']) + '.'
                                        return toret
                else:
                    date = date - timedelta(days=20)
        except Exception as err:
            print str(err), link
            date = date - timedelta(days=20)
    return "Sorry, I can't find that player..."
        

def prettifyDate(date):
    date = date.split('-')
    if date[2][1] == '1':
        date[2] += 'st'
    elif date[2][1] == '2':
        if date[2][0] == '1':
            date[2] += 'th'
        else:
            date[2] += 'nd'
    elif date[2][1] == '3':
        if date[2][0] == '1':
            date[2] += 'th'
        else:
            date[2] += 'rd'
    else:
        date[2] += 'th'
    if date[2][0] == '0':
        date[2] = date[2][1:]
    return months[date[1]] + ' ' + date[2]

def makeDate(date):
    year = str(date.year)
    month = str(date.month)
    day = str(date.day)
    if len(month) < 2:
        month = '0' + month
    if len(day) < 2:
        day = '0' + day
    return year + '-' + month + '-' + day

def makeGameLink(league,city,team,date):
    link1 = "https://api.mysportsfeeds.com/v1.1/pull/"
    link2 = "/team_gamelogs.json?"
    link = link1+league+'/'+seasons[league]+link2
    tst = "team=" + city.replace(' ','').lower() + '-' + team.replace(' ','').lower()
    tst = tst.replace(".","")
    link = link + "&" + tst
    ndate = makeDate(date).replace('-','')
    dst = "date=since-" + ndate
    link = link + '&' + dst
    return link

def makePlayerLink(league,city,team,date,player):
    link1 = "https://api.mysportsfeeds.com/v1.1/pull/"
    link2 = "/player_gamelogs.json?"
    link = link1+league+'/'+seasons[league]+link2
    tst = "team=" + city.replace(' ','').lower() + '-' + team.replace(' ','').lower()
    tst = tst.replace(".","")
    link = link + "&" + tst
    ndate = makeDate(date).replace('-','')
    dst = "date=since-" + ndate
    link = link + '&' + dst
    pst = "player=" + player
    link = link + '&' + pst
    return link
