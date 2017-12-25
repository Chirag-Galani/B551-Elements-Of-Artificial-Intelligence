#!/usr/bin/python
#
# ./ocr.py : Perform optical character recognition, usage:
#     ./ocr.py train-image-file.png train-text.txt test-image-file.png
#
# Authors: Chirag Galani, Shreejit Panicker, Khushboo Sah
# (based on skeleton code by D. Crandall, Oct 2017)
#
#Citations =======================================================================================

# Problem discussed with Akshay Naik, Umang Mehta and Praneta Paithankar
# Forward Backward: https://en.wikipedia.org/wiki/Forward%E2%80%93backward_algorithm


#Files used for training: bc.train

from PIL import Image, ImageDraw, ImageFont
import sys
import math

CHARACTER_WIDTH = 14
CHARACTER_HEIGHT = 25
#
# train_img_fname = "courier-train.png"
# train_txt_fname = "test-strings.txt"
# test_img_fname = "test-17-0.png"


#To convert strings to String of characters
def return_arr_string(aa):
    a = ""
    for x in aa:
        for y in x:
            a += str(y)
    return a

def print_arr(aa):
    a = ""
    for x in aa:
        for y in x:
            a += str(y)
        print a
        a = ""


def load_letters(fname):
    im = Image.open(fname)

    px = im.load()

    (x_size, y_size) = im.size
    result = []
    for x_beg in range(0, int(x_size / CHARACTER_WIDTH) * CHARACTER_WIDTH, CHARACTER_WIDTH):
        result += [["".join(['*' if px[x, y] < 1 else ' ' for x in range(x_beg, x_beg + CHARACTER_WIDTH)]) for y in
                    range(0, CHARACTER_HEIGHT)], ]

    return result

#If the characters ('*' or ' ') of the 2 Letters (train & test) match then multiply by 0.8 if not punish it by 0.2
def return_emission_probablity(a, b):
    pos_prob = 0.8
    prob = 1
    for i in range(len(a)):
        if a[i] != b[i]:
            prob = prob * (1 - pos_prob)
        else:
            prob = prob * pos_prob
    return prob

def load_training_letters(fname):
    TRAIN_LETTERS = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789(),.-!?\"' "
    # TRAIN_LETTERS = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789(),.-!?\"' "
    letter_images = load_letters(fname)
    return {TRAIN_LETTERS[i]: letter_images[i] for i in range(0, len(TRAIN_LETTERS))}

(train_img_fname, train_txt_fname, test_img_fname) = sys.argv[1:]
train_letters = load_training_letters(train_img_fname)
test_letters = load_letters(test_img_fname)

test_letter = [r for r in test_letters[0]]
''

# print "_____________________"
char_list_array = [[0 for x in range(2)] for y in range((len(train_letters)))]

count = 0
for z in train_letters:
    char_list_array[count][0] = z
    char_list_array[count][1] = return_arr_string(train_letters[z])
    count += 1

test_letter = [r for r in test_letters[15]]
output = ""

#For Simple we just see who among the training letters has the highest probablity
for test_letter in test_letters:

    min_letter = char_list_array[0][0]
    min_value = return_emission_probablity(return_arr_string(test_letter), return_arr_string(char_list_array[0][1]))
    for p in range(len(char_list_array)):
        up = return_emission_probablity(return_arr_string(test_letter), return_arr_string(char_list_array[p][1]))
        if min_value < up:
            min_value = up
            min_letter = char_list_array[p][0]

    output += min_letter
print "Simple: "+output

TRAIN_LETTERS = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789(),.-!?\"' "

count = 1


def read_data(fname):
    exemplars = []
    file = open(fname, 'r')
    for line in file:
        data = tuple([w for w in line.split()])
        exemplars += [(data[0::2]), ]
    return exemplars

#Clean data by removing all foreign characters and replacing ' .' with '.' to improving the transition probablity of last letter
def return_clean_data():
    train_data = read_data(train_txt_fname)
    cleaned_data = ""

    for line1 in train_data:
        strp = ""
        for line in line1:
            # TRAIN_LETTERS = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz+(),.-!?\"' "
            strp += " " + ''.join(c for c in line if c in TRAIN_LETTERS)
        strp = strp.replace(" .", ".")
        cleaned_data += strp + "\n"
    return cleaned_data.strip()


initial_freq_dict = dict()
initial_prob_no_log_dict = dict()
initial_prob_dict= dict()
total_char_dict=dict()
total_char = 0
content = return_clean_data().splitlines()


#Calculating character count as well as the characters of each letter
for line in content:
    for ch in line:
        current_val = total_char_dict.get(ch, 0)
        total_char_dict[ch]=current_val+1
        total_char += 1

#Calculating initial frequency and adding the condition  list(line)[0] == " " as some lines start with space
for line in content:
        if len(list(line))>1:
            if list(line)[0] == " ":
                ch=list(line)[1]
            else:
                ch=list(line)[0]
            current_val = initial_freq_dict.get(ch, 0)
            initial_freq_dict[ch] = current_val + 1

# print "total_char", total_char
total_initial=0
for key in initial_freq_dict:
    total_initial+=initial_freq_dict[key]

#Calculating initial probablity with and without log as Viterbi requires LOG as the value is too low
for key in initial_freq_dict:
    initial_prob_no_log_dict[key] = (float(initial_freq_dict[key]) / total_initial)
    initial_prob_dict[key] = -math.log(float(initial_freq_dict[key]) / total_initial)

#Calculating transition frequency and stroing the key as concatenation of characters
transition_freq = dict()
for line in content:
    for ch_index in range(len(line) - 1):
        current_val = transition_freq.get(line[ch_index] + line[ch_index + 1], 0)
        transition_freq[line[ch_index] + line[ch_index + 1]] = current_val + 1

transition_prob = dict()
transition_no_log_prob = dict()

#Calculation transition probablity by the first letter present
for key in transition_freq:
    minValue = total_char
    value = initial_freq_dict.get(key[0], minValue)
    transition_prob[key] = -math.log(float(transition_freq[key]) / value)
    transition_no_log_prob[key] = (float(transition_freq[key]) / total_char_dict[key[0]])

least_value = -math.log(1.0 / total_char)
least_no_log_value = (1.0 / total_char)
count = 0
total_prob_dict = dict()

temp_emission_key = dict()

#Comoyting the emission table for Variable Elimination
def pre_compute_emission(test_letters_passed):
    for i in range(len(test_letters_passed)):
        temp_emission_train_letter_dict = dict()
        for j in TRAIN_LETTERS:
            temp_emission_train_letter_dict[j] = return_emission_probablity(return_arr_string(train_letters[j]),
                                                            return_arr_string(test_letters[i]))
        temp_emission_key[i] = temp_emission_train_letter_dict


pre_compute_emission(test_letters)

alpha_dict_2 = dict()
beta_dict_2 = dict()

#Calculating the Alpha Section from start to end
def forward():
    alpha=[]
    alpha_first=dict()
    for i in range(len(test_letters)):
        alpha_current=dict()
        for train_letter in train_letters:
            if(i==0):
                prev_sum=initial_prob_no_log_dict.get(train_letter,math.pow(10,-6))
            else:
                prev_sum=0.0
                for k in train_letters:
                    prev_sum+=alpha_first[k] * transition_prob.get(k+train_letter, math.pow(10, -6))
            alpha_current[train_letter]=prev_sum*temp_emission_key[i].get(train_letter,math.pow(10,-6))
        maxi= max(alpha_current.values())
        for key, value in alpha_current.iteritems():
            alpha_current[key] = value / maxi
        alpha.append(alpha_current)
        alpha_first=alpha_current
    return alpha

#Calculating the Beta Section from end to start by initializing the last column to 1
# and initializing by considering the current column and next column (which was calculated in previous iteration)
def backward():
    backward_list = []
    previous_dict = dict()
    next_list = test_letters[::-1]
    for i in range(len(next_list)):
        letter=next_list[i]
        current_dict = dict()
        for character in train_letters:
            if i == 0:
                current_dict[character] = 1
            else:
                current_sum=0.0
                for future_letter in train_letters:
                    current_sum += previous_dict[future_letter] * temp_emission_key[i - 1].get(future_letter, math.pow(10, -6)) * transition_prob.get(character+future_letter, math.pow(10, -6))
                current_dict[character]=current_sum
        maxi= max(current_dict.values())
        for key,value in current_dict.iteritems():
            current_dict[key]= value / maxi
        backward_list.append(current_dict)
        previous_dict = current_dict
    return backward_list

#Multipling the forward & backward dictionary and selecting the index with maximum value of each column
def hmm_ve():
    fwd=forward()
    bwd=backward()
    sequence=[]
    k=len(test_letters)-1
    for i in range(len(test_letters)):
        temp_prob_dict= {character: bwd[k][character] * fwd[i][character] for character in train_letters}
        sequence.append(max(temp_prob_dict, key=temp_prob_dict.get))
        k = k- 1
    print "HMM VE "+"".join(sequence)

count = 0
total_prob_dict = dict()


#Only 2 dictionaries are used interchangably in Viterbi implementation. As the values of the previous iterations are used only in the current iteration unlike the Variable eliminiation algorithm where the whole matrix is required
def hmm_viterbi():
    first_dict = dict()
    second_dict = dict()

    op = ""
    count = 0
    test_count_var = 0
    use_first_dict_as_new = False #use_first_dict_as_new is used to decide which one to use in the next iteration
    min_trans_selected_dict = dict()
    for test_letter in test_letters:
        use_first_dict_as_new = not use_first_dict_as_new
        if (use_first_dict_as_new):
            first_dict = dict()
        else:
            second_dict = dict()
        for letter in TRAIN_LETTERS:
            emission_prob = -math.log(
                return_emission_probablity(return_arr_string(train_letters[letter]), return_arr_string(test_letter)))
            if count == 0:
                first_dict[letter] = (initial_prob_dict.get(letter, -math.log(1.0 / total_char)) + emission_prob)
            else:
                temp_combo_viterbi_dict = dict()
                for oxe in TRAIN_LETTERS:

                    transition_prob_value = transition_prob.get(oxe + letter, -math.log(1.0 / total_char))

                    temp_combo_dict_key = str(count) + str(oxe) + str(letter)
                    if use_first_dict_as_new:
                        temp_combo_viterbi_dict[temp_combo_dict_key] = (
                            transition_prob_value + emission_prob + second_dict.get(str(oxe),
                                                                                    -math.log(1.0 / total_char)))

                    else:
                        temp_combo_viterbi_dict[temp_combo_dict_key] = (
                            transition_prob_value + emission_prob + first_dict.get(str(oxe),
                                                                                   -math.log(1.0 / total_char)))

                minimum_dict_selected_key = min(temp_combo_viterbi_dict, key=temp_combo_viterbi_dict.get)
                min_trans_selected_dict[str(count) + letter] = minimum_dict_selected_key[-2]
                if use_first_dict_as_new:
                    first_dict[letter] = temp_combo_viterbi_dict[minimum_dict_selected_key]
                else:
                    second_dict[letter] = temp_combo_viterbi_dict[minimum_dict_selected_key]
        if use_first_dict_as_new:
            minimum = min(first_dict, key=first_dict.get)
        else:
            minimum = min(second_dict, key=second_dict.get)

        count += 1
        op += str(minimum)
        test_count_var += 1
    temp_count = count - 1

    final_output = minimum
    while temp_count > 0:
        minimum = min_trans_selected_dict[str(temp_count) + str(minimum)]
        temp_count -= 1
        final_output = minimum + final_output

    print "HMM MAP:"+ op


hmm_ve()
hmm_viterbi()


