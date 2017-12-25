#!/usr/bin/env python

# Problem Statement ===============================================================================

# Program to find a short sequence of moves that restores the canonical configuration of given 
# initial board.
# Input : File name to read the given puzzle state from
# Output : All steps taken in form of R/U/D/L<row_no/col_no><tiles_moved> seprated by whitespace

# Basic Solution Idea =============================================================================

# The algorithm uses algo#3 from the slides to find the step to reach to canonical configuration of
# board. For using algo#3 we need to have admissible and consistent heuristic. Hence, we take the
# heuristic to be the sum of manhatten distances divided by 3.00.

# Citations =======================================================================================

# Heuristic discussed with Ronak Parekh(parekhr) and group of first year MS in CS students (don't know names)
# Reading files, http://www.pythonforbeginners.com/files/reading-and-writing-files-in-python
# Heapq documentation, https://docs.python.org/2/library/heapq.html
# Functions for sum of row and column taken from Assignment 0
# Printing group code from code for printing matrix from Assignemnt 0

# Imports =========================================================================================

import sys
import heapq

# Helper functions ================================================================================

# Finds and returns the position of 0 in given state matrix
def find_pos_0(state):					
	for row in range(0, 4):							# For all rows and column
		for col in range(0, 4):
			if state[row][col] == 0:				# If item on the position is 0, return that position as tuple
				return (row, col)

# Taken from assignment0 nrooks implementation, returns sum of all numbers in a row
def row_sum(state, row):
	return sum(state[row]) 

# Taken from assignment0 nrooks implementation, returns sum of all numbers in a col
def col_sum(state, col):
	return sum([row[col] for row in state]) 
	
# Checking if a state is goal state
# Since we know the position of all the numbers in canonical confirguration hence,
# For goal state we can check the sum of rows and cols against the sum of rows and cols in canonical configuration
def is_goal(state):	
	# Sum of row1 = 10, row2 = 26, row3 = 42 and row4 = 42
	if row_sum(state, 0) != 10 or row_sum(state, 1) != 26 or row_sum(state, 2) != 42 or row_sum(state, 3) != 42:	# Check sum in rows
		return False
	# Sum of col1 = 28, col2 = 32, col3 = 36 and col4 = 24
	if col_sum(state, 0) != 28 or col_sum(state, 1) != 32 or col_sum(state, 2) != 36 or col_sum(state, 3) != 24:	# Check sum in cols
		return False
	return True										# All sums of rows and cols matches, hence state is goal state, return true

# calculate_h calculates the value of heuristic for the given state
# Heuristic is taken as sum of manhatten distances for all elements divided by 3.00
# this heuristic is admissible and consistent, since we can move maximum of 3 tiles in 1 move
# hence, to can put maximum of 3 numbers in place in 1 move, therefore we divide the sum by 3.00 
def calculate_h(state):
	h_s = 0.00
	for row in range(0, 4):							# for all rows and cols
		for col in range(0, 4):
			if state[row][col] != 0:
				# Use of mathematical properties to find the position of a number in canonical configuration
				# 0 based row no. of a number is (number - 1) / 4
				# 0 based col no. of a number is (number - 1) % 4
				h_s = h_s + abs(row - (state[row][col] - 1) / (4)) + abs(col - (state[row][col] - 1) % (4))
	return (h_s / 3.00)								# return sum of all manhatten distances divided by 3.00
	
# successor generates the successor states for the given state
# each state could generate maximum of 6 states, with all the 3 tiles moved in row and column
# we generate the new states by first preparing the new row or new col formed by moving tiles
# and then replace it with old row or col in the original given state
def successor(state_tuple):
	succ_states = []
	state = state_tuple[1]
	pos_0 = state_tuple[2]
	g_s = state_tuple[3]
	str_so_far = state_tuple[4]
	for row in range(0, 4):													# This will generate 3 states, for all row != pos_0[0]
		new_row = []
		if row < pos_0[0]:													# Moving tiles on the top of tile with 0
			for i in range(0, row):
				new_row.append(state[i][pos_0[1]])
			new_row.append(0)
			for i in range(row, pos_0[0]):
				new_row.append(state[i][pos_0[1]])
			for i in range(pos_0[0] + 1, 4):
				new_row.append(state[i][pos_0[1]])
		elif row > pos_0[0]:												# Moving tiles below tile with 0
			for i in range(0, pos_0[0]):
				new_row.append(state[i][pos_0[1]])
			for i in range(pos_0[0] + 1, row + 1):
				new_row.append(state[i][pos_0[1]])
			new_row.append(0)
			for i in range(row + 1, 4):
				new_row.append(state[i][pos_0[1]])
		if row != pos_0[0]:													# Generating string for each successor state from previous state
			new_state = []
			new_pos_0 = (row, pos_0[1])
			new_str = ""
			if row < pos_0[0]:												# If 0 tile is moved up, then other tiles are moved down
				new_str = "D"
			else:
				new_str = "U"												# If 0 tile is moved down, then other tiles are moved up
			for r in range(0, 4):											# replace the old row by new_row and generate new state
				new_r = []
				for c in range(0 ,4):
					if c == pos_0[1]:
						new_r.append(new_row[r])
					else:
						new_r.append(state[r][c])
				new_state.append(new_r)
			succ_states.append((1 + g_s + calculate_h(new_state), new_state, new_pos_0, (g_s + 1), str_so_far + " " + new_str + str(abs(row - pos_0[0])) + str(pos_0[1] + 1)))
	for col in range(0, 4):													# This will generate 3 states, for all col != pos_0[1]
		new_col = []
		if col < pos_0[1]:													# Moving tiles on the left of tile with 0
			for i in range(0, col):
				new_col.append(state[pos_0[0]][i])
			new_col.append(0)
			for i in range(col, pos_0[1]):
				new_col.append(state[pos_0[0]][i])
			for i in range(pos_0[1] + 1, 4):
				new_col.append(state[pos_0[0]][i])
		elif col > pos_0[1]:												# Moving tiles on the right of tile with 0
			for i in range(0, pos_0[1]):
				new_col.append(state[pos_0[0]][i])
			for i in range(pos_0[1] + 1, col + 1):
				new_col.append(state[pos_0[0]][i])
			new_col.append(0)
			for i in range(col + 1, 4):
				new_col.append(state[pos_0[0]][i])
		if col != pos_0[1]:													# Generating string for each successor state from previous state
			new_pos_0 = (pos_0[0], col)
			new_str = ""
			if col < pos_0[1]:												# If 0 tile is moved left, then other tiles are moved right
				new_str = "R"
			else:															# If 0 tile is moved right, then other tiles are moved left
				new_str = "L"
			new_state = state[0:pos_0[0]] + [new_col] + state[pos_0[0] + 1:]# replace the old col by new_col and generate new state
			succ_states.append((1 + g_s + calculate_h(new_state), new_state, new_pos_0, (g_s + 1), str_so_far + " " + new_str + str(abs(col - pos_0[1])) + str(pos_0[0] + 1)))
	return succ_states														# Return list of successor states

# Since, the h(s) we are taking is consistent, hence we are going to use algo#3
def solve(state):
	if is_goal(state):														# Check if given state is goal state, if yes, return with ""
		return ""
	fringe = []																# Fringe to store unvisited states
	closed = []																# List to store visited states
	pos_0 = find_pos_0(initial_state)										# Find the initial position for 0
	heapq.heappush(fringe, (0 + calculate_h(state) , state, pos_0, 0, ""))	# Push the current state on fringe
																			# (g(s) + h(s), state, pos_0, g(s), "<string_till_state>")
	while len(fringe) > 0:													# While there is an element in the fringe
		current_tuple = heapq.heappop(fringe)								# Pop the element from the fringe
		closed.append(current_tuple[1])										# Add current state to closed state
		if is_goal(current_tuple[1]):										# If current state is goal state, return the solution string
			return current_tuple[4].strip()
		for succ in successor(current_tuple):								# For all the successors of current state
			if succ[1] not in closed:										# If succ is already in closed states then discard it
				in_fringe = False											# Flag for succ in fringe
				for st in fringe:											# Loop over whole fringe
					if st[1] == succ[1]:									# If fringe item matches then set flag to true
						in_fringe = True
						if st[0] > succ[0]:									# If item in fringe has lower priority then remove it from fringe
							fringe.remove(st)								# and put the new one in
							heapq.heappush(fringe, succ)
				if not in_fringe:											# If succ is not in fringe, add to fringe
					heapq.heappush(fringe, succ)
	return "No Solution Found!"												# No solution exists

# Main ============================================================================================

# Initialize initial_state with all 0's
initial_state = [[0]*4]*4

# Reading file name from the console
file_name = sys.argv[1]

# Using list comprehension to read file and initialize initial_state
with open(file_name, "r") as file_obj:
    initial_state = [[int(pos) for pos in line.strip().split()] for line in file_obj]	

# Print the solution string received from solve function
print solve(initial_state)