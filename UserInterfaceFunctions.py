'''
So the goal of this Shitty User Interface is to allow us to do tests, not to have a working game with all the bells and whistles. To get that I need:

- [ ] A simple graphic rendering of the current board state
- [X] A way for the user to choose different options (select from a list of pieces, valid moves, tiles, etc...)
	- Well document the functions to make it clear to others how to use them. 
- [ ] Update the state based on the user input
- [ ] To be able to see information about individual objects without exiting the program
	- Maybe put a more info option each time I give a list of options. It just displays all the useful info from each option.
	- Also a way to access more info about specific tiles when looking at the board.
- [ ] We don't want to have to go back through all the old dialog to debug an error that 3 prompts in. We need a way to start from the middle
	- The current architecture of the building the UI as a class and then running it through a function kind of forces people to start from the beginning. But if I make the UI a collection of functions, then we can run each one starting with the appropriate data. 
	- We still have one larger function RunGame which puts all the smaller functions in order. It would defined all the 'global' variables like player_name, num_of_teams, etc... that the functions need access to if we're doing them in a row. 
- [ ] A simple 'move' and 'turn' counter
- [ ] A way to undo a move

'''

#import Piece 
from gamePiece import *
from board import *


"Data collection functions"

def _pick_option(options, keys = None, return_values = None):
		"options is a list of strings presented the the user to choose from."
		"keys is a list of strings or ints. They represent the key combination users need to enter to select the associated option."
		"return_values is the list of values that will be returned. This can be of any type."
		"All lists must be the same length."
		"If keys is not present, it will become a list of integers starting with 1"
		"If return_values is not present, it will be equivalent to keys"
		"If keys are strings, they must be entered into the  function in ALL CAPS. Otherwise the loop can never be ended!"

		#This part creates the keys and return_values if they don't already exist
		if (keys == None):
			keys = range(1,len(options)+1)

		if (return_values == None):
			return_values = keys

		#Tests to see if all the lists are the same length
		if (len(options) != len(keys)):
			#print('Error: keys not the same length as options')
			raise ValueError('List of keys is not the same length as list of options')
		if (len(options) != len(return_values)):
			print('The return_values list is not the same length as the list of options')
			raise ValueError

		#Ensures that the keys are strings. Users can only enter strings.
		keys = list(map(str,keys))

		#Prints the list of options with their keys for the user to hit
		for i in range(0,len(options)):
			print("[", keys[i], "]", options[i])

		#Collecting the answer
		choosing = True
		while (choosing == True):
			print("you select:")
			answer = input()
			answer = answer.upper()
			if (answer in keys):
				i = keys.index(answer)
				print('You selected ', options[i],)
				return return_values[i]
				choosing = False
			else:
				print('not a valid option')

def _get_input(forbidden = [], error_message = "Not a valid input, try again."):
	"forbidden is a list of strings that will not be accepted as valid."
	"This function returns a valid input in all caps."
	"Can be used to record the name of a player."

	choosing = True
	while (choosing == True):
		choice = input()
		choice = choice.upper()
		if (choice not in forbidden):
			choosing = False
		else:
			print(error_message)
	return choice

def _get_first(L):
	return L[0]

def _get_list_of_pieces(all_possible_moves):
	return list(map(_get_first,all_possible_moves))



def choose_piece(list_of_pieces):
	"Enter the list, return the position on the list of the chosen piece"

	return_values = list(range(0,len(list_of_pieces)))

	#generate the displays and keys
	options = []
	keys = []
	index = {}
	
	for p in list_of_pieces:

		#adds display name to options
		p.update_display_name()
		options.append(p.display_name)

		#adds key to keys
		key = p.type_key
		if(key in list(index)):
			index[key] += 1

			key = key + ' ' + str(index[key])
			keys.append(key)
		else:
			index[key] = 1
			keys.append(key)

	keys = list(map(str,keys))
	_pick_option(options, keys = keys, return_values = return_values)


L = [g,h,g,g]











'''



def _get_class(obj): 
	#Better safe than sorry?
	return obj.__class__

def _get_key(obj):
	#Returns the prefered key

	if issubclass(_get_class(obj), Piece):
		if (obj.pieceType != ''):
			return obj.pieceType

	elif issubclass(_get_class(obj), Tile):
		if (obj.terrainType != ''):
			return obj.terrainType

	else:
		return None

def _get_display_name(obj):
	#Returns the prefered name

	if (type(obj)==str):
		return obj 

	elif issubclass(_get_class(obj), Piece):
		if (obj.pieceType == ''):
			return 'Game Piece'
		elif (obj.pieceType in list(Piece._cheat_sheat)):
			return Piece._cheat_sheat[obj.pieceType]
		else:
			raise Exception("'" + str(obj.pieceType) + "'" + " is not a real piece type.")

	elif issubclass(_get_class(obj), Tile):
		if (obj.terrainType != ''):
			return obj.terrainType

	else:
		return None

def _get_more_info(obj):
	#Should be built for more stuff

	return repr(obj)

def _get_all_info(obj):
	#Should be built for more stuff

	return str(obj.__dict__)

def _get_display_name_list(list_of_objs):
	#Enter in a list of objects, get back a list of their display names

	index = {}
	list_of_display_names = []

	for obj in list_of_objs:
		class_ = _get_class(obj) 
		if (class_ not in list(index)):
			index[class_] = 1
			list_of_display_names.append(str(_get_display_name(obj)))
		else:
			index[class_] += 1
			list_of_display_names.append(str(_get_display_name(obj)) + ' ' + str(index[class_]))

	return list_of_display_names


def _get_piece_display_name(piece):
	"enter a game piece and returns a name to display"





"Tailoring the functions for us"




def _make_choice(list_of_objs):
	"I will be given a list of game pieces, or a list of tiles or vectors. The player has to make a choice between them."
	pass




'''
