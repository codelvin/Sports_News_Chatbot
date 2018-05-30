import json
from watson_developer_cloud import ConversationV1
from ay_news_api import *
import pickle
from flask import Flask,render_template,request
from mySportsFeedAPI import *
app = Flask(__name__)

with open('credentials.json') as js:
    credentials = json.load(js)
    
conversation = ConversationV1(username=str(credentials['username']), password=str(credentials['password']), version='2017-04-21')

workspace_id = '73a74624-91c6-447c-86df-b0a8a3eb6724'

class Team:
    def __init__(self, city, nfl, mlb, nba, nhl):
        self.leagues = {}
        self.leagues['NFL'] = nfl
        self.leagues['MLB'] = mlb
        self.leagues['NBA'] = nba
        self.leagues['NHL'] = nhl

teams = {}
teams['Boston'] = Team("Boston", [], ["Red Sox"], ["Celtics"], ["Bruins"])
teams['New England'] = Team("New England", ["Patriots"], [],[],[])
teams['Chicago'] = Team("Chicago", ["Bears"], ["White Sox", "Cubs"], ["Bulls"], ["Blackhawks"])
teams['Los Angeles'] = Team("Los Angeles", ["Rams", "Chargers"], ["Dodgers", "Angels"], ["Lakers"], ["Kings"])
teams['Detroit'] = Team("Detroit", ["Lions"], ["Tigers"], ["Pistons"],["Redwings"])
teams['Pittsburgh'] = Team("Pittsburgh", ["Steelers"], ["Pirates"], [], ["Penguins"])
teams['Atlanta'] = Team("Atlanta", ["Falcons"], ["Braves"], ["Hawks"], [])
teams['Miami'] = Team("Miami", ["Dolphins"], ["Marlins"], ["Heat"], [])
teams['Houston'] = Team("Houston", ["Texans"], ["Astros"], ["Rockets"], [])
teams['Carolina'] = Team("Carolina", ["Panthers"], [], [], ["Hurricanes"])
teams['Charlotte'] = Team("Charlotte", [], [], ["Hornets"], [])
teams['Nashville'] = Team("Nasvhille", [], [], [], ["Predators"])
teams['Tennessee'] = Team("Tennessee", ["Titans"], [], [], [])
teams['Cincinnati'] = Team("Cincinnati", ["Bengals"], ["Reds"], [], [])
teams['Columbus'] = Team("Columbus", [], [], [], ["Blue Jackets"])
teams['Washington'] = Team("Washington", ["Redskins"], ["Nationals"], ["Wizards"], ["Capitals"])
teams['New Jersey'] = Team("New Jersey", [],[],[],["Devils"])
teams['New York'] = Team("New York", ["Jets", "Giants"], ["Yankees", "Mets"], ["Knicks"], ["Islanders", "Rangers"])
teams['Brooklyn'] = Team("Brooklyn", [], [], [], ["Nets"])
teams['Anaheim'] = Team("Anaheim", [], [], [], ["Ducks"])
teams['Dallas'] = Team("Dallas", ["Cowboys"], [], ["Mavericks"], ["Stars"])
teams['Texas'] = Team("Texas", [], ["Rangers"], [], [])
teams['Denver'] = Team("Denver", ["Broncos"], [], ["Nuggets"], [])
teams['Colorado'] = Team("Colorado", [], ["Rockies"], [], ["Avalanche"])
teams['Minnesota'] = Team("Minnesota", ["Vikings"], ["Twins"], ["Timberwolves"], ["Wild"])
teams['Phoenix']= Team("Phoenix", [], [], ["Suns"], [])
teams['Arizona'] = Team("Arizona", ["Cardinals"], ["Diamondbacks"], [], ["Coyotes"])
teams['San Francisco']= Team("San Francisco", ["49ers"], ["Giants"], [], [])
teams['Golden State']= Team("Golden State", [], [], ["Warriors"], [])
teams['San Jose']= Team("San Jose", [], [], [], ["Sharks"])
teams['Oakland']= Team("Oakland", ["Raiders"], ["Athletics"], [], [])
teams['Washington'] = Team("Washington", ["Redskins"], ["Nationals"], ["Wizards"], ["Capitals"])
teams['Green Bay'] = Team("Green Bay", ["Packers"], [], [], [])
teams['Kansas City'] = Team("Kansas City", ["Chiefs"], ["Royals"], [], [])
teams['Milwaukee'] = Team("Milwaukee", [], ["Brewers"], ["Bucks"], [])
teams['New Orleans'] = Team("New Orleans", ["Saints"], [], ["Pelicans"], [])
teams['Oklahoma City'] = Team("Oklahoma City", [], [], ["Thunder"], [])
teams['Portland'] = Team("Portland", [], [], ["Blazers"], [])
teams['Sacramento'] = Team("Sacramento", [], [], ["Kings"], [])
teams['San Antonio'] = Team("San Antonio", [], [], ["Spurs"], [])
teams['Seattle'] = Team("Seattle", ["Seahawks"], ["Mariners"], [], [])
teams['San Diego'] = Team("San Diego", [], ["Padres"], [], [])
teams['St. Louis'] = Team("St. Louis", [], ["Cardinals"], [], [])
teams['Utah'] = Team("Utah", [], [], ["Jazz"], [])
teams['Vegas'] = Team("Vegas", [], [], [], ["Golden Knights"])
teams['Baltimore'] = Team("Baltimore", ["Ravens"], ["Orioles"], [], [])
teams['Buffalo'] = Team("Buffalo", ["Bills"], [], [], ["Sabres"])
teams['Cleveland'] = Team("Cleveland", ["Browns"], ["Indians"], ["Cavaliers"], [])
teams['Florida'] = Team("Florida", [], [], [], ["Panthers"])
teams['Indiana'] = Team("Indiana", [], [], ["Pacers"], [])
teams['Jacksonville'] = Team("Jacksonville", ["Jaguars"], [], [], [])
teams['Memphis'] = Team("Memphis", [], [], ["Grizzlies"], [])
teams['Orlando'] = Team("Orlando", [], [], ["Magic"], [])
teams['Philadelphia'] = Team("Philadelphia", ["Eagles"], ["Phillies"], ["76ers"], ["Flyers"])
teams['Tampa Bay'] = Team("Tampa Bay", ["Buccaneers"], ["Rays"], [], ["Lightning"])
teams['Ottawa'] = Team("Ottawa", [], [], [], ["Senators"])
teams['Montreal'] = Team("Montreal", [], [], [], ["Canadiens"])
teams['Calgary'] = Team("Calgary", [], [], [], ["Flames"])
teams['Edmonton'] = Team("Edmonton", [], [], [], ["Oilers"])
teams['Toronto'] = Team("Toronto", [], ["Blue Jays"], ["Raptors"], ["Maple Leafs"])
teams['Vancouver'] = Team("Vancouver", [], [], [], ["Canucks"])
teams['Winnipeg'] = Team("Winnipeg", [], [], [], ["Jets"])      

@app.route('/')
def input_display():
    story = {"body" : ''}
    response = ''
    team = ''
    city = ''
    league = ''
    input_text = request.args.get('input')
    days = ''
    entities = []
    date = ''
    playerstat = ''

    if input_text == None or input_text == '':
        pick(date,days,story,response,team,city,league,entities,playerstat)
        return render_template('sports_bot.html', name="I'm the Sports Bot. How can I help?")
    else:
        output = conv_att(input_text)
        return render_template('sports_bot.html', name=output)

def conv_att(input_text):
    story = {"body" : ''}
    response = ''
    team = ''
    city = ''
    league = ''
    days = ''
    entities = []
    playerstat = ''
    date = ''
    try:
        story = pickle.load(open('story.p','rb'))
        response = pickle.load(open('res.p','rb'))
        team = pickle.load(open('team.p','rb'))
        city = pickle.load(open('city.p','rb'))
        league = pickle.load(open('league.p','rb'))
        days = pickle.load(open('days.p','rb'))
        entities = pickle.load(open('entities.p','rb'))
        date = pickle.load(open('date.p','rb'))
        playerstat = pickle.load(open('playerstat.p','rb'))
    except:
        pass
    if "subject" in input_text.lower():
        try:
            return subject
        except:
            return "Subject Unavailable."
    elif "more" in input_text.lower():
        try:
            return story.body
        except:
            return "Story Unavailable."
    elif "source" in input_text.lower():
        try:
            return story.source.name
        except:
            return "Source Unavailable."
    elif "author" in input_text.lower():
        try:
            return story.author.name
        except:
            return "Author Unavailable."
    elif "description" in input_text.lower():
        try:
            if response != '':
                return response
            else:
                return "Description Unavailable."
        except:
            return "Description Unavailable."
    elif 'how did ' in input_text.lower() and 'play' in input_text.lower():
        start = input_text.lower().find('did ') + 4
        end = input_text.lower().find('play')
        player = capitalize(clean_st(input_text[start:end]))
        playerstat = lookupPlayer(league, city, team, date, player)
        pick(date,days,story,response,team,city,league,entities,playerstat)
        return playerstat
    elif 'what about' in input_text.lower():
        if capitalize(clean_st(input_text.lower().replace('what about',''))).replace('?','') in teams.keys():
            city = input_text.lower().replace('what about','').replace('?','')
            city = clean_st(city)
            city = city.replace('?','').replace('!','').replace('.','').replace(',','')
            city = capitalize(city)
            team = lookup_city(league, city)
            entities = [city,league]
            if len(team) == 0:
                team = ''
                response = "There is no " + league + " team in " + city + '!'
            else:
                if len(team) == 1:
                    team = team[0]
                else:
                    team = team[0]
                entities.append(team)
                lookup_str = city + ' ' + team
                low = int(days.split(',')[0])
                high = int(days.split(',')[1])
                returned = None
                while returned == None:
                    days = ','.join([str(low),str(high)])
                    returned = ay_lookup(lookup_str, entities=entities, timeframe=days)
                    high += 1
                story = returned[0]
                date = story.published_at
                pickle.dump(date,open('date.p','wb'),protocol=pickle.HIGHEST_PROTOCOL)
                response = returned[1]
                date, extraresponse = lookupGame(league,city,team,date)
                response = response + '  ' + extraresponse
                pick(date,days,story,response,team,city,league,entities,playerstat)
                return response
        return "There is no " + league + " team in " + capitalize(input_text.lower().replace('what about','')).replace('?','') + '!'
    else:
        watson_response = conversation.message(workspace_id=workspace_id, message_input={'text': input_text})
        entities = []
        lookup_str = ''
        for i in range(0,len(watson_response['entities'])):
            pkeyword = watson_response['entities'][i]['value']
            entity = watson_response['entities'][i]['entity'].replace('-',' ')
            if len(pkeyword) >= len(lookup_str):
                lookup_str = pkeyword.replace('-',' ')
                league = entity.split('_')[1]
                team = pkeyword.split('-')[1]
                city = pkeyword.split('-')[0]
            if entity.split('_')[1] not in entities:
                entities.append(entity.split('_')[1])
                
        if len(watson_response['entities']) == 0:
            if 'red sox' in input_text.lower():
                league = 'MLB'
                city = 'Boston'
                team = 'Red Sox'
                entities = [league, team, city]
            elif 'white sox' in input_text.lower():
                league = 'MLB'
                city = 'Chicago'
                team = 'White Sox'
                entities = [league, team, city]
                
        if lookup_str == '':
            lookup_str = input_text
        low = 0
        high = 2
        if 'last week' in input_text.lower():
            low = 6
            high = 13
        if 'last month' in input_text.lower():
            low = 20
            high = 50
        if 'last year' in input_text.lower():
            low = 250
            high = 500
        if 'last night' in input_text.lower():
            low = 0
            high = 1
        returned = None
        while returned == None:
            days = ','.join([str(low),str(high)])
            returned = ay_lookup(lookup_str, entities=entities, timeframe=days, league=league)
            high += 1
        story = returned[0]
        date = story.published_at
        response = returned[1]
        date, extraresponse = lookupGame(league,city,team,date)
        response = response + '  ' + extraresponse
        pick(date,days,story,response,team,city,league,entities,playerstat)
        return response

class info:
    def __init__(this):
        this.last_response = ''
        this.stor = ''

def capitalize(st):
    pieces = st.split(' ')
    try:
        toret = pieces[0][0].upper() + pieces[0][1:]
    except:
        toret = pieces[0]
    for piece in pieces[1:]:
        try:
            toret += ' ' + piece[0].upper() + piece[1:]
        except:
            pass
    return toret

def lookup_city(league,city):
    try:
        return teams[city].leagues[league]
    except:
        return ''

def pick(date,days,story,response,team,city,league,entities,playerstat):
    pickle.dump(date,open('date.p','wb'),protocol=pickle.HIGHEST_PROTOCOL)
    pickle.dump(days,open('days.p','wb'),protocol=pickle.HIGHEST_PROTOCOL)
    pickle.dump(story,open('story.p','wb'),protocol=pickle.HIGHEST_PROTOCOL)
    pickle.dump(response,open('res.p','wb'),protocol=pickle.HIGHEST_PROTOCOL)
    pickle.dump(team,open('team.p','wb'),protocol=pickle.HIGHEST_PROTOCOL)
    pickle.dump(city,open('city.p','wb'),protocol=pickle.HIGHEST_PROTOCOL)
    pickle.dump(league,open('league.p','wb'),protocol=pickle.HIGHEST_PROTOCOL)
    pickle.dump(entities,open('entities.p','wb'),protocol=pickle.HIGHEST_PROTOCOL)
    pickle.dump(playerstat,open('playerstat.p','wb'),protocol=pickle.HIGHEST_PROTOCOL)
        
app.run()
