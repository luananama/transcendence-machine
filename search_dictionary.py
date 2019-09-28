# TODO:
# first sentence contains headline
# assign probabilities for the random pick
# probabilities dependend on similarity to the start



from nltk.corpus import reuters
import numpy as np
import pickle

import nltk
import re
from nltk.tokenize import sent_tokenize


#in the dictionary, we are looking for the input word and get the text_id
def search(input_word):
    # call the dictionary
    with open('word_dictionary.pickle', 'rb') as f:
        word_dictionary = pickle.load(f)
    # word_dictionary = mpu.io.read()

    txt_ids = []
    for k in word_dictionary:
        if k ==  input_word:
            txt_ids = word_dictionary[k]
            # pick a random document, that incluedes our start word
            chosen_text = reuters.raw(np.random.choice(txt_ids,1))
            # text to list transformation
            # tokenize the input sentence to a list
            text_2sents = sent_tokenize(chosen_text)
            #pick the sentence that matches, and prints it
            matching_sents = [s for s in text_2sents if input_word in s]
            #print(matching_sents[0])

            start_sent = matching_sents[0] #mby rndm it
            return start_sent

            # first sentence contains headline
            # assign probabilities for the random pick
            # probabilities dependend on similarity to the start
    return 0 #in case word wasnt in the dict
