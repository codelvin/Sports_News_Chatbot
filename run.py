import sportReference as sr
import Queue
import nltk
import csv
import parsingTools as pt 
import copy
from context import ContextFrame
from context import ContextTracker


ourContextTracker = ContextTracker(basketballRef)

#examples = ['How did Anthony Brown play?']
examples = ['Lonzo Ball played on Wednesday night against the Celtics.',
			'How many points did Anthony Brown score on 3-28-18?',
			'How many minutes did Ian Clark play against the Kings?',
			'Did Los Angeles play the Bulls on Monday?',
			'Did the Warriors play the Nets on Friday?']

for example in examples:
	print(example)
	tokens = nltk.word_tokenize(example)
	tagged = nltk.pos_tag(tokens)
	ourContextTracker.new_frame()

