import sys
import random
import re
import nltk
from baseball_rosters import baseball_roster


bot_template = "BOT : {0}"
user_template = "USER : {0}"
query_winner = "Cardinals"
roster_team = " "
user_input = raw_input("Ask The Bot A Question: ")
message = user_input.lower()
query_team = message.split()[3]
query_roster = "blabla"
roster_team = message.split()[3] +" "+ message.split()[4] +" "+ message.split()[5]

#query_roster = baseball_roster[roster_team]
#pattern = "give me the roster for (.*)"
#match = re.search(pattern, message)
#roster_team2 = match.group(1)
#print roster_team2


responses = {
	"who won the cubs game yesterday?" : "Yesterday, the {0} won the game".format(query_winner),
	"give me the boston red sox roster?" : "The roster for {0} is: {1}".format(roster_team, query_roster),
	"give me the toronto blue jays roster?" : "The roster for {0} is: {1}".format(roster_team, query_roster),
	"give me the chicago white sox roster?" : "The roster for {0} is: {1}".format(roster_team, query_roster),
}

def respond(message):
	if roster_team in baseball_roster:
		query_roster = baseball_roster[roster_team]
		return "The roster is: " + query_roster
	if message in responses:
		return responses[message].format(query_winner)
	else:
		return "Sorry, can you rephrase the question?"

def make_question(message):
	if not message.endswith("?"):
		message = message + "?"



def send_message(message):
    # Print user_template including the user_message
    print(user_template.format(message))
    # Get the bot's response to the message
    response = respond(message)
    # Print the bot template including the bot's response.
    print(bot_template.format(response))

# Send a message to the bot


def swap_pronouns(message):
	if "I" in message: 
		return re.sub('I', 'you', message)
	if "my" in message: 
		return re.sub('my', 'your', message)
	else:
		return message

message = make_question(message)
print respond(message)
#message = raw_input('Ask another question:')
#make_question(message)
#print respond(message)

#pattern1 = "do you remember .*"
#message1 = "do you remember when you ate berries?"
#phrase = pattern.search(pattern, message).group(1)

#pattern2 = "if (.*)"
#message2 = "what would happen if bots took over the world?"
#match = re.search(pattern, message)

#def respond(message):
	#if not baseball_roster[roster_team]:
	#	print reportUpdate(message)
	#else:
	#	query_roster = baseball_roster[roster_team]
	#	return "The roster is: " + query_roster
