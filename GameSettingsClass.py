import gamePiece
from gamePiece import *

class GameSettings:
	"The objects of this class are just boxes that contain the list of rules/settings for the game. This includes number of players, number of pieces of each type, and number of moves per turn."
	"It will also have the gerate_pieces function which will create all the peices."
	"Lastly, it should have contain some sort of info on the board, and also a way to generate it."

	def __init__(self, name):


		self.name = name 
			# A short name used to quickly refer to this game setting
		self.description = '[description goes here]' 
			# A description of the game setting

		self.num_of_teams = 1
		self.num_moves_per_turn = 1
		self.pieces = {'I':0, 'H':0, 'A':0, 'A_H':0, 'C':0, 'C_H':0}

	def generate_pieces(self):
		"This function generates all the movable pieces that will be in play."

		L = []
			#This is the list of all pieces to be placed on the board. We will probably want a different data structure for this in the future.

		for team_num in range(0,self.num_of_teams):
			for piece_type in list(self.pieces):
				for piece_num in range(0,self.pieces[piece_type]):
					
					temp_piece = eval(GamePiece._cheat_sheat[piece_type])(0,0)
					temp_piece.team = team_num
					L.append(temp_piece)

		return L 
		#This prints something out which is long and messy. Maybe I need to change __repr__ again.




simple = GameSettings('simple')
simple.description = 'This is a very simple game setting where there is just 1 player and 1 game piece.'
simple.pieces['I'] = 1

accurate = GameSettings('accurate')
accurate.description = 'This is the actual game settings for the real Game of War.'
accurate.num_of_teams = 2
accurate.pieces = {'I':7, 'H':4, 'A':1, 'A_H':1, 'C':1, 'C_H':1}
accurate.num_moves_per_turn = 5

