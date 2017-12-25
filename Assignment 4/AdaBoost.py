#!/usr/bin/env python
'''
#
# The adaboost classifier, is a supervised learning classifier, which uses the cumulative impact of a variety of weak classifiers, which were trained using the training data,
# to classify the test-data set w.r.t. the problem at hand. The main impact of this algorithm is that while training, for a set of weak classifiers the error's made by one classifier are 
# more important for the subsequent classifiers to classify.
#
# Problem : We have been given a train data set which contains the correct orientations of around 36000 images, using this we have to train our program.
#		    We then have to predict/assign an orientation for the images in the test-data set
#
# Formulation : We defined the weak classifier are a comparision between the color values for 2 randomly selected pixels. We utilize a defined subset of the entire training data for training
#				each of the weak classifiers. Once training is completed, we use the weak classifier data stored in the model file to evaluate the closest orientation for the test-data, which is then assigned to it.
#				This results into a much smaller model_file, which takes much less time for test-data classification. For this problem we have done a one-against-many comparision for creating the model.
#				We check if the training data can be classified as 0 orientation or otherwise or 90 or otherwiste, etc.
#
# Citation : 1. Discussed with Kushal Giri.
#			 2. General understanding of Adaboost : 
#				http://rob.schapire.net/papers/explaining-adaboost.pdf
#			 3. Understanding the weight re-calculation and alpha calculation: 
#				http://mccormickml.com/2013/12/13/adaboost-tutorial/
#
# Code-Descrption : The class file present here is called from orient.py based on the input provided
#
#					Training:
#					orient.py train train_file.txt mddel_file.txt adaboost
#					The above calls the class in training mode, in which we select a subset of the entire training data (1000 in our case),for each of the weak classifiers, we have used 250 in this instance.
#					On the basis of the weak classifiers choice (if first random pixel value > second random pixel value), we classify the entire subset on the basis of this, for each of the available orientation values
#					We then compute the error rate and an alpha (estimated orientation) for each of the classifier. We write into the model file for each weak classifier the following, which represents the weak classifier
#					first random pixel value, second random pixel value, color selected, orientation, alpha.
#					We have also computed weights for each classifier, which is impacted by the error rate, this ensures that the wrongly classified values of a previous classifier are more likely to be picked up by the next for
#					its training. We ensure the weights are normalized so that everything lies inside the condition of probability, assuming that the train data is representative of the real world.
#
#					Testing:
#					orient.py test test_file.txt mddel_file.txt adaboost
#					The above calls the class in test mode, in which for each of the test-data set we run the weak classifiers, which have been written into the model_file. We run each of the classifer to get the orientation of
#					for each, if they match then we define a positive multiplier else a negative multiplier, which is multiplied with the alpha value stored. The cumulative of each of the weak classifier for the orientation 
#					is stored and we run a vote to find which of the orientation has the maximum alpha summation, which is then assigned to the test-image. The accuracy is calculated by dividing the correct classifications
#					by comparing the predicted orientation with the actual orientation and dividing it with the entire test-images available.
#
#
# Problems(P), Assumptions(A), Simplifications (S), Design Decisions (DD):
#	The input file names for the model_file will be the one created by the train function of this class (A)
#	Write the data directly into the output_file or model_file instead of storing it into memory (DD)	
#	
#
# Analysis : 
#		We evaluated the implementation for varying values of classifiers used and training datasubset used, we found our accuracy going from 43.69 for 10 classifiers and 10000 training datasubset, to 64.09 for 250 classifiers and 1000 training data subste.
#		It takes around 2 minute for training and less than 1 min for testing the entire data-set.
#
#			classifier 	|  DataSubset 	|     Accuracy     |
#      -------------------------------------------------------
#			10			|	1000		|		50.15	   | 
#			10			|	10000		|		43.69	   | 
#			10			|	30000		|		55.18	   | 
#			50			|	1000		|		62.88	   |
#			50			|	10000		|		61.22	   |
#			50			|	30000		|		62.75	   |
#			100			|	1000		|		63.3	   |
#			100			|	10000		|		62.14	   |
#			100			|	30000		|		62.46	   |
#			120			|	1000		|		60.55	   |
#			120			|	10000		|		62.88	   |
#			120			|	30000		|		61.08	   |
#			250			|	1000		|		64.05	   |
#			250			|	10000		|		63.52	   |
#			250			|	30000		|		63.63	   |
#	 ---------------------------------------------------------
'''
import Queue as Q
import os
import math
import numpy as np
import random
import copy

class ADABoost:
	def __init__(self):
		self.classifierQuant = 250
		self.classfifierSize = 1000
		self.orientations = [0,90,180,270]

	def train(self,train_file,model_file):
		if os.path.isfile(model_file):
			os.remove(model_file)		
		tf=open(train_file,'r')
		pixel_colors=[[],[],[]]
		trainOrientation=[]
		for row in tf:
			pixel_colors[0]+=[[int(line) for line in row.split()[2::3]]]
			pixel_colors[1]+=[[int(line) for line in row.split()[3::3]]]
			pixel_colors[2]+=[[int(line) for line in row.split()[4::3]]]
			trainOrientation+=[int(row.split()[1])]
		pixel=np.array((pixel_colors))
		pixel[0]=np.array(pixel_colors[0])
		pixel[1]=np.array(pixel_colors[1])
		pixel[2]=np.array(pixel_colors[2])
		trainOrientLabel=np.array(trainOrientation)
		for j in range(len(self.orientations)):
			classifiersUsed=0
			bool_label=trainOrientLabel==self.orientations[j]
			inst_weight=1.0/len(pixel[0])*np.ones((len(pixel[0]))) #Initializing the weights for each new orientation			
			while classifiersUsed<=self.classifierQuant:
				[randomPixel1,randomPixel2]=random.sample(range(0,63),2)  #Randomly selecting two pixels
				randomColor=random.randint(0,2)   #Randomly selecting color
				pixelSubset=np.unique(np.random.choice(len(pixel[0]),self.classfifierSize,list(inst_weight))) #Create a subset of the train data, considering the weights assigned to each
				valuedDecisionTrueMatch=pixelSubset[np.where(pixel[randomColor][pixelSubset,randomPixel1]>pixel[randomColor][pixelSubset,randomPixel2])] #Evaluate the decision of the pixel1 being greater than pixel 2
				valuedDecisionFalseMatch=pixelSubset[np.where(pixel[randomColor][pixelSubset,randomPixel1]<=pixel[randomColor][pixelSubset,randomPixel2])]
				allTruth=np.argmax(np.bincount(bool_label[valuedDecisionTrueMatch]))
				falseMatchIndex=valuedDecisionFalseMatch[np.where(bool_label[valuedDecisionFalseMatch]==(allTruth+1)%2)] #Not the current orientation
				truthMatchIndex=valuedDecisionTrueMatch[np.where(bool_label[valuedDecisionTrueMatch]==allTruth)] #he current orientation
				errorRate=1-float(len(falseMatchIndex)+len(truthMatchIndex))/len(pixelSubset) #Evaluate error
				inst_weight[falseMatchIndex]*=errorRate/(1-errorRate) #Revaluate the weights
				inst_weight[truthMatchIndex]*=errorRate/(1-errorRate)
				inst_weight=inst_weight/float(np.sum(inst_weight)) #Normalize the weights
				alpha=0.5*math.log((1-errorRate)/errorRate) #Evaluate alpha
				#Writing into the model file
				with open(model_file,'a') as mf:
					mf.write('%s\n'%[randomPixel1,randomPixel2,randomColor,self.orientations[j],alpha])
					mf.close
				classifiersUsed+=1
		return False

	def test(self,model_file,test_file,output_file):
		if os.path.isfile(output_file):
			os.remove(output_file)			
		ttf=open(test_file,'r')
		modelValuesList=[]
		with open(model_file,'r') as model_file:
			modelValuesList=[eval(line.rstrip('\n')) for line in model_file]
		testPixels=[[],[],[]]
		actualOrientation=[]
		image_name=[]
		c = self.classifierQuant
		for row in ttf:
			testPixels[0]+=[[int(line) for line in row.split()[2::3]]]
			testPixels[1]+=[[int(line) for line in row.split()[3::3]]]
			testPixels[2]+=[[int(line) for line in row.split()[4::3]]]
			actualOrientation+=[int(row.split()[1])]
			image_name+=[row.split()[0]]
		counter=0
		for i in range(len(testPixels[0])):
			votes=np.zeros((4))
			for j in range(c):
				for k in range(4):
					if testPixels[modelValuesList[j+c*k][2]][i][modelValuesList[j+c*k][0]]>testPixels[modelValuesList[j+c*k][2]][i][modelValuesList[j+c*k][1]]:
						votes[k]-=modelValuesList[j+c*k][4]
					else:
						votes[k]+=modelValuesList[j+c*k][4]
		    #Predicted output by taking a weighted vote of all the weak classifiers
			predicted=self.orientations[np.argmax(votes)]
			if predicted==actualOrientation[i]:
				counter+=1
			with open(output_file,'a') as outf:
				outf.write('%s %s\n'%(image_name[i],predicted))
				outf.close
		print 'Accuracy: ',float(counter)*100/len(testPixels[0])
		return False