"This is the new User Interface Class. It's so advanced that it needs it's own file."
"The idea is to have the UI have a bunch of predefined funcitons. So to create a new UI, you just instantiate the class and only edit the functions that need changing"

"These are useful functions when defining this class"

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

		self.welcome_message = "Welcome to " + self._game_name "\n" +"You're using the " + self.name + " Version:" + str(self.version)
		self.outro = "Let's get started!"

	"As a convention, variables and methods that start with a single underscore, like _get_Input should not be changed when creating a new instance of the class."

	def _get_Input(self, forbidden = [], message = "Not a valid input, try again."):
		"Returns a valid input in all caps. Used to record the name of a player."
		choosing = True
		while (choosing == True):
			choice = input()
			choice = choice.upper()
			if (choice not in forbidden):
				choosing = False
			else:
				print(message)
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

	def _select_Player(self):
		"For now, it just grabs the name of the player. But once we get a player class it will instantiate the Player. In the future it could select from a list of players."

		print('Enter your name:')
		player_name = self._get_Input(forbidden = ['', 'NEW PLAYER', 'OPTIONS'])
			#self.player = Human_Player(player_name)
			self.player_name = player_name

	def _select_Board(self, list_of_boards):
		"This should display a list of board configurations along with a brief description of each. The user then can select one. The appropriate board will then be imported from a file which contains a list of all our premade board configurations. That board will then be saved to a global variable 'board' which is defined in RunGame.py"

		board_name = self._pick_Option(list_of_boards)
		from Board_Configurations import board_name as temp_board
		global board
		board = temp_board

	def _select_Game_Settings(self, list_of_game_settings):
		"This should display a list of game settings along with a brief description of each. The user then can select one. If the settings need to probably be imported from a file somewhere. If needed the settings will be saved to a global variable 'game_settings' which is defined in RunGame.py"

		settings_name = self._pick_Option(list_of_game_settings)
		from Different_game_settings import settings_name as temp_settings
		global game_settings
		game_settings = temp_settings

	"Now we write the parts of the code that get changed a lot"

	def setup(self):
		"If there is any setup that needs to be done before the welcome, it goes here. Probably we import/load the list_of_boards and list_of_game_settings."
		#self.load_lists()

	def welcome(self):
		"Plays the welcome message. Gives the selections of players, board layouts, and AI. Gives the options menu."

		#welcome's the player
		print(self.welcome_message)
		
		#Enter player's name
		self._selectPlayer()

		#Confirms name
		print("Hello " + self.player_name)

		#Pick the board layout
		print("Select your game board")
		self._select_Board(list_of_boards) #where does this list come from?

		#Copy any information the UI needs from the board

		#Select Game Settings
		print("Select your game settings")
		self._select_Game_Settings(list_of_game_settings)
		
		#Copy any information the UI needs form the game_settings
		self.num_of_moves = game_settings.num_of_moves

		#You exit the menu screen and display the outro. Now the game is ready to start
		print(self.outro)

	def game_Setup(self, board, game_settings):
		"The board will be an instance of the GameBoard class. It will be used to print out the board. The game_settings variable will tell us how many pieces we're using, of what type, and whether we're putting them down or using a predefined starting location."

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





