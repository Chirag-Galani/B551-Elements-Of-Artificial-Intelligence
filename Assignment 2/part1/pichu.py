#!/usr/bin/env python
#
#
#
#
#
# P = 10, R = 20, B = 20, N = 30, Q = 50, K = 100
#
#
import sys
import copy
import Queue as Queue

def PrintAsLine(board):
	z=0
	listboard = [0]*64
	for x in range(0,8):
		for y in range(0,8):
			listboard[z] = board[x][y]
			z += 1
	return ''.join(listboard)

def boardCost(board):
	white_points = 0
	black_points = 0	
	for x in range (0,8):
		for y in range (0,8):
			if board[x][y].islower():
			    black_points += piece_costs[board[x][y]]
			elif board[x][y].isupper():
			    white_points += piece_costs[board[x][y].lower()]			
	if currentPlayer == "w":
		currentPlayer_points = white_points
		oppPlayer_points = black_points
	else:
		currentPlayer_points = black_points
		oppPlayer_points = black_points
	return currentPlayer_points - oppPlayer_points

def KingKilled(board,currentPlayer):
	isOppKingDead = 0
	if (currentPlayer == "w" and (not any('k' in subboard for subboard in board))) or (currentPlayer == "b" and (not any('K' in subboard for subboard in board))):
		isOppKingDead = 1
	return isOppKingDead

def checkPiece(board,player,curr_piece_x,curr_piece_y,next_x,next_y):
	if board[next_x][next_y]!=".":
		if (player == "w" and board[next_x][next_y].isupper()) or (player == "b" and board[next_x][next_y].islower()):
			return 0
		elif (player == "b" and board[next_x][next_y].isupper()) or (player == "w" and board[next_x][next_y].islower()):
			return 2
	return 1

def successors(board,player):
	#parse through the board searching for the pieces to move
	successors_list = []
	for x in range (0,8):
		for y in range(0,8):
			piece = board[x][y]
			t = 0
			z = 0
			if (player == "w" and piece.isupper()) or (player == "b" and piece.islower()):
				#Q,R,B
				if piece.lower() in ("qrb"):
					x_positive_range = 8
					x_negative_range = 0
					y_positive_range = 8
					y_negative_range = 0
					#Q,R
					if piece.lower() in ("qr"):
						#Horizontal right
						t = y+1
						while t<y_positive_range:
							piece_move = checkPiece(board,player,x,y,x,t)
							if piece_move>0:
								new_board = copy.deepcopy(board)
								new_board[x][y]="."
								new_board[x][t]=piece
								successors_list.append(new_board)
							if piece_move!=1:
								break
							t+=1
						#horizontal left
						t = y-1
						while t>=y_negative_range:
							piece_move = checkPiece(board,player,x,y,x,t)
							if piece_move>0:
								new_board = copy.deepcopy(board)
								new_board[x][y]="."
								new_board[x][t]=piece
								successors_list.append(new_board)
							if piece_move!=1:
								break
							t-=1
						#vertical down
						z = x+1
						while z<x_positive_range:
							piece_move = checkPiece(board,player,x,y,z,y)
							if piece_move>0:
								new_board = copy.deepcopy(board)
								new_board[x][y]="."
								new_board[z][y]=piece
								successors_list.append(new_board)
							if piece_move!=1:
								break
							z+=1
						#vertical up
						z = x-1
						while z>=x_negative_range:
							piece_move = checkPiece(board,player,x,y,z,y)
							if piece_move>0:
								new_board = copy.deepcopy(board)
								new_board[x][y]="."
								new_board[z][y]=piece
							if piece_move!=1:
								break
							z-=1
					#Q,B
					if piece.lower() in ("qb"):
						#Right up
						t = y+1
						z = x-1
						while t<y_positive_range and z>=x_negative_range:
							piece_move = checkPiece(board,player,x,y,z,t)
							if piece_move>0:
								new_board = copy.deepcopy(board)
								new_board[x][y]="."
								new_board[z][t]=piece
								successors_list.append(new_board)
							if piece_move!=1:
								break							
							t+=1
							z-=1
						#Right down
						t = y+1
						z = x+1
						while t<y_positive_range and z<x_positive_range:
							piece_move = checkPiece(board,player,x,y,z,t)
							if piece_move>0:
								new_board = copy.deepcopy(board)
								new_board[x][y]="."
								new_board[z][t]=piece
								successors_list.append(new_board)
							if piece_move!=1:
								break							
							t+=1
							z+=1
						#Left up
						t = y-1
						z = x-1
						while t>=y_negative_range and z>=x_negative_range:
							piece_move = checkPiece(board,player,x,y,z,t)
							if piece_move>0:
								new_board = copy.deepcopy(board)
								new_board[x][y]="."
								new_board[z][t]=piece
								successors_list.append(new_board)
							if piece_move!=1:
								break							
							t-=1
							z-=1
						#Left down
						t = y-1
						z = x+1
						while t>=y_negative_range and z<x_positive_range:
							piece_move = checkPiece(board,player,x,y,z,t)
							if piece_move>0:
								new_board = copy.deepcopy(board)
								new_board[x][y]="."
								new_board[z][t]=piece
								successors_list.append(new_board)
							if piece_move!=1:
								break							
							t-=1
							z+=1						
				elif (piece.lower() == "k"):
						#left
						t = y-1
						z = x
						if t >=0:
							piece_move = checkPiece(board,player,x,y,z,t)
							if piece_move>0:
								new_board = copy.deepcopy(board)
								new_board[x][y]="."
								new_board[z][t]=piece
								successors_list.append(new_board)
						#left up
						t = y-1
						z = x-1
						if t >=0 and z>=0:
							piece_move = checkPiece(board,player,x,y,z,t)
							if piece_move>0:
								new_board = copy.deepcopy(board)
								new_board[x][y]="."
								new_board[z][t]=piece
								successors_list.append(new_board)
						#left down
						t = y-1
						z = x+1
						if t >=0 and z<8:
							piece_move = checkPiece(board,player,x,y,z,t)
							if piece_move>0:
								new_board = copy.deepcopy(board)
								new_board[x][y]="."
								new_board[z][t]=piece
								successors_list.append(new_board)
						#up
						t = y
						z = x-1
						if z >=0:
							piece_move = checkPiece(board,player,x,y,z,t)
							if piece_move>0:
								new_board = copy.deepcopy(board)
								new_board[x][y]="."
								new_board[z][t]=piece
								successors_list.append(new_board)
						#down
						t = y
						z = x+1
						if z <8:
							piece_move = checkPiece(board,player,x,y,z,t)
							if piece_move>0:
								new_board = copy.deepcopy(board)
								new_board[x][y]="."
								new_board[z][t]=piece
								successors_list.append(new_board)
						#right
						t = y+1
						z = x
						if t<8:
							piece_move = checkPiece(board,player,x,y,z,t)
							if piece_move>0:
								new_board = copy.deepcopy(board)
								new_board[x][y]="."
								new_board[z][t]=piece
								successors_list.append(new_board)
						#right up
						t = y+1
						z = x-1
						if z >=0 and t<8:
							piece_move = checkPiece(board,player,x,y,z,t)
							if piece_move>0:
								new_board = copy.deepcopy(board)
								new_board[x][y]="."
								new_board[z][t]=piece
								successors_list.append(new_board)
						#right down
						t = y+1
						z = x+1
						if z<8 and t<8:
							piece_move = checkPiece(board,player,x,y,z,t)
							if piece_move>0:
								new_board = copy.deepcopy(board)
								new_board[x][y]="."
								new_board[z][t]=piece
								successors_list.append(new_board)
				elif (piece.lower() == "n"):
						#left up
						t = y-2
						z = x-1
						if z >=0 and t>=0:
							piece_move = checkPiece(board,player,x,y,z,t)
							if piece_move>0:
								new_board = copy.deepcopy(board)
								new_board[x][y]="."
								new_board[z][t]=piece
								successors_list.append(new_board)
						#left down
						t = y-2
						z = x+1
						if z<8 and t>=0:
							piece_move = checkPiece(board,player,x,y,z,t)
							if piece_move>0:
								new_board = copy.deepcopy(board)
								new_board[x][y]="."
								new_board[z][t]=piece
								successors_list.append(new_board)
						#up left
						t = y-1
						z = x-2
						if z>=0 and t>=0:
							piece_move = checkPiece(board,player,x,y,z,t)
							if piece_move>0:
								new_board = copy.deepcopy(board)
								new_board[x][y]="."
								new_board[z][t]=piece
								successors_list.append(new_board)
						#up right
						t = y+1
						z = x-2
						if t<8 and z>=0:
							piece_move = checkPiece(board,player,x,y,z,t)
							if piece_move>0:
								new_board = copy.deepcopy(board)
								new_board[x][y]="."
								new_board[z][t]=piece
								successors_list.append(new_board)
						#right up
						t = y+2
						z = x-1
						if z>=0 and t<8:
							piece_move = checkPiece(board,player,x,y,z,t)
							if piece_move>0:
								new_board = copy.deepcopy(board)
								new_board[x][y]="."
								new_board[z][t]=piece
								successors_list.append(new_board)
						#right down
						t = y+2
						z = x+1
						if z<8 and t<8:
							piece_move = checkPiece(board,player,x,y,z,t)
							if piece_move>0:
								new_board = copy.deepcopy(board)
								new_board[x][y]="."
								new_board[z][t]=piece
								successors_list.append(new_board)
						#down left
						t = y-1
						z = x+2
						if z<8 and t>=0:
							piece_move = checkPiece(board,player,x,y,z,t)
							if piece_move>0:
								new_board = copy.deepcopy(board)
								new_board[x][y]="."
								new_board[z][t]=piece
								successors_list.append(new_board)
						#down right
						t = y+1
						z = x+2
						if z<8 and t<8:
							piece_move = checkPiece(board,player,x,y,z,t)
							if piece_move>0:
								new_board = copy.deepcopy(board)
								new_board[x][y]="."
								new_board[z][t]=piece
								successors_list.append(new_board)
				elif (piece.lower() == "p"):
					if player == "w":
						piece_move_one = checkPiece(board,player,x,y,x+1,y)
						if piece_move_one == 1:
							if x < 6:							
								new_board = copy.deepcopy(board)
								new_board[x][y]="."
								new_board[x+1][y]=piece
								successors_list.append(new_board)
								if x == 1: #pawn hasn't moved
									piece_move_two = checkPiece(board,player,x,y,x+2,y)
									if piece_move_one == 1:
										new_board = copy.deepcopy(board)
										new_board[x][y]="."
										new_board[x+2][y]=piece
										successors_list.append(new_board)
							else:	#promotion
								new_board = copy.deepcopy(board)
								new_board[x][y]="."
								new_board[x+1][y]="Q"
								successors_list.append(new_board)
						if y-1 >=0:								
							piece_move_left = checkPiece(board,player,x,y,x+1,y-1)
							if piece_move_left == 2:
								new_board = copy.deepcopy(board)
								new_board[x][y]="."
								new_board[x+1][y-1]=piece
								successors_list.append(new_board)
						if y+1<8:												
							piece_move_right = checkPiece(board,player,x,y,x+1,y+1)
							if piece_move_right == 2:
								new_board = copy.deepcopy(board)
								new_board[x][y]="."
								new_board[x+1][y+1]=piece
								successors_list.append(new_board)
					else:
						piece_move_one = checkPiece(board,player,x,y,x-1,y)
						if piece_move_one == 1:
							if x > 1:							
								new_board = copy.deepcopy(board)
								new_board[x][y]="."
								new_board[x-1][y]=piece
								successors_list.append(new_board)
								if x == 6: #pawn hasn't moved
									piece_move_two = checkPiece(board,player,x,y,x-2,y)
									if piece_move_one == 1:
										new_board = copy.deepcopy(board)
										new_board[x][y]="."
										new_board[x-2][y]=piece
										successors_list.append(new_board)
							else:	#promotion
								new_board = copy.deepcopy(board)
								new_board[x][y]="."
								new_board[x-1][y]="Q"
								successors_list.append(new_board)
						if y-1 >=0:								
							piece_move_left = checkPiece(board,player,x,y,x-1,y-1)
							if piece_move_left == 2:
								new_board = copy.deepcopy(board)
								new_board[x][y]="."
								new_board[x-1][y-1]=piece
								successors_list.append(new_board)
						if y+1<8:												
							piece_move_right = checkPiece(board,player,x,y,x-1,y+1)
							if piece_move_right == 2:
								new_board = copy.deepcopy(board)
								new_board[x][y]="."
								new_board[x-1][y+1]=piece
								successors_list.append(new_board)
	return successors_list

def Maximize(board,curDept):
	curDept += 1
	maxVal = -1
	if curDept == depthToParse:
		return boardCost(board)
	else:
		for s in successors(board,currentPlayer):
			#print s,boardCost(s)
			if boardCost(s) > maxVal:
				if KingKilled (s,currentPlayer):
					maxVal = 64 * 100
					break
				curMax = (Minimize(s,curDept))
				if maxVal < curMax:
					maxVal = curMax
	return maxVal

def Minimize(board,curDept):
	curDept += 1
	minVal = 64 * 100
	if curDept == depthToParse:
		return boardCost(board)
	else:
		for s in successors(board,oppPlayer):
			if boardCost(s) < minVal:
				if KingKilled (s,oppPlayer):
					minVal = -1
					break
			curMin = (Maximize(s,curDept))
			if minVal > curMin:
				maxVal = curMin
	return minVal

#Code starts
#Input From user
currentPlayer = str(sys.argv[1])
stringBoardInput = str(sys.argv[2])
timeInSec = int(sys.argv[3])
#piece costs
piece_costs = {'p': 10, 'b': 20, 'n': 30, 'r': 20, 'q': 50, 'k': 100}
#depth to parse
if timeInSec <= 120:
	depthToParse = 3
elif timeInSec <= 500:
	depthToParse = 4
elif timeInSec > 500:
	depthToParse = 5
#current player and opposite player
if currentPlayer == "w":
	oppPlayer = "b"
else:
	oppPlayer = "w"
#Convert string board to 2D array list
listBoard = list(stringBoardInput)
startBoard = [[None]*8 for _ in range(8)]
z = 0
for x in range (0,8):
	for y in range (0,8):
		startBoard[x][y] = listBoard[z]
		z += 1
#Run a pseudo Maximize code to get the value of the board with Max Minimum
#Printing the output as soon as I find a value which is more than the current Maximum or a node which has killed the opponents king
#This helps to provide atleast one output, and then improves upon it.
maxVal = -1
new_board=[]
for s in successors(startBoard,currentPlayer):
	if KingKilled (s,currentPlayer):
		print PrintAsLine(s)
		break
	curMax = Minimize(s,1)
	if maxVal < curMax:
		maxVal = curMax
		print PrintAsLine(s)
