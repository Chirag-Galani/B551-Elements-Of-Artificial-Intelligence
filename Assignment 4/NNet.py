#!/usr/bin/env python
'''
#
# Neural networks is a supervised learning algorithm, which utilizes neurons (which is a mathematical functions which accepts weighted values, and gives an output using an activation function) inorder to learn a problem and 
# then to evaluate and predict the outcomes for data which has not yet been seen.
#
# Problem : We have been given a train data set which contains the correct orientations of around 36000 images, using this we have to train our program.
#           We then have to predict/assign an orientation for the images in the test-data set
#
# Formulation : We utilize the pixels of the image, representing an unique feature, which is fed into the neural network, which results in a model file post training.
#               The model file contains the weights and biases which are to be fed into the input, hidden and output layer.
#               
# Citation : 1. Discussed with Zoher Kachwala, Umang Mehta, Chetan Patil and Kushal Giri.
#            2. Understanding the whole process of back propagation neural network: 
#               https://www.youtube.com/watch?v=aircAruvnKk&list=PLZHQObOWTQDNU6R1_67000Dx_ZCJB-3pi
#            3. Used as a reference to check the working of code with a small sample input and expected output data &
#               Understanding the implementation of batch gradient descent & bias matrix and also learnt about the keepdims parameter used for numpy.sum: 
#               https://www.analyticsvidhya.com/blog/2017/05/neural-network-from-scratch-in-python-and-r/
#            4. Referred for understanding the mathematical formulas and its working: 
#               1. https://mattmazur.com/2015/03/17/a-step-by-step-backpropagation-example/
#               2. http://neuralnetworksanddeeplearning.com/chap2.html
#
# Code-Descrption : The class file present here is called from orient.py based on the input provided
#
#                   NOTE: please provide extension .npz for the model file instead of .txt
#
#                   Training:
#                   orient.py train train_file.txt mddel_file.npz nearest
#                   NOTE: please provide extension .npz for the model file instead of .txt
#                   Initialize with random weights between -1 to 1, for input to hidden, hidden to output, hidden bias and output bias. This auto-corrects itself by evaluating itself against the training data via feed forward.
#                   We compute the error rate, on the basis of mis-classification, and use to reduce the error rate via back-propogation. We again update the bias and the weights. This continues for the number of iterations we 
#                   defined. We evaluate the error rate for each iteration by computing the root means square error for each iteration. Output bias is the sum of all the delta output times the learning rate, and bias hidden layer
#                   is the sum of delta of hidden layer for each image. Finally, we store the weights and bias into the model file.
#
#                   Testing:
#                   orient.py test test_file.txt mddel_file.npz nearest
#                   NOTE: please provide extension .npz for the model file instead of .txt
#                   We initialize all the weights and biases as per the model file. Then we perform feed forward to compute the predicted orientation of the test-image. We provide the accurace based on the correctly identified images
#                   over the total images.
#                   
#
# Problems(P), Assumptions(A), Simplifications (S), Design Decisions (DD):
#   Experimented with the learning rates to get better output (DD)
#   Experimented with the hidden layer to get better output (DD)   
#   Stochastic gradient descent takes a lot of time for computation (P)
#   Implemented batch gradient descent, to get better performance (DD)
#   Store the model file as a default file format supported by numpy, instead of txt (DD)
#
# Analysis : 
#   We evaluated the implementation for various values of epochs and hidden layer, with a constant learning rate of 0.0001
#   It takes approx 15 minutes for training and approx 5 mins for the test process, on the whole set.
#   We had multiple values but decided to go with the following to show our process, we came to 564 after much analysis.
#
#         hidden layer size  | epochs           |     Accuracy     |
#      ------------------------------------------------------------------
#               20           |  1000            |     69.88        |
#               20           |  2000            |     68.82        |
#               20           |  500             |     70.41        |
#               10           |  1000            |     67.97        |
#               10           |  2000            |     69.35        |
#               10           |  5000            |     66.38        |
#                8           |  1000            |     70.94        |
#                8           |  2000            |     69.03        |
#                8           |  5000            |     68.08        |
#                8           |  1500            |     68.39        |
#                8           |  6000            |     69.67        |
#                6           |  2000            |     70.837       |
#                6           |  1000            |     69.56        |
#                6           |  4377            |     71.36        |
#      ------------------------------------------------------------------
'''
import os
import numpy as np
np.warnings.filterwarnings('ignore')
class NNet:
# Variable Initialization
    def __init__(self):
        self.input_layer_size = 192
        self.hidden_layer_size = 6 #Hidden layer size
        self.output_layer_size = 4
        self.epoch_iterations = 4377 #Training iterations
        self.alpha = 0.0001 # Learning rate
        # self.epoch_iterations = 100
        self.possible_output = [0, 90, 180, 270] #Different orientation types
    
    '''
    This function returns the orientation value to output layer formats
    0
    90
    180
    270
    '''
    def returnBinForm(self,orientation):
        single_output = [0,0,0,0]
        single_output[self.possible_output.index(int(orientation))]=1
        return single_output
    
    
    # Sigmoid Function
    def sigmoid(self,xx):
        return 1 / (1 + np.exp(-xx))
    
    
    # Derivative of Sigmoid Function
    def d_sigmoid(self,xx):
        return xx * (1 - xx)
    
    #Train file needs the train_file.txt and the model file name without any file format extension 
    #as numpy saves the model in npz format'
    def train(self,trainFile, modelFile):
        input_text_size = sum(1 for line in open(trainFile))
        input_data = np.zeros(shape=(input_text_size, self.input_layer_size)) #a numpy matrix of 36976 x 192
        output_data = np.zeros(shape=(input_text_size, self.output_layer_size))
    
        i = -1
        with open(trainFile) as f:
            for line in f:
                i = i + 1
                item = line.split()
                for j in range(len(item) - 2):
                    input_data[i][j] = int(item[j + 2])
                output_data[i] = self.returnBinForm(item[1])
    
        random_start = -1
        random_end = +1
        np.random.seed(1)
        input_to_hidden = np.random.uniform(random_start, random_end, size=(self.input_layer_size, self.hidden_layer_size))
        bias_hidden_layer = np.random.uniform(random_start, random_end, size=(self.hidden_layer_size))
        hidden_to_output = np.random.uniform(random_start, random_end, size=(self.hidden_layer_size, self.output_layer_size))
        output_bias = np.random.uniform(random_start, random_end, size=(self.output_layer_size))
    
        for i in range(self.epoch_iterations + 1):
            #Feed Forward network
            hidden_layer = self.sigmoid(np.dot(input_data, input_to_hidden) + bias_hidden_layer)
            actual_output = self.sigmoid(np.dot(hidden_layer, hidden_to_output) + output_bias)
    
            #Back Propogation network
            error_value = output_data - actual_output
            delta_output = error_value * self.d_sigmoid(actual_output)
            delta_hidden_layer = np.dot(delta_output, (np.transpose(hidden_to_output))) * self.d_sigmoid(hidden_layer)
            hidden_to_output += np.dot(np.transpose(hidden_layer), delta_output) * self.alpha
            input_to_hidden += np.dot(np.transpose(input_data), delta_hidden_layer) * self.alpha
            output_bias += np.sum(delta_output, axis=0) * self.alpha
            bias_hidden_layer += np.sum(delta_hidden_layer, axis=0) * self.alpha
            RMSError= np.sum(np.square(error_value))*0.5
            #print str(i)+" RMS= "+str(RMSError)    

        np.savez_compressed(modelFile, input_to_hidden=input_to_hidden, hidden_to_output=hidden_to_output,
                            bias_hidden_layer=bias_hidden_layer, output_bias=output_bias)
    
    
    def test(self,modelFile, testFile, outputFile):
    
        #Save data to model
        test_file_lines = sum(1 for line in open(testFile))
        test_X = np.zeros(shape=(test_file_lines, self.input_layer_size))
        test_correct_orientation = np.zeros(shape=(test_file_lines))
    
        #Load data from model
        modelData = np.load(modelFile)
        input_to_hidden = modelData['input_to_hidden']
        hidden_to_output = modelData['hidden_to_output']
        bias_hidden_layer = modelData['bias_hidden_layer']
        output_bias = modelData['output_bias']
        test_label=dict()
        i = -1
        with open(testFile) as f:
            for line in f:
                i = i + 1
                x = line.split()
                for j in range(len(x) - 2):
                    test_X[i][j] = x[j + 2]
                test_correct_orientation[i] = x[1]
                test_label[i] = x[0]
    
        correct_track_counter = 0
        total_track_counter = 0
    
        if os.path.isfile(outputFile):
            os.remove(outputFile)
    
        for i_counter in range(len(test_X)):
            hidden_layer = self.sigmoid(np.dot(test_X, input_to_hidden) + bias_hidden_layer)
            actual_output = self.sigmoid(np.dot(hidden_layer, hidden_to_output) + output_bias)
            predicted_test_out = self.possible_output[np.argmax(actual_output[i_counter])]
            if predicted_test_out == int(test_correct_orientation[i_counter]):
                correct_track_counter += 1
            total_track_counter += 1
    
            with open(outputFile, 'a') as outs:
                output_line = test_label[i_counter] + " " + str(predicted_test_out) + "\n"
                outs.write(output_line)
        # print "Results = ", str(self.epoch_iterations) + " == " + str((correct_track_counter * 100.0) / len(test_X))
        print "Accuracy: " + str((correct_track_counter * 100.0) / len(test_X))
    
#    train("train-data.txt", "nnet_model")
#    test("nnet_model.npz","test-data.txt","output.txt")
