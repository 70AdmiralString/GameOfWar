"This is the file we'll load to run our shitty UI and test our game."

import UserInterfaceClass
UI = UserInterfaceClass.Interface()

import GameSettingsClass
simple = GameSettingsClass.simple
accurate = GameSettingsClass.accurate
list_of_game_settings = [simple, accurate]

list_of_boards = ['board one', 'bad board', 'water boarding']


def RunGame(UI):
	"This is the architecture of the whole game, including set up and everything"

	UI.setup(list_of_boards, list_of_game_settings)
	UI.welcome()
	#UI.Game_intro()
	#UI.Game_Play()
	#UI.Save_data()
	#UI.Goodbye()

