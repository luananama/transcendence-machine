from nltk.corpus import reuters
import mpu

# in this dictionary we are iterating through the categories of the reuters corpus of nltk
word_dictionary = {}


for category in reuters.categories():
    for document in reuters.fileids(category):
        for word in reuters.words(document):
            word_dictionary[word] = document

mpu.io.write('word_dictionary.pickle', word_dictionary)
