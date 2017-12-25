#!/usr/bin/env python

# Problem Statement ===============================================================================

# Program to find an assignment of students to teams that minimizes the total amount of work the
# course staff needs to do.
# Input : File name to read data from
# 		: k, time in minutes to evalaute a group
#		: m, time in minutes for meetings to resolve conflict if someone not to work with is in group
#		: n, time in minutes for meetings to address is someone preferred is not on list
# Output : Each line containing people from a group
#		 : Last line, total times in minutes required by course staff

# Basic Solution Idea =============================================================================

# While reading the input file we calculate the maximum cost which a particular person could incur,
# we record the person's preferences in a dictionary with name as key and other data as tuple and
# store the cost in priority queues. We loop till the priority queue is empty and assign groups by
# considering the preferences of the person with maximum cost.

# Since, the time for address group size issue is 1, hence we consider it to be really small and
# hence, try to make group of 3 irrespective of person's preference.

# Citations =======================================================================================

# Problem discussed with Ronak Parekh(parekhr), Sagar Vora(savora) and Manan Papdiwala(manpapdi)
# Reading files, http://www.pythonforbeginners.com/files/reading-and-writing-files-in-python
# Heapq documentation, https://docs.python.org/2/library/heapq.html
# Printing group code from code for printing matrix from Assignemnt 0

# Imports =========================================================================================

import sys
import heapq

# Helper functions ================================================================================

# solve_problem goes through the input_dict and forms group out of it, removing people who are assigned to any group
def solve_problem(input_dict, fringe, reverse_fringe):
	group_assignment = []												# Data structure to store group formed
	total_cost = 0														# Variable to store total cost of all groups
	while len(reverse_fringe) > 0:										# Loop till reverse_fringe as an item left
		nxt = heapq.heappop(reverse_fringe)								# Pop the element with maximum cost from reverse_fringe
		fringe.remove((-(nxt[0]), nxt[1]))								# Remove the counter part from fringe
		if nxt[1] in input_dict:										# If that item is in input_dict, this is just precautionary check
			cost = k													# Cost for a particular group, k
			group = [nxt[1]]											# Form new group with person as it's first member
			item = input_dict[nxt[1]]									# Fetch the data for the person form the input_dict
			for person in item[1]:										# For each person in people preferred by person we are considering
				if person in input_dict:								# If that person is not assigned to any group
					person_item = input_dict[person]
					if nxt[1] in person_item[2]:
						if m < n:
							if len(group) < 3:							# If the new group's size is less than 3 then sdd person to the new group
								group.append(person)
					else:
						if len(group) < 3:								# If the new group's size is less than 3 then sdd person to the new group
							group.append(person)
			new_fringe = []												# Data structure to store item's pulled from fringe
			while len(group) < 3 and len(fringe) != 0:					# If fringe is not empty and length of new groups is less than 3
				nxt_p = heapq.heappop(fringe)							# Pop the element with minimum cost from fringe
				heapq.heappush(new_fringe, nxt_p)						# Add that element to new_fringe
				item_p = input_dict[nxt_p[1]]							# Fetch the data for the person form the input_dict
				if nxt_p[1] not in group and nxt_p[1] not in item[2]:	# If the person is not already in group and not in people not preferred
					add_to_group = True									# Flag to mark if the person could be added to group
					for ignore_person in item_p[2]:						# If any person not preferred is in the group then mark the flag false
						if ignore_person in group:
							add_to_group = False						
							break
					if add_to_group:									# If the flag is true then add that person to group
						group.append(nxt_p[1])
			while len(fringe) != 0:										# Copy all remaning items from fringe to new_fringe
				nxt_p = heapq.heappop(fringe)
				heapq.heappush(new_fringe, nxt_p)
			fringe = new_fringe											# Set fringe to be new_fringe
			for person in group:										# For every person in the group
				person_item = input_dict[person]						# Fetch the data for the person form the input_dict
				# Add Group Size Cost
				if person_item[0] != 0 and person_item[0] != len(group):# If the size of group is not equal to what person wanted, add 1
					cost = cost + 1
				# Add mCost
				for prefer_person in person_item[1]:					# If a person preferred is not in group, add n to cost
					if prefer_person not in group:
						cost = cost + n
				# Add nCost
				for ignore_person in person_item[2]:					# If a person not preferrred is in the group, add m to cost
					if ignore_person in group:
						cost = cost + m
				if person in input_dict:								# Precautionary check if that person is in the input_dict
					del input_dict[person]								# delete that person from the input_dict
				if (-(person_item[3]), person) in reverse_fringe:		# Precautionary check if that person is in the reverse_fringe
					reverse_fringe.remove((-(person_item[3]), person))	# Remove the person's record from reverse_fringe
					fringe.remove(((person_item[3]), person))			# Remove the person's record from fringe
			group_assignment.append(group)								# Add new group to global group directory
			total_cost = total_cost + cost								# Add new group's cost to total cost
	return (group_assignment, total_cost)								# Return all groups and total cost as tuple

# Main ============================================================================================

# Read inputs from console
input_file = sys.argv[1]
k = int(sys.argv[2])
m = int(sys.argv[3])
n = int(sys.argv[4])

# Data structures for storing data read from file and meta data
# input_data stores the data from input file as is, with person's name as key and other values like
# group size, preferences etc as tuple
# reverse_fringe and fringe stores the cost along with person's name, and are used as priority queues
input_dict = dict()
reverse_fringe = []
fringe = []

# Read data from given file, store in dictionary and populate metadata
# We read a line, split it by whitespaces and store the data in a dictionary with person's name as key
# We calculate the maximum cost a person could incur and store that cost in two priority queues
# First has cost with negation and person's name, hence, on pop it gives person with maximum cost
# Second has cost along with person's name, hence, on pop it gives person with minimum cost
with open(input_file, "r") as file_obj:								# Open and start reading file
    for line in file_obj:											# Read a line from file 
		items = line.strip().split()								# Split a line by whitespace
		item_tuple = (int(items[1]), [person for person in items[2].strip().split(',') if person != '_'], [person for person in items[3].strip().split(',') if person != '_'])		# Create a tuple with entries from input file
		itemCost = (2 if item_tuple[0] != 0 else 0) + (len(item_tuple[1]) * n) + (len(item_tuple[2]) * m)		# Calculate maximum cost a person would cost
		input_dict[items[0]] = item_tuple + (itemCost,)															# Add cost as part of data structure
		heapq.heappush(reverse_fringe, (-(itemCost), items[0]))													# Store negation of cost along with person's name 
		heapq.heappush(fringe, (itemCost, items[0]))															# Store cost along with person's name 
		
		
# solve_problem solves the given problem and returns a tuple with groups and total cost
answers = solve_problem(input_dict, fringe, reverse_fringe)

# Print all the groups which we formed
print ("\n".join([" ".join([person for person in group]) for group in answers[0]]))	
	
# Print the total incurring cost
print answers[1]