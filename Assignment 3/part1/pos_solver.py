###################################
# CS B551 Fall 2017, Assignment #3
#
# Your names and user ids: Shreejith Panicker (skpanick), Chirag Galani (cgalani), Khushboo Sah (sahk)
#
# (Based on skeleton code by D. Crandall)
#
#
####
# Put your report here!!
# Report
# The problem at hand is to tag each word of a given sentece with its Part of Speech(POS).
# For this problem we have considered the following parts of speech
# ADJ (adjective),ADV (adverb), ADP (adposition), 
# CONJ (conjunction), DET (determiner), NOUN, 
# NUM (number), PRON(pronoun), PRT (particle), 
# VERB, X (foreign word), and . (punctuation mark).
# 
# What we are tasked to do is to determine by using trained knowledge the pos for a given word.
# This can be seen as a Hidden Markov Model (HMM), the pos being the Markov chain (which have a logical transition from one to next) and the words being the observation (which seem to be randomly observed).
# 
# We have used three methods to do this, in order to show their implementation for a HMM and salient differences.
# 1. Simplified : We determine the pos for a word using only the probability of that word's association with a pos. 
# Implemented as a simple maximization of each word-pos asspociation
# 2. Variable elimination: We determine the pos of the word as being the one with the maximum probability for that word summing over all the possibilities for the other words.
# Implemented it by determining all variations of previous word-pos association and transition association for a given word-pos association.
# Maximum for each determined using the above is tagged to the word
# 3. Viterbi algorith (Maximum Apriori MAP) : viterbi is a bit special it determines the pos on the basis of the sequence of pos which have the maximum likelihood given the words.
# Run through the entire sentence calculating probabilities for each word-pos based on the maximum word-pos association * transition of the previous word to the current word.
# Calculated this till the last word, determined the max for the last word and back-tracked using recursion to the first word, chaining the pos which provided the next maximum value.
#
#   Emission : Count the number of associations of a word-pos and then divide by the count of the pos eg: P(dog-noun) = c(dog-noun) / c(noun)
#   Transition : Count the number of transitions of pos-pos and then divide by the count of the second pos eg: P(noun-verb) = c(noun-verb) / c(noun)
#   Initial : Count of number of pos associated with the first word of each sentence then divide by the number of sentences eg: P(first.noun) = c(first.noun) / c(sentences)
# 
# I believe viterbi is the best as it allows for corrections of previous word-pos associations based on the maximum determined in the end.
# The second best being variable elimination as we trying to determine the maximum probability for a word-pos association given that we have calculated all the other words-pos associations.
# But, given that on the test dataset (bc.test), they are giving such close answers when it comes to percentage of word correct, I believe the simplified implementation cannot just be discarded, as being the worst.
# The simplfied has the advantage of having the least amount of computation work.
# 
# Additionally, you have asked us to determine the posterior of the outputs of each algorithm (As per the discussion with Prof. Crandall, we need to use the simplified for calculations of the posterior)
# I have calculated it as asked
# Posterior  = Likelihood * Prior [We don't consider the division by evidence as per requirement]
# Likelihood is determined as the probability of the word bein that pos
# Prior is the probability of that pos
# Both of these are determined from thhe training dataset.
# 
# Assumptions (A), Design Decisions (DD), Problems (P)
# The training dataset is sufficient to train the model (A)
# The intermediate values slipped off the maximum range which python can handle (P)
# Took the logs of the values to ensure they remained in calculable and comparable realms (DD)
# Took a global minimum in case a particular associatio, transition or emission was not found (DD)
# 
# We discussed general strategies for this problem with "aybhimdi-mehtau-vsriniv" group
###

import random
import math
import copy
#import copy

# We've set up a suggested code structure, but feel free to change it. Just
# make sure your code still works with the label.py and pos_scorer.py code
# that we've supplied.
#
class Solver:

    # Calculate the log of the posterior probability of a given sentence
    #  with a given part-of-speech labeling
    def posterior(self, sentence, label):
        TotPosteriorProbab = 1.0
        for i in range(0,len(sentence)):
            wordPos = ""
            word = sentence[i]
            pos = label[i]
            wordPos = word + pos
            if self.emission_probab.has_key(wordPos):
                Likelihood = self.emission_probab[wordPos]
            else:
                Likelihood = 1.0
            if self.PosProbab.has_key(pos):
                priorProbab = self.PosProbab[pos]
            else:
                priorProbab = 1.0
            TotPosteriorProbab = TotPosteriorProbab * (Likelihood * priorProbab)
        return math.log(TotPosteriorProbab)
    #def posterior(self, sentence, label):
    #    print sentence
    #    print label
    #    return 0

    # Do the training!
    #
#    def train(self, data):
#        pass
    def train(self, data):
        self.first_pos_count = dict() #count of initial pos
        self.emission_count = dict() #count of word-pos associations
        self.transition_count = dict() #count of pos-pos transitions
        self.POSCount = dict() #count of each pos
        self.WordCount = dict() #counnt of each word
        for i in data:
            cur_word_set = i[0]
            cur_pos_set =  i[1]
            for j in range (0,len(cur_word_set)):
                if j != 0:
                    prev_word = cur_word
                    prev_pos = cur_pos
                    cur_word = cur_word_set[j]
                    cur_pos = cur_pos_set[j]                
                    transition_var = prev_pos + cur_pos
                    if self.transition_count.has_key(transition_var):
                        self.transition_count[transition_var]+=1.0
                    else:
                        self.transition_count.update({transition_var:1.0})                
                else:
                    cur_word = cur_word_set[j]
                    cur_pos = cur_pos_set[j]                
                    if self.first_pos_count.has_key(cur_pos):
                        self.first_pos_count[cur_pos_set[j]]+=1.0
                    else:
                        self.first_pos_count.update({cur_pos:1.0})
                emission_var = cur_word + cur_pos
                if self.emission_count.has_key(emission_var):
                    self.emission_count[emission_var]+=1.0
                else:
                    self.emission_count.update({emission_var:1.0})

                if self.POSCount.has_key(cur_pos):
                    self.POSCount[cur_pos]+=1.0
                else:
                    self.POSCount.update({cur_pos:1.0})                    
        #Calculating Emission Probability
        self.emission_probab = copy.deepcopy(self.emission_count)
        for pos in self.POSCount.keys():
            for wordPos in list(k for k,v in self.emission_probab.iteritems() if pos in k.lower()):
                self.emission_probab[wordPos] = self.emission_probab[wordPos] / self.POSCount[pos]
        #Calculating Transition Probability
        self.transition_probab = copy.deepcopy(self.transition_count)
        for pos in self.POSCount.keys():
            for wordPos in list(k for k,v in self.transition_probab.iteritems() if pos == k[-len(pos):].lower()):
                self.transition_probab[wordPos] = self.transition_probab[wordPos] / self.POSCount[pos]
        #Calculating First POS Probability
        self.first_pos_probab = copy.deepcopy(self.first_pos_count)
        self.first_pos_probab = {k: v / total for total in (sum(self.first_pos_probab.itervalues(), 0.0),) for k, v in self.first_pos_probab.iteritems()}
        #Calculating the POS probab
        self.PosProbab = copy.deepcopy(self.POSCount)
        self.PosProbab = {k: v / total for total in (sum(self.PosProbab.itervalues(), 0.0),) for k, v in self.PosProbab.iteritems()}
        minList = []
        minList.append(min(self.first_pos_probab.itervalues()))
        minList.append(min(self.transition_probab.itervalues()))
        minList.append(min(self.emission_probab.itervalues()))
        self.globalMin = min(minList) * 0.01 #determining a global minimum for calculations
        return False

    # Functions for each algorithm.
    #
    #def simplified(self, sentence):
    #    return [ "noun" ] * len(sentence)
    def simplified(self, sentence):
        posSentence = list()
        for word in sentence:
            wordPos = ""
            maxProb = 0.0
            for pos in self.POSCount.keys():
                checkKey = word+pos
                if self.emission_probab.has_key(checkKey):
                    Likelihood = self.emission_probab[checkKey]
                else:
                    Likelihood = self.globalMin * 0.01
                curPosProbab = Likelihood 
                if maxProb < curPosProbab:
                    maxProb = curPosProbab
                    wordPos = pos
            posSentence.append(wordPos)
        return posSentence

    #def hmm_ve(self, sentence):
    #    return [ "noun" ] * len(sentence)
    def hmm_ve(self, sentence):
        posAll = list(self.POSCount.keys())
        smallestVal = self.globalMin * 0.01
        posSentence = []
        prevProbab = []
        for i in range(0,len(sentence)):
            j = 0
            maxProb = 0
            Word = sentence[i]
            for pos in posAll:
                WordPos = Word + pos
                if self.emission_probab.has_key(WordPos):
                    probabWordPos = self.emission_probab[WordPos]
                else:
                    probabWordPos = smallestVal
                if i == 0:
                    if self.first_pos_probab.has_key(pos):
                        probabOfFirstPos = self.first_pos_probab[pos]
                    else:
                        probabOfFirstPos = smallestVal
                    probabCurPair = probabOfFirstPos * probabWordPos
                else:
                    prevWord = sentence[i-1]
                    AddingOver = 0
                    for k in range(0,len(posAll)):
                        prevPos = posAll[k]
                        prevWordPos = prevWord + prevPos
                        PosTransitionPrev = prevPos + pos
                        if self.emission_probab.has_key(prevWordPos):
                            probabWordPosprev = self.emission_probab[prevWordPos]
                        else:
                            probabWordPosprev = smallestVal                        
                        if self.transition_probab.has_key(PosTransitionPrev):
                            transProb = self.transition_probab[PosTransitionPrev]
                        else:
                            transProb = smallestVal
                        AddingOver = AddingOver + (probabWordPosprev * transProb) 
                    probabCurPair =  AddingOver * probabWordPos
                if probabCurPair > maxProb:
                    maxProb = probabCurPair
                    ActualPos = pos
            posSentence.append(ActualPos)
            prevProbab.append(maxProb) 
        return posSentence

    #def hmm_viterbi(self, sentence):
    #    return [ "noun" ] * len(sentence)
    def iterateThruArray(self,PosArray,ProbabArray,Column,MaxRow,LastMaxPOS):
        curColumn = 0
        for i in range(Column):
            if PosArray[0][i] == LastMaxPOS:
                curColumn = i
        curMaxPos = PosArray[MaxRow][curColumn]
        if MaxRow == 1:
            ActualFirstPos = curMaxPos
            maxValFirstRow = math.log(self.globalMin)
            for i in range(0,Column):
                curVal =  ProbabArray[1][i]
                if curVal > maxValFirstRow:
                    maxValFirstRow = curVal
                    ActualFirstPos = PosArray[0][i]
            return [ActualFirstPos]
        else:
            MaxString = self.iterateThruArray(PosArray,ProbabArray,Column,MaxRow-1,curMaxPos)
        MaxString.append(LastMaxPOS)
        return MaxString

    def hmm_viterbi(self, sentence):
        posAll = list(self.POSCount.keys())
        ArrayForPOS = [["-" for i in range (len(posAll))]for j in range(len(sentence)+1)]
        for i in range(0,len(posAll)):
            ArrayForPOS[0][i] = posAll[i]
        ArrayForPOSProbabForMax = [[0.0 for i in range (len(posAll))]for j in range(len(sentence)+1)]
        smallestVal = math.log(self.globalMin)
        for i in range(0,len(sentence)):
            j = 0
            Word = sentence[i]
            for pos in posAll:
                WordPos = Word + pos
                priorProbab = math.log(self.PosProbab[pos])
                if self.emission_probab.has_key(WordPos):
                    probabWordPos = math.log(self.emission_probab[WordPos])
                else:
                    probabWordPos = smallestVal + math.log(0.1)
                if i == 0:
                    if self.first_pos_probab.has_key(pos):
                        probabOfFirstPos = math.log(self.first_pos_probab[pos])
                    else:
                        probabOfFirstPos = smallestVal + math.log(0.1)
                    ArrayForPOSProbabForMax[i+1][j] = probabWordPos + probabOfFirstPos
                else:
                    curPosVal = ArrayForPOS[0][j]
                    maxVal = smallestVal
                    prevPosActual = curPosVal
                    for cntr in range(0,len(posAll)):
                        prevPosVal = ArrayForPOS[0][cntr]
                        transitionPOS = prevPosVal + curPosVal
                        if self.transition_probab.has_key(transitionPOS):
                            transVal = math.log(self.transition_probab[transitionPOS])
                        else:
                            transVal = smallestVal - 10
                        prevPosValProbab = ArrayForPOSProbabForMax[i][cntr]
                        curVal = prevPosValProbab + transVal
                        if smallestVal > curVal:
                            smallestVal = curVal
                        if maxVal < curVal:
                            maxVal = curVal
                            prevPosActual = prevPosVal
                        ArrayForPOSProbabForMax[i+1][j] = probabWordPos + maxVal
                        ArrayForPOS[i+1][j] = prevPosActual
                j += 1
        maxString = []
        lastRowMaxCol = smallestVal + math.log(0.1)
        for i in range(0,len(posAll)):
            curVal =  ArrayForPOSProbabForMax[len(sentence)][i]
            if curVal > lastRowMaxCol:
                lastRowMaxCol = curVal
                lastRowMaxPOS = ArrayForPOS[len(sentence)][i]
                ActualLastPos = ArrayForPOS[0][i]
        if len(sentence) !=1:
            maxString = self.iterateThruArray(ArrayForPOS,ArrayForPOSProbabForMax,len(posAll),len(sentence)-1,lastRowMaxPOS)
        maxString.append(ActualLastPos)
        return maxString

    # This solve() method is called by label.py, so you should keep the interface the
    #  same, but you can change the code itself. 
    # It should return a list of part-of-speech labelings of the sentence, one
    #  part of speech per word.
    #
    def solve(self, algo, sentence):
        if algo == "Simplified":
            return self.simplified(sentence)
        elif algo == "HMM VE":
            return self.hmm_ve(sentence)
        elif algo == "HMM MAP":
            return self.hmm_viterbi(sentence)
        else:
            print "Unknown algo!"