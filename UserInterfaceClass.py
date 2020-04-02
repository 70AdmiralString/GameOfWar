"This is the new User Interface Class. It's so advanced that it needs it's own file."
"The idea is to have the UI have a bunch of predefined functions. So to create a new UI, you just instantiate the class and only edit the functions that need changing"


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



#These are useful functions when defining this class
new_input = input
def return_number(s):
	try:
		int(s)
		return int(s)
	except ValueError:
		return str(s) 




class Interface: 
	"Objects of this class will be the different skins and versions on the UI."

	def __init__(self):
		self._game_name = "Game of War"

		self.name = "Basic Shitty UI"
		self.version = 0.1

		#temp = "Welcome to " + self._game_name "\n" +"You're using the " + self.name + " Version:" + str(self.version)
		temp = "Welcome to " + self._game_name + "\n" +"You're using the " + self.name + " Version: " + str(self.version)

		self.outro = "Let's get started!"
		self.welcome_message = temp


	"As a convention, variables and methods that start with a single underscore, like _get_Input should not be changed when creating a new instance of the class."

	def _get_Input(self, forbidden = [], error_message = "Not a valid input, try again."):
		"Returns a valid input in all caps. Used to record the name of a player."
		choosing = True
		while (choosing == True):
			choice = input()
			choice = choice.upper()
			if (choice not in forbidden):
				choosing = False
			else:
				print(error_message)
		return choice

	def _pick_Option(self, options, keys = None, return_values = None):
		"Options are a list of things to choose from. Keys are the list of keys the player must press. Reuturn_values is a list of things the function will return"
		"If keys are strings, they must be entered into the _pickOption function in all caps. Otherwise the loop can never be ended!"

		"This part creates the keys and return_values if they don't already exist"
		if (keys == None):
			keys = range(0,len(options))

		if (return_values == None):
			return_values = keys

		"This part ensures that the keys are strings and the return_values are ints if they are supposed to be"
		keys = list(map(str,keys))
		return_values = list(map(return_number, return_values))

		"This part prints the list of options with their keys for the user to hit"
		for i in range(0,len(options)):
			print("[", keys[i], "]", options[i])

		"This part actually collects the answer"
		choosing = True
		while (choosing == True):
			print("you select:")
			answer = new_input()
			answer = answer.upper()
			if (answer in keys):
				i = keys.index(answer)
				print('You selected ', options[i],)
				return return_values[i]
				choosing = False
			else:
				print('not a valid option')

	def _select_player(self):
		"For now, it just grabs the name of the player. But once we get a player class it will instantiate the Player. In the future it could select from a list of players."

		print('Enter your name:')
		player_name = self._get_Input(forbidden = ['', 'NEW PLAYER', 'OPTIONS'])
		#self.player = Human_Player(player_name)
		self.player_name = player_name

	def _select_Board(self):
		"This should display a list of board configurations along with a brief description of each. The user then can select one. The appropriate board will then be imported from a file which contains a list of all our premade board configurations. That board will then be saved to a global variable 'board' which is defined in RunGame.py"

		board_name = self._pick_Option(self.list_of_boards)

		'''
		from Board_Configurations import board_name as temp_board
		global board
		board = temp_board
		'''

	def _select_Game_Settings(self):
		"This should display a list of game settings along with a brief description of each. The user then can select one. If the settings need to probably be imported from a file somewhere. If needed the settings will be saved to a global variable 'game_settings' which is defined in RunGame.py"

		settings_names = [o.name for o in self.list_of_game_settings]

		self.game_settings = self.list_of_game_settings[self._pick_Option(settings_names)]

		'''
		from Different_game_settings import settings_name as temp_settings
		global game_settings
		game_settings = temp_settings
		'''

	"Now we write the parts of the code that get changed a lot"

	def setup(self, list_of_boards, list_of_game_settings):
		"If there is any setup that needs to be done before the welcome, it goes here. Probably we import/load the list_of_boards and list_of_game_settings."

		self.list_of_boards = list_of_boards
		self.list_of_game_settings = list_of_game_settings

		#self.load_lists()

	def welcome(self):
		"Plays the welcome message. Gives the selections of players, board layouts, and AI. Gives the options menu."

		#welcomes the player
		print(self.welcome_message)
		
		#Enter player's name
		self._select_player()

		#Confirms name
		print("Hello " + self.player_name)

		#Pick the board layout
		print("Select your game board")
		self._select_Board() 


		#Copy any information the UI needs from the board

		#Select Game Settings
		print("Select your game settings")
		self._select_Game_Settings()
		print(self.game_settings.description)

		#Copy any information the UI needs form the game_settings
		#self.num_of_moves = game_settings.num_of_moves

		#You exit the menu screen and display the outro. Now the game is ready to start
		print(self.outro)

	def game_Setup(self, board, game_settings):
		"The board will be an instance of the GameBoard class. It will be used to print out the board. The game_settings variable will tell us how many pieces we're using, of what type, and whether we're putting them down or using a predefined starting location."
		pass

		#print board
		#place pieces

	def Game_play(self):
		"The way the game works or ends. Usually this is simple, but there might be some intermittent text"
		self.player1_turn = True
		self.playing = True
		while (self.playing == True):
			self.turn()
	
	def turn(self):
		"Each player's turn is here"
		i = 1
		while (i <= self.num_of_moves):
			self.move() 
			i = i + 1
		self.player1_turn = not self.player1_turn

	def move(self):
		"Now we're getting into some real complicated stuff. I'm not even sure if this should be a method of the Interface class or of the Player class."





