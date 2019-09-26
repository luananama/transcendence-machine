from nltk.corpus import reuters
import mpu

import nltk
import re
from nltk.tokenize import sent_tokenize

# call the dictionary
word_dictionary = mpu.io.read('word_dictionary.pickle')

# in the dictionary, we are looking for the input word and get the text_id
def search(input_word, word_dictionary):
    txt_id = 0
    for k in word_dictionary:
        if k ==  input_word:
            txt_id = word_dictionary[k]
            return txt_id
    return txt_id


#sample_sentences = []

input_word = input("Enter a starting word: ")
#print(input_word)

# this is the text found, that matches our input word
text_found = reuters.raw(search(input_word, word_dictionary))
#print the text text_found
#print(text_found)

# text to list transformation
# tokenize the input sentence to a list

text_2sents = sent_tokenize(text_found)
#print([s.strip('\\n') for s in text_2sents])

###TODO PSBL try to remove the /n or make the headline own entry
###Randomisation, so that we get different texts

#pick the sentence that matches, and prints it
matching_sents = [s for s in text_2sents if input_word in s]
print(matching_sents[0])

#now search for the sentece in the list
