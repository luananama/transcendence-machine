
steps = [] #array that tracks which weight-index was chosen in each iteration during one session

weight_probs = pickle.load(weight_probs.pickle) #get the learned probabilites as an array

def set_weight_probs(itr, index, feedback): #adjusts the value of weights in one iteration acoording to feedback
    
    feedback = feedback*0.1 #if user input between -10 and + 10
    #add feedback-value to the weight that was selected in the given iteration
    weight_probs[itr][index] += feedback
    
    #adjust the other 9 values in this iteration so that we get a total probability of 1 again
    for i in range(len(weight_probs[itr])):
        if not i == index:
            weight_probs[itr][i] -= (feedback/9)



def apply_feedback(feedback): #iterates over the steps taken in every iteration of the last session and calls set_weight_probs(feedback) on each
    
    for i in range(len(steps)):
        set_weight_probs(i, steps[i], feedback)
    pickle.write(weight_probs)

def choose_weights(itr): #choses a weight between 0.1 and 0.9 for the similarity to the goal by taking the learned probabilites for this iteration into account

    goal_weight_array = [0,1,2,3,4,5,6,7,8]

    chosen_index = np.random.choice(goal_weight_array, 1, weight_probs[itr])
    steps.append(chosen_index)
    chosen_goal_weight = (chosen_index*0.1)+0.1   
    current_sentence_weight = 1-chosen_goal_weight

    return chosen_goal_weight,current_sentence_weight

# from nltk.corpus import reuters
# import mpu
#
# # in this dictionary we are iterating through the categories of the reuters corpus of nltk
# word_dictionary = {}
#
#
# for category in reuters.categories():
#     for document in reuters.fileids(category):
#         for word in reuters.words(document):
#             if word not in word_dictionary:
#                 word_dictionary[word] = [document]
#             else:
#                 word_dictionary[word].append(document)
#
# mpu.io.write('word_dictionary.pickle', word_dictionary)

