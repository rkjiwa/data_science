import copy

from dlgo.octopawn.types import Player, Point

__all__ = [
	'Board',
	'GameState',
	'Move',
]


class IllegalMoveError(Exception):
	pass


BOARD_SIZE = 4
ROWS = tuple(range(1, BOARD_SIZE + 1))
COLS = tuple(range(1, BOARD_SIZE + 1))



class Board:
	def __init__(self):
		# initial board position
		self._grid = {
			Point(1,1):Player.x,
			Point(1,2):Player.x,
			Point(1,3):Player.x,
			Point(1,4):Player.x,
			Point(2,1):None,
			Point(2,2):None,
			Point(2,3):None,
			Point(2,4):None,
			Point(3,1):None,
			Point(3,2):None,
			Point(3,3):None,
			Point(3,4):None,
			Point(4,1):Player.o,
			Point(4,2):Player.o,
			Point(4,3):Player.o,
			Point(4,4):Player.o
			}

	def place(self, player, start_point, point):
		# to place the moves
		# remove the start point from the grid
		self._grid.pop(start_point)
		# set the start point to None
		self._grid[start_point] = None
		# set the move point to the player 
		self._grid[point] = player
		

	@staticmethod
	def is_on_grid(point):
		return 1 <= point.row <= BOARD_SIZE and \
			1 <= point.col <= BOARD_SIZE

	def get(self, point):
		"""Return the content of a point on the board.

		Returns None if the point is empty, or a Player if there is a
		stone on that point.
		"""
		return self._grid.get(point)


class Move:
	def __init__(self, point):
		self.point = point

	def __str__(self):
		return(str(self.__class__) + ": " + str(self.__dict__))


class GameState:
	def __init__(self, board, next_player, move):
		self.board = board
		self.next_player = next_player
		self.last_move = move

	def apply_move(self, start_move, move):
		"""Return the new GameState after applying the move."""
		# check that the start move and the move are Move objects
		if not isinstance(move, Move):
			move = Move(move)
		if not isinstance(start_move, Move):
			start_move = Move(start_move)
		# copy the board
		next_board = copy.deepcopy(self.board)
		# place the move on the next board
		next_board.place(self.next_player, start_move.point, move.point)
		return GameState(next_board, self.next_player.other, move)

	@classmethod
	def new_game(cls):
		board = Board()
		return GameState(board, Player.x, None)


	def is_valid_move(self, move):
		return (
			self.board.get(move.point) is None and
			not self.is_over())


	# define the legal moves
	def legal_moves_hex(self, player):
		# create a list of the moves
		moves = []
		# create a dictionary for the pairings
		legal_moves_dict = {}
		# create a list for the starting points
		starting_point = []
		# create a variable to refer to grid
		points = self.board._grid
		# check player.X
		if player == Player.x:
			# iterate through the items in the grid
			for key, value in points.items():
				# if point is player.x
				if value == Player.x:
					# check conditions for the forward move
					if (Point(key[0]+1,key[1]) in points.keys()) and (points[Point(key[0]+1,key[1])] == None):
						# add forward move point to moves 
						moves.append(Point(key[0]+1, key[1]))
						# add the move and the current piece point to the dictionary
						legal_moves_dict[key] = Point(key[0]+1, key[1])
						# add current piece point to starting point list
						starting_point.append(key)
					# check conditions for a right side attack
					if Point(key[0]+1,key[1]+1) in points.keys() and points[Point(key[0]+1,key[1]+1)] == Player.o:
						# add right side attack to moves
						moves.append(Point(key[0]+1,key[1]+1))
						# add starting poing and move point to dictionary
						legal_moves_dict[key] = Point(key[0]+1, key[1]+1)
						# add starting move to list
						starting_point.append(key)
					# check for left side attack
					if Point(key[0]+1,key[1]-1) in points.keys() and points[Point(key[0]+1,key[1]-1)] == Player.o:
						# add left side attack to moves
						moves.append(Point(key[0]+1,key[1]-1))
						# add move start and end point to dictionary
						legal_moves_dict[key] = Point(key[0]+1, key[1]-1)
						# add starting point to list
						starting_point.append(key)
		# same as player X, the differences lie in that the rows are - rather than +
		if player == Player.o:
			for key, value in points.items():
				if value == Player.o:
					if Point(key[0]-1,key[1]) in points.keys() and points[Point(key[0]-1,key[1])] == None:
						moves.append(Point(key[0]-1, key[1]))
						legal_moves_dict[key] = Point(key[0]-1,key[1])
						starting_point.append(key)
					if Point(key[0]-1,key[1]+1) in points.keys() and points[Point(key[0]-1,key[1]+1)] == Player.x:
						moves.append(Point(key[0]-1,key[1]+1))
						legal_moves_dict[key] = Point(key[0]-1,key[1]+1)
						starting_point.append(key)
					if Point(key[0]-1,key[1]-1) in points.keys() and points[Point(key[0]-1,key[1]-1)] == Player.x:
						moves.append(Point(key[0]-1,key[1]-1))
						legal_moves_dict[key] = Point(key[0]-1,key[1]-1)
						starting_point.append(key)
		# check if there are no viable moves
		if not moves:
			return None
		# return the list for moves, starting points and the map dictionary	
		return moves, starting_point, legal_moves_dict


	def is_over(self):
		# end conditions for player X
		if (self.hex_cross(Player.x) == True) or (self.legal_moves_hex(Player.x) == None):
			return True
		# end conditions for player O
		if (self.hex_cross(Player.o) == True) or (self.legal_moves_hex(Player.o) == None):
			return True
		return False


	# define the crossing, for X and O to reach otherside of the board
	# rather than hard coding this, you could modify it to refer to board size
	def hex_cross(self, player):
		if player == Player.x:
			if self.board.get(Point(4,1)) == Player.x or \
				self.board.get(Point(4,2)) == Player.x or \
				self.board.get(Point(4,3)) == Player.x or \
				self.board.get(Point(4,4)) == Player.x:
				return True
		if player == Player.o:
			if self.board.get(Point(1,1)) == Player.o or \
				self.board.get(Point(1,2)) == Player.o or \
				self.board.get(Point(1,3)) == Player.o or \
				self.board.get(Point(1,4)) == Player.o:
				return True
		return False

	# function to call the winner
	def winner(self):
		if self.hex_cross(Player.x):
			return Player.x
		if self.hex_cross(Player.o):
			return Player.o
		if self.legal_moves_hex(Player.x) == None:
			return Player.o
		if self.legal_moves_hex(Player.o) == None:
			return Player.x
		return None
