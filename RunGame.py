"This is the file we'll load to run our shitty UI and test our game."

import UserInterfaceClass

UI = UserInterfaceClass.Interface()

#board = 'NONE'
#game_settings = 'NONE'

list_of_boards = ['board one', 'bad board', 'water boarding']
list_of_game_settings = ['level one', 666, 'battle royal']

def RunGame(UI):
	"This is the architecture of the whole game, including set up and everything"

	UI.setup(list_of_boards, list_of_game_settings)
	UI.welcome()
	#UI.Game_intro()
	#UI.Game_Play()
	#UI.Save_data()
	#UI.Goodbye()

