# Sports_News_Chatbot

Check out "driver.py" to see an example of everything working thus far. It will parse a question into teams, players, dates, locations, etc.

For each sport, there is an instance of the sportReference class. This can be used to check if a player exists, if a team exists, etc. All three of the sportReferences instances (one for baseball, one for basketball, one for football) are set up in "driver.py." If you need to search a roster or a sport dictionary using a function that I haven't already defined, do that in the sportReference class. If you do not know what sport a query may be referring to (for example, if the first question asked only contains a player name) you need to call the necessary functions on the sportReference instances of all available sports. 

The ParsingTools file contains functions to grab the relevant data from questions. It will identify dates, player names, team names, locations, etc. in query text. 

The context class contains classes for the ContextTracker and ContextFrames, but it is not filled in at all. 
