"This is the file we'll load to run our shitty UI and test our game."

#Import stuff

board = 'NONE'
game_settings = 'NONE'

def RunGame(UI):
	"This is the architecture of the whole game, including set up and everything"

	UI.Setup()
	UI.Welcome()
	UI.Game_intro()
	UI.Game_Play()
	#UI.Save_data()
	#UI.Goodbye()
