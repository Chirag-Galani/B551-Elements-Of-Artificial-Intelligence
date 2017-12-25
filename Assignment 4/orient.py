#!/usr/bin/env python
'''
#
#
# Problem : We have been given a train data set which contains the correct orientations of around 36000 images, using this we have to train our program.
#           We then have to predict/assign an orientation for the images in the test-data set
#
# For the purpose of our work, the best algorithm is neural networks
# It gives us a good level of accuracy with high rate of classification, knn also gives us a good classification but the speed is low
#
# For description and analysis of each algorithm please refer to their respective modules.
# KNN.py : k nearest neighbors
# Adaboost.py : Adaboost
# NNet.py : Nerual networks
#
#
'''
import sys
import Queue as Q
import os
import math
import numpy as np
from KNN import KNN
from AdaBoost import ADABoost
from NNet import NNet


output_file = "output.txt"
test_train = str(sys.argv[1])
tt_file = str(sys.argv[2])
model_file = str(sys.argv[3])
model = str(sys.argv[4])

if model == "nearest":
	algo = KNN()
if model == "adaboost":
	algo = ADABoost()
if model == "nnet" or model == "best":
	algo = NNet()
if test_train == "train":
	algo.train(tt_file,model_file)
else:
	algo.test(model_file,tt_file,output_file)
