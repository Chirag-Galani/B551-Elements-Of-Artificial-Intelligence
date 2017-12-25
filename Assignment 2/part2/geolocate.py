#!/usr/bin/python
#!/usr/local/bin/python3
# cat tweets.test1.txt | tr '\200-\377' '*' | tr '\r' ' '   > tweets.test1.clean.txt
# cat tweets.train.txt | tr '\200-\377' '*' | tr '\r' ' '   > tweets.train.clean.txt
import re
import math
import sys
##from nltk.corpus import stopwords

##----------------------------------------------------------Citation----------------------------------------------------------------
## cite : https://monkeylearn.com/blog/practical-explanation-naive-bayes-classifier/
#  We have taken the logic to solve this problem from above given URL. 
#
#  -------------------------------------------*********Description***********--------------------------------------------------------
# We tried implementing Multinomial Naive Bayes. The multinomial naive Bayes model is typically used for discrete counts. 
# To accomplish this, we have first cleaned the training data from all the non-ASCII values. After cleaning the data, separated
# the location name from the tweet and stored it into different list. We have mantained two different list to store location and tweet seperately.
#  
# Created two matrix, frequency and probability. First columns of this matrix consists of all the unique words from the training data
# and its first column consists of all the unique location of training data.
# Frequency matrix stores the number of times each word has appeared in a location.
# Probability matrix stored the probability of each word for that specific location.
#
# Probability of a word = (frequency of that word for that specific location + 1) / (total no. of word in that location + total number of uinque word in tweet)
# We have done Laplace smoothing to handle those words which doesn't appear in training file but are present in test file. To handle,
# this we are adding one into the numerator. e.x(frequency of that word for that specific location + 1)
#  
# We have cleaned the test data by removing all non ASCII values then removed all the stop words.
# And then calculated total probability of each tweet for every location present in given Test data.
#
# 
# Printed top 5 words in each location by calling returnListWord.


training_file= sys.argv[1] 
testing_file= sys.argv[2] 
output_file= sys.argv[3] 

##To remove non ascii values from the training file
def removeNonAscii(string):
    nonascii = bytearray(range(0x80, 0x100))
    return string.translate(None, nonascii)

##To eliminates stopwords from the given training file
def eliminateStopWords(word_list):
    noset = {'ourselves', 'hers', 'between', 'yourself', 'but', 'again', 'there', 'about', 'once', 'during', 'out',
             'very',
             'having', 'with', 'they', 'own', 'an', 'be', 'some', 'for', 'do', 'its', 'yours', 'such', 'into', 'of',
             'most',
             'itself', 'other', 'off', 'is', 's', 'am', 'or', 'who', 'as', 'from', 'him', 'each', 'the', 'themselves',
             'until',
             'below', 'are', 'we', 'these', 'your', 'his', 'through', 'don', 'nor', 'me', 'were', 'her', 'more',
             'himself',
             'this', 'down', 'should', 'our', 'their', 'while', 'above', 'both', 'up', 'to', 'ours', 'had', 'she',
             'all', 'no',
             'when', 'at', 'any', 'before', 'them', 'same', 'and', 'been', 'have', 'in', 'will', 'on', 'does',
             'yourselves',
             'then', 'that', 'because', 'what', 'over', 'why', 'so', 'can', 'did', 'not', 'now', 'under', 'he', 'you',
             'herself', 'has', 'just', 'where', 'too', 'only', 'myself', 'which', 'those', 'i', 'after', 'few', 'whom',
             't',
             'being', 'if', 'theirs', 'my', 'against', 'a', 'by', 'doing', 'it', 'how', 'further', 'was', 'here',
             'than'}

    # print "Old list=" + str(word_list)
    filtered_words = [word for word in word_list if word not in noset]
    # print "New List=" + str(filtered_words)
    return filtered_words

##Cleanising of training file from non-Ascii 
in_file = open( training_file, "rt")  # open file lorem.txt for reading text data
contents = in_file.read()  # read the entire file into a string variable
in_file.close()  # close the file
# contents = contents.encode('ascii',errors='ignore').decode()
contents = removeNonAscii(contents)
contents = re.sub(r"([a-z])\-([a-z])", r"\1 \2", contents, 0, re.IGNORECASE)


contents = contents.rstrip().strip() ##space removal from each line
contArr = contents.splitlines()
newList = []
j = 0
for i in range(len(contArr)):
    try:
        contArr[i].index(",_")             ##identify the location in each tweet
        newList.insert(j, contArr[i])
        j += 1

    except:
        newList[j - 1] = newList[j - 1] + " " + contArr[i] ## If location name not found then merge the line to previous line 

location_list = [] ##stores all the location from training data
tweet_list = [] ## list containing each tweets  of every location from training data 
i = 0
for x in newList:
    try:
        i += 1
        seperator_index = x.index(" ")
        # #print seperator_index
        location_list.append(x[:(seperator_index)])
        tweet_list.append(x[(seperator_index + 1):])
        if x[:seperator_index] == "#amazing":
            print("#amazing Error at val=" + x + " at " + str(i))
    except ValueError:
        # print("Error at "+i)
        print("Error at val=" + x + " at " + str(i))

new_tweet_list = []
unique_loc_set = set(location_list)

no_punc_word_array_list = []
unique_word_set = set() ##has unique loctaion of training data
all_word_list = [] ## all the tweet words of loaction data

##removal of punctuation from training data set
punc = set(":+\"()[],./;'?-_!@#1234567890*\\")
for line in tweet_list:
    strp = ''.join(c for c in line if not c in punc)
    words = strp.lower().split()
    for current_word in words:
        unique_word_set.add(current_word)
        all_word_list.append(current_word)
    no_punc_word_array_list.append(words)
# #print no_punc_word_array_list

b = []
b = list(unique_loc_set) ##  has unique location of training data
count = 1

row = len(unique_word_set)
col = len(unique_loc_set)
##created frequency and probability matrix structure
frequency_matrix = [[0 for x in range(col + 2)] for y in range(row + 2)]
probablity_matrix = [[0 for x in range(col + 1)] for y in range(row + 2)]

##Add all the location gathered from training file into loc_dict location dictionary
loc_dict = dict()
for item in unique_loc_set:
    # e = next(iter(unique_loc_set))
    frequency_matrix[0][count] = item
    probablity_matrix[0][count] = item
    loc_dict[item] = count
    count += 1
frequency_matrix[0][count] = "Total"
frequency_matrix[(len(unique_word_set) + 1)][0] = "Total"

##Loc_count stored the number of times a location has repeated in the training file 
loc_count = dict()
for item in location_list:
    if (item in loc_count):
        loc_count[item] += 1
    else:
        loc_count[item] = 1


count = 1
uw_dict = dict()
for item in unique_word_set:
    frequency_matrix[count][0] = item
    probablity_matrix[count][0] = item
    uw_dict[item] = count 
    count += 1


##frequency_matrix contains the frequency of a word repeated under each location
count = 0
for sentenceArray in no_punc_word_array_list:
    loc = location_list[count]
    for word in sentenceArray:
        frequency_matrix[uw_dict[word]][loc_dict[loc]] += 1
    count += 1

xLastIndex = len(frequency_matrix) - 1
yLastIndex = len(frequency_matrix[0]) - 1

totalRowSum = 0
totalColSum = 0

# Calculates total of row 
for x in range(1, len(frequency_matrix)):
    totalRowSum = 0
    for y in range(1, len(frequency_matrix[0])):
        totalRowSum += frequency_matrix[x][y]
        # #print "frequency_matrix["+str(x)+"]["+str(y)+"] =" + str(frequency_matrix[x][y])
    frequency_matrix[x][len(frequency_matrix[0]) - 1] = totalRowSum

# Calculate total of column i.e.total number of word in each location
for y in range(1, len(frequency_matrix[0])):
    totalColSum = 0
    for x in range(1, len(frequency_matrix) - 1):
        totalColSum += frequency_matrix[x][y]
    # #print 'totalColSum for '+str(y)+" = "+str(totalColSum)
    frequency_matrix[len(frequency_matrix) - 1][y] = totalColSum

##calculation of probability matrix
for i in range(1, len(frequency_matrix)):
    for j in range(1, len(unique_loc_set) + 1):
        # #print  frequency_matrix[i+1][j],frequency_matrix[len(frequency_matrix)-1][j]
        a = frequency_matrix[i][j]  ##no. of times a word has repeat in a location
        b = frequency_matrix[len(frequency_matrix) - 1][j]  ##total of word in that sepcific location
        c = len(unique_word_set)  ##all the unique words
        #d = loc_count[frequency_matrix[0][j]]  ##no. of times a location has repeated
        #e = len(location_list)  ##all the location

        probablity_matrix[i][j] = -(math.log(((a + 1) / float(b + c)))) # * (d / float(e))))
#print probablity_matrix

## Opening and cleansing of test file
in_file = open(testing_file, "rt")  # open file lorem.txt for reading text data
test_data = in_file.read()  # read the entire file into a string variable
in_file.close()

test_data = removeNonAscii(test_data)

#test_data = re.sub("\-([a-zA-Z]+)", r"\1", test_data)
test_data = re.sub(r"([a-z])\-([a-z])", r"\1 \2", test_data, 0, re.IGNORECASE)

##seperation of location with the tweet in test file
test_data = test_data.rstrip().strip()
tempArr = test_data.splitlines()
testlist = []
j = 0
for i in range(len(tempArr)):
    try:
        tempArr[i].index(",_")
        testlist.insert(j, tempArr[i])
        j += 1
    except:
        testlist[j - 1] = testlist[j - 1] + " " + tempArr[i]

locationTest_list = []
tweetTest_list = []
i = 0
for x in testlist:
    try:
        i += 1
        seperator_index = x.index(" ")
        locationTest_list.append(x[:(seperator_index)])
        tweetTest_list.append(x[(seperator_index + 1):])
    except ValueError:
        
        locationTest_list.append(x)
        tweetTest_list.append(" ")
    
new_tweet_list_test = []
unique_loc_set_test = set(location_list)

no_punc_word_array_list_test = []
unique_word_set_test = set()
all_word_list_test = []

##cleansing of test data
punc = set(":+\"()[],./;'?-_!@#1234567890*\\")
for line in tweetTest_list:
    strp = ''.join(c for c in line if not c in punc)
    words = strp.lower().split()
    for current_word in words:
        unique_word_set_test.add(current_word)
        all_word_list_test.append(current_word)
    no_punc_word_array_list_test.append(words)


# print no_punc_word_array_list_test

def printDict(d):
    for i in d:
        print d[i], i


f = open(output_file,"w")


for i in range(len(no_punc_word_array_list_test)):
    no_punc_word_array_list_test[i]= eliminateStopWords(no_punc_word_array_list_test[i])

## Calculate the total probability value for all the words in the test file 
for i in range(len(no_punc_word_array_list_test)):
    temp_test_prod_dict = dict()
    for k in range(1, len(unique_loc_set) + 1):
        prod_prob_per_tweet = 1
        # #print "len(unique_loc_set) + 1="+str(len(unique_loc_set) + 1)
        for j in range(len(no_punc_word_array_list_test[i])):
            word = no_punc_word_array_list_test[i][j]
            # #print word
            try:
                index_probablity_of_word = uw_dict[word]
            except:
                KeyError
                index_probablity_of_word = -1
            if index_probablity_of_word != -1:
                total = probablity_matrix[index_probablity_of_word][k]
                prod_prob_per_tweet *= total
            else:
                a = 0
                b = frequency_matrix[len(frequency_matrix) - 1][k]  ##total of word in that sepcific location
                c = len(unique_word_set)  ##all the unique words
                d = loc_count[frequency_matrix[0][k]]  ##no. of times a location has repeated
                e = len(location_list)  ##all the location
                total = -(math.log(((a + 1) / float(b + c)) * (d / float(e))))
                # #print " ELSE CASE Total of '"+ word+ "' in region "+frequency_matrix[0][k] +" ="+str(total)
                prod_prob_per_tweet *= total
        temp_test_prod_dict[frequency_matrix[0][k]] = prod_prob_per_tweet
    max_value = min(temp_test_prod_dict.values())
    result = [key for key, value in temp_test_prod_dict.iteritems() if value == max_value]
    # #print "suggested elem ="+str(result)
    line = ""
    for word in no_punc_word_array_list_test[i]:
        line += " " + word
    #print "---------------------------"
    # print "****" + line + "*****"
    #print result[0]
    f.write(result[0]+',  '+locationTest_list[i]+ ',  '+tweetTest_list[i]+'\n') ## write into the output file with following format : 
                                                                                ## estimated_location, actual_location , tweets from test file
##printed top 5 words for each location
def returnListWord(score_top_5_wordlist, y):

    final_word_list=[]
    for o in range(len(score_top_5_wordlist)) :
        for x in range(1,(len(frequency_matrix)-1)):
            if score_top_5_wordlist[o] == frequency_matrix[x][y]:
                # print frequency_matrix[x][0]
                final_word_list.insert(len(final_word_list),frequency_matrix[x][0])
            if (len(final_word_list)>=5):
                return final_word_list


temp_list=[]
unique_top_5_wordlist=[]
score_top_5_wordlist=[]
num = 5



for y in range(1, (len(frequency_matrix[0]) - 1)):
    temp_list=[]
    for x in range(1, (len(frequency_matrix)) - 1):
        temp_list.append(frequency_matrix[x][y])
    # score_top_5_wordlist=frequency_matrix[0][y]+str(temp_list)
    score_top_5_wordlist=(sorted(temp_list, reverse=True)[:num])
    # print "For "+frequency_matrix[0][y]
    # print "For "+frequency_matrix[0][y]+str(score_top_5_wordlist)
    print frequency_matrix[0][y]+" = "+str(returnListWord(score_top_5_wordlist,y))


