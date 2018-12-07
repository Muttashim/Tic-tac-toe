from tkinter import *
from tkinter import messagebox
import sys,os,random
from PIL import Image
from PIL import ImageTk
from AIplayer import *


def restart():
	# Function to restart the program
	python = sys.executable				# Gets the executable process
	os.execl(python, python, *sys.argv)	# Exchanges the process image with this program 


def displayresult(result):
	# Function to display the result of the game
	messagebox.showinfo('Result', result)						
	res = messagebox.askyesno('Play Again', 'Do You Want To Play Again?')
	if res:
		restart()
	else:
		sys.exit()


def buttonPressed(btn, point):
	# Button press event handler function
	global remainingButtons,player,turn,width,height,singlePlayer
	result = ''
	if turn == 'circle':
		global circle,player2
		player2.append(point)		# Appends the position of player2's move
		image = circle				# Uses circle image on that position
		if check(player2):			# Checks if player2 wins or not
			result = 'Player 2 wins!'
			if singlePlayer:
				result = 'You Lost!\nBetter Luck Next Time.'
		turn = 'cross'				# Changes turn to cross
		player.set('Player 1')		# Sets the turn to player1 
	else:
		global cross,player1
		player1.append(point)
		image = cross
		if check(player1):
			result = 'Player 1 wins!'
			if singlePlayer:
				result = 'Congratulations!\nYou won.'
		turn = 'circle'
		player.set('Player 2')
	
	btn.config(image = image, width = width, height = height)	# Changes the configuration of the button
	btn['command'] = 0											# Makes the button disabled
	remainingButtons.remove(btn)
	if result != '':
		displayresult(result)
	checkDraw()
	if singlePlayer and turn == 'circle':
		autoplay()												# Calls autoplay method if in singleplayer mode

		
def getButton():
	# Gets the best move by the AIplayer
	global remainingButtons,player1,player2,buttonList
	
	for i in remainingButtons:			# Checks if AIplayer can win in the next move
		machine = player2.copy()
		point = buttonList.index(i) + 1
		machine.append(point)
		if check(machine):
			return i
	
	for i in remainingButtons:			# Checks if the player wins in the next move
		human = player1.copy()
		point = buttonList.index(i) + 1
		human.append(point)
		if check(human):
			return i
	
	board = get_board(player1,player2)		# Gets a board replica
	pos = find_best_move(board)				# Uses advanced algorithm to find the best move 
	return buttonList[pos-1]				# Returns the best move(Button) for autoplay

	
def autoplay():
	# Autoplay function for the AIplayer
	global buttonList
	btn = getButton()
	pos = buttonList.index(btn) + 1
	buttonPressed(btn, pos)					# Calls the buttonPressed command to use the move


def checkDraw():
	# Checks if the move results in a draw
	global remainingButtons
	if len(remainingButtons) == 0:
		displayresult('Draw!')


def check(player):
	# Checks if the player wins or not with this move
	global winPoints
	for i in winPoints:
		won = True
		for j in i:
			if j not in player:
				won = False
				break
		if won:
			return True
	return False

if __name__ == '__main__':
	root = Tk()																			
	singlePlayer = messagebox.askyesno('Select Mode','Singleplayer?')	
	root.title('Tic-Tac-Toe')
	width,height = 60,70
	
	crossImg = Image.open('assets/cross.png')							# Opens the image cross
	crossImg = crossImg.resize((width,height), Image.ANTIALIAS)			# Resizes the image
	circleImg = Image.open('assets/circle.png')							# Opens the image for circle
	circleImg = circleImg.resize((width,height), Image.ANTIALIAS)		
	
	# Converts those images to Tkinter image type
	cross = ImageTk.PhotoImage(crossImg)			
	circle = ImageTk.PhotoImage(circleImg)
	
	turn = 'cross'								# Sets the turn to player1 by default
	player = StringVar()
	player.set('Player 1')
	
	# Main UI Implementation
	
	w,h = 7	,3
	
	Label(root, text = 'Tic-Tac-Toe', font = ('bold', 20), fg = 'darkblue').pack(side = TOP)
	labelframe = Frame(root)
	labelframe.pack(side = TOP)
	Label(labelframe, text = 'Turn : ', fg = 'red').pack(side = LEFT)
	Label(labelframe, textvariable = player, fg = 'green').pack(side = LEFT)
	
	row0 = Frame(root)
	row0.pack(side = TOP)
	row1 = Frame(root)
	row1.pack(side = TOP)
	row2 = Frame(root)
	row2.pack(side = TOP)
	
	b1 = Button(row0,width = w, height = h, command = lambda : buttonPressed(b1, 1))
	b1.pack(side = LEFT)
	b2 = Button(row0, width = w, height = h,  command = lambda : buttonPressed(b2, 2))
	b2.pack(side = LEFT)
	b3 = Button(row0, width = w, height = h, command = lambda : buttonPressed(b3, 3))
	b3.pack(side = LEFT)
	
	b4 = Button(row1, width = w, height = h, command = lambda : buttonPressed(b4, 4))
	b4.pack(side = LEFT)
	b5 = Button(row1, width = w, height = h, command = lambda : buttonPressed(b5, 5))
	b5.pack(side = LEFT)
	b6 = Button(row1, width = w, height = h, command = lambda : buttonPressed(b6, 6))
	b6.pack(side = LEFT)
	
	b7 = Button(row2, width = w, height = h, command = lambda : buttonPressed(b7, 7))
	b7.pack(side = LEFT)
	b8 = Button(row2, width = w, height = h, command = lambda : buttonPressed(b8, 8))
	b8.pack(side = LEFT)
	b9 = Button(row2, width = w, height = h, command = lambda : buttonPressed(b9, 9))
	b9.pack(side = LEFT)
	
	remainingButtons = [b1,b2,b3,b4,b5,b6,b7,b8,b9]
	buttonList = remainingButtons.copy()
	
	winPoints = [[1,2,3], [1,4,7], [1,5,9], 
			[2,5,8], 
			[3,6,9], [3,5,7],
			[4,5,6],
			[7,8,9]]
	player1 = []
	player2 = []
	
	root.mainloop()											# Mainloop of the UI is called