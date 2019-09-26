import sys
print(sys.path)
sys.path.insert(1, 'D:/Documents/UNI/WS19-20/ComputationalCreativityBlock/gpt2/src')

# import conditional_samples.py
from gpt2.src.conditional_samples import interact_model


# splits text into sentences and returns the sentence that is most desired
# output = dict
# TODO rename function
def get_candidates(text, goal_word):
    candidates = {}
    # TODO tokenize the sentences
    # similarity between current sentence and goal_word (must be updated)
    current_sim = 0.0
    # for each sentence:
    #   get similarity between it and goal word
    #   if this_sim > current_sim:
    #       candidates.append(sentence : similarity)
    # return candidates

    pass

# input = dict
def get_best_sentence(candidates, previous_sentence):
    # for each candidate:
    #   new_similarity_val = similarity between candidate and previous_sentence
    #   candidates[candidate] = (candidates[candidate], new_similarity_val)
    # final_output.append(best_sentence)
    # return candidate that is most similar to the goal_word



# input comes from reuter
inp = ""


# out = string
out = interact_model(input=inp)

# def goal_reached()

'''
while iter < MAX_ITER:
    if best sentence contains goal_word:
        return final_output
    if best_sentence is > n similar to goal_word:
        return final_output
    interact_model(input=best_sentence)
    iter =+ 1
    
return final_output

'''

get_candidates(out)