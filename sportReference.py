import pandas as pd

class sportReference:
    teams = {}

    def __init__(self, sport, file, stats, rosters):
        dataframe = pd.ExcelFile(file)
        self.data = dataframe.parse(dataframe.sheet_names[0])
        self.sport = sport
        self.stats = stats
        self.rosters = rosters

    # check if a team named 'name' exists (could also be mascot name, ex: Red Sox)
    def teamExists(self, name):
        name = name.lower()
        for index, row in self.data.iterrows():
            if row['Team Name'].lower() == name:
                return row['Team Name']
            if row['Mascot'].lower() == name:
                return row['Team Name']
        return None

    def getLocationTeam(self, location):
        location = location.lower()
        for index, row in self.data.iterrows():
            if row['City'].lower() == location:
                return row['Team Name']
            if row['State'].lower() == location:
                return row['Team Name']

    # using a known piece of information about a team, get an unknown piece of information
    # about the same team
    # ex: getInfo("Mascot", "Mets", "City") will return New York i.e. the city of the New York Mets
    def getInfo(self, knownCol, knownVal, desiredCol):
        for index, row in self.data.iterrows():
            if row[knownCol].lower() == knownVal:
                return row[desiredCol].lower()

        return None

    # returns the name of the team with a player named 'player_name'
    def get_player_team(self, player_name):
        name = player_name.lower()
        for team, roster in self.rosters.items():
            for player in roster:
                if player.lower() == name:
                    return team

    # returns true if a player exists with the name 'player_name'
    # if you know the team the player should be on, input value as 'team' param to speed up search
    def playerExists(self, player_name, team = None):
        name = player_name.lower()
        if team != None:
            roster = self.rosters[team]
            for player in roster:
                if player.lower() == name:
                    return True
        else:
            for team, roster in self.rosters.items():
                for player in roster:
                    if player.lower() == name:
                        return True
        return False

    # check if 'location' is the city of a team
    def locationHasTeam(self, location):
        location = location.lower()
        for index, row in self.data.iterrows():
            if row['City'].lower() == location:
                return True
        return False





