import math

def get_board(player1,player2):
	# Creates a replica of the current board status	
	board = [[],[],[]]
	pos = 1
	for i in range(3):
		for j in range(3):
			if pos in player1:
				board[i].append('X')
			elif pos in player2:
				board[i].append('O')
			else:
				board[i].append('_')
			pos = pos+1
	return board

def check(player):
	# Checks if the player wins the board or not
	winPoints = [[1,2,3], [1,4,7], [1,5,9], 
			[2,5,8], 
			[3,6,9], [3,5,7],
			[4,5,6],
			[7,8,9]]
	for i in winPoints:
		won = True
		for j in i:
			if j not in player:
				won = False
				break
		if won:
			return True
	return False
	

def isMoveLeft(board):
	# Checks if any more move is left 
	for i in range(3):
		if '_' in board[i]:
			return True
	return False


def evaluate(board):
	# Evaluates the board provided and returns score or checks for draw
	player1 = []
	player2 = []
	for i in range(3):
		for j in range(3):
			if board[i][j] == 'X':
				player1.append((i*3) + j + 1)
			elif board[i][j] == 'O':
				player2.append((i*3) + j + 1)
	if check(player1):							# If player1 wins then we return a positive score
		return 10
	elif check(player2):						# If player2 wins then we return a negative score
		return -10
	return 0									# Returns 0 if there is a tie
	

	
def findmoves(board,depth,isP1):		
	# Recursive function to determine score if a move is done
	# depth is the number of moves done, isP1 is boolean value that informs if turn is for Player1 or not
	score = evaluate(board)				# Gets the evaluated score 
	
	# If a score is returned we can say which player wins the board hence we return the score
	if score == 10:
		return score 					
	if score == -10:
		return score
		
	# If the board cannot determine winner i.e. it returns 0
	if not isMoveLeft(board):			# If no more moves are left then it returns 0
		return 0
	
	if isP1:					# If next turn is for player1
		best = -1000
		for i in range(3):
			for j in range(3):
				if board[i][j] == '_':			# We check for the highest score obtained by using all the remaining moves
					board[i][j] = 'X'
					best = max(best, findmoves(board, depth + 1,not isP1))
					board[i][j] = '_'
		return best								# Returns the highest score obtained in any move
	else:										# When next turn is of player2
		best = 1000
		for i in range(3):
			for j in range(3):			
				if board[i][j] == '_':			# Checks for the minimum score obtained by using all the moves left
					board[i][j] = 'O'
					best = min(best, findmoves(board, depth+1, not isP1))
					board[i][j] = '_'
		return best								# Returns the minimum score obtained from any move

		
		
def find_best_move(board):		
	# Determines the best move possible 
	# We will check for the minimum possible score as computer is the minimizer here
	bestVal = 1000
	pos = -1
	
	for i in range(3):
		for j in range(3):
			if board[i][j] == '_':		# Makes a move to all the remaining positions and checks for the score
				board[i][j] = 'O'
				moveVal = findmoves(board,0,True)
				board[i][j] = '_'
				if moveVal < bestVal:	# If a move fetches less score than the best move till now 
					pos = (i*3) + j + 1	# Updates the position
					bestVal = moveVal	# Updates the value of bestVal
	return pos		# Returns the best move

		
	
