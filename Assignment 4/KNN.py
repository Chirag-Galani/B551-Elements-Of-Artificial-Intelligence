#!/usr/bin/env python
'''
#
# The nearest neighbour algorithm is a supervised learning algorithm, which on the basis of its training and the problem at hand, defines neighbors for the test-data 
# and assigns the output to the test-data as per k-nearest neighbors, where k is a defined value.
#
# Problem : We have been given a train data set which contains the correct orientations of around 36000 images, using this we have to train our program.
#		    We then have to predict/assign an orientation for the images in the test-data set
#
# Formulation : For knn, we require miimal training, i.e. create the model file, it is essentially a copy of the train_file. Once the model file is created
#				we use it for classification of the test-data, we find n-neighbors based on euclidean distance of it's pixels w.r.t. to the pixels in the model file.
#				We then select k neighbors based on least euclidean distance, and then go through a voting to find the most orientation represented by the neighbors.
#				This is then assigned to the test-data file.
#
# Code-Descrption : The class file present here is called from orient.py based on the input provided
#
#					Training:
#					orient.py train train_file.txt mddel_file.txt nearest
#					The above calls the class in training mode, in which we essentially create a replica of the train_file in the model_file.
#					we remove the image_name present in the train file, as it is of no use for the test-data classification purpose.
#
#					Testing:
#					orient.py test test_file.txt mddel_file.txt nearest
#					The above calls the class in test mode, in which we get the pixels for the test-file and compute the euclidean distance	
#					against each pixel set in the model_file, we then use a priority queue to find the K nearest neighbors (we use k value of 37).
#					Using the k nearest neighbors we setup a vote list which finds out the orientation most represented by the neighbors
#					We assign this orientation to the test-image, and evaluate if the one predicted/assigned is the same as the one provided in the test-data
#					If they are not same we increment a counter which when divided by the number of test-images, gives us the accuracy.
#
# Problems(P), Assumptions(A), Simplifications (S), Design Decisions (DD):
#	The input file names for the model_file will be the one created by the train function of this class (A)
#	Storing the imageName of the training-data interferes with testing while trying to pull it into a numpy array (P)
#	Remove the imageName while training (S)
#	Write the data directly into the output_file or model_file instead of storing it into memory (DD)	
#
#
# Analysis : 
#	We evaluated the implementation for various values of k, we found k = 1 gives us an accuracy of ____ and k = 37, gives us an accuracy of 70.94.
#	It takes less than 20sec to train the data and approximately 28 minutes for the test classification, but for some values of k it escalated more than 60 mins,
#	for a safer estimate I will state that testing will take approximately 60 mins.
#			k 	|     Accuracy             |
#      ----------------------------------------------------------
#			1	|	66.58		   |
#			5	|	64.98		   |
#			10	|	67.3		   |
#			15	|	68.11		   |
#			20	|	68.84		   |
#			25	|	70.6		   |
#			30	|	69.58		   |
#			35	|	69.98		   |
#			37	|	70.94		   |
#			40	|	69.6		   |
#	 ----------------------------------------------------------
'''

import Queue as Q
import os
import math
import numpy as np

class KNN:
	#Globally defining K, can be done elsewhere as well, but preferred to keep it here
	def __init__(self):
		self.k = 37

	#Evaluate the vote and distances associated with an image
	def evaluateVote(self,votes,dists):
		votesMax = [i for i,x in enumerate(votes) if x == max(votes)]
		if len(votesMax) == 1:
			position = votesMax[0]
		else:
			minDist = max(dists) + 100
			for i in votesMax:
				Dist = dists[i]
				if minDist > Dist:
					minDist = Dist
					position = i
		orientation = 0 if position == 0 else 90 if position == 1 else 180 if position == 2 else 270
		return orientation


	#Test portion
	def test(self,model_file,test_file,output_file):
		TestRight = 0.0
		TestAll = 0.0
		if os.path.isfile(output_file):
			os.remove(output_file)		
		with open(test_file) as tf:
			for testline in tf: 
				toRemoveText = testline.find('.') + 5
				TestFile = testline[:toRemoveText]
				newTestLine = testline.replace(testline[:toRemoveText],'')
				TestArray = np.fromstring(newTestLine, dtype=int, sep=' ')
				testOrientation = TestArray[0]
				TestPixels = np.delete(TestArray,[0])
				#cur_orientation = algo.test(TestPixels,model_file)
				priorityQueue = Q.PriorityQueue()
				#print testOrientation,TestPixels
				mf = open(model_file,"r")
				for modelline in mf:
					ModelArray = np.fromstring(modelline, dtype=int, sep=' ')
					ModelOrientation = ModelArray[0]
					ModelPixels = np.delete(ModelArray,[0])
					#priorityQueue.put((math.sqrt(np.sum(np.power(np.linalg.norm(TestPixels)-np.linalg.norm(ModelPixels),2))),ModelOrientation))
					priorityQueue.put((math.sqrt(np.sum(np.power(TestPixels-ModelPixels,2))),ModelOrientation))
				dists = [0]*4
				votes = [0]*4
				for a in range(self.k):
					distance,orientation = priorityQueue.get()
					orientation = int(orientation)
					if orientation == 0:
						dists[0] += distance
						votes[0] += 1
					if orientation == 90:
						dists[1] += distance
						votes[1] += 1
					if orientation == 180:
						dists[2] += distance
						votes[2] += 1
					if orientation == 270:
						dists[3] += distance
						votes[3] += 1
				cur_orientation = self.evaluateVote(votes,dists)
				with open(output_file,'a') as outs:
					output_line = str(TestFile) + " " + str(cur_orientation) + "\n"
					outs.write(output_line)
				TestAll += 1.0
				if cur_orientation == testOrientation:
					TestRight += 1.0
		print "Accuracy :",(TestRight/TestAll)*100
		return cur_orientation

	def train(self,train_file,model_file):
		#import the training file and create the model file
		#For KNN we shall just replicate the test file
		
		#If model.txt exists then delete it
		if os.path.isfile(model_file):
			os.remove(model_file)
		#Copy the training file into the model file, no changes
		with open(train_file) as f:
			with open(model_file, "w") as f1:
				for line in f:
					toRemoveText = line.find('.') + 5
					newLine = line.replace(line[:toRemoveText],'')
					f1.write(newLine)
			f1.close
		f.close
		return False