#!/usr/bin/env python3

import fire
import json
import os
import nltk
import gensim
import numpy as np
import tensorflow as tf
from nltk import tokenize
from nltk.tokenize import RegexpTokenizer
from gpt2model import model, encoder, sample

# Mute tf WARNING messages
tf.compat.v1.logging.set_verbosity(tf.compat.v1.logging.ERROR)
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

# Load Google's pre-trained Word2Vec model.
Gmodel = gensim.models.KeyedVectors.load_word2vec_format('./GoogleNewsModel/GoogleNews-vectors-negative300.bin', binary=True)



def interact_model(raw_text,
    model_name='774M',
    seed=None,
    nsamples=1,
    batch_size=1,
    length=None,
    temperature=1,
    top_k=40,
    top_p=1,
    models_dir='gpt2model',
):
    """
    Interactively run the model
    :model_name=124M : String, which model to use
    :seed=None : Integer seed for random number generators, fix seed to reproduce
     results
    :nsamples=1 : Number of samples to return total
    :batch_size=1 : Number of batches (only affects speed/memory).  Must divide nsamples.
    :length=None : Number of tokens in generated text, if None (default), is
     determined by model hyperparameters
    :temperature=1 : Float value controlling randomness in boltzmann
     distribution. Lower temperature results in less random completions. As the
     temperature approaches zero, the model will become deterministic and
     repetitive. Higher temperature results in more random completions.
    :top_k=0 : Integer value controlling diversity. 1 means only 1 word is
     considered for each step (token), resulting in deterministic completions,
     while 40 means 40 words are considered at each step. 0 (default) is a
     special setting meaning no restrictions. 40 generally is a good value.
     :models_dir : path to parent folder containing model subfolders
     (i.e. contains the <model_name> folder)
    """
    models_dir = os.path.expanduser(os.path.expandvars(models_dir))
    if batch_size is None:
        batch_size = 1
    assert nsamples % batch_size == 0

    enc = encoder.get_encoder(model_name, models_dir)
    hparams = model.default_hparams()
    with open(os.path.join(models_dir, model_name, 'hparams.json')) as f:
        hparams.override_from_dict(json.load(f))

    if length is None:
        length = hparams.n_ctx // 2
    elif length > hparams.n_ctx:
        raise ValueError("Can't get samples longer than window size: %s" % hparams.n_ctx)

    options = tf.GPUOptions(allow_growth = True)


    with tf.Session(graph=tf.Graph()) as sess:
        context = tf.placeholder(tf.int32, [batch_size, None])
        np.random.seed(seed)
        tf.set_random_seed(seed)
        output = sample.sample_sequence(
            hparams=hparams, length=length,
            context=context,
            batch_size=batch_size,
            temperature=temperature, top_k=top_k, top_p=top_p
        )

        saver = tf.train.Saver()
        ckpt = tf.train.latest_checkpoint(os.path.join(models_dir, model_name))
        saver.restore(sess, ckpt)


        #raw_text = input("Model prompt >>> ")
        context_tokens = enc.encode(raw_text)
        generated = 0
        for _ in range(nsamples // batch_size):
            out = sess.run(output, feed_dict={
                context: [context_tokens for _ in range(batch_size)]
            })[:, len(context_tokens):]
            for i in range(batch_size):
                generated += 1
                text = enc.decode(out[i])
                # and here gpt2 returns the output
        sess.close()
    return text

### Test the GPT2 Function
# print(interact_model('Cats are cute.'))



# ================================ Google W2V ==================================
# =================================Helper Functions=============================

# deal with stopwords and punctuation marks
stopwords_list = nltk.corpus.stopwords.words('english')
tokenizer = nltk.RegexpTokenizer(r'\w+')


# function to convert a sentence to a list of words
def sent_to_list(sent):
    '''
    gets sentence returns a list of words
    '''
    # tokenize the input sentence to a list
    sent_list = tokenizer.tokenize(sent)
    # and remove the stopwords
    sent_list = [word for word in sent_list if (not(word in stopwords_list) and word in Gmodel.vocab)]
    return sent_list


# function to convert a paragraph to a list of sentences
def text_to_sents(text):
    '''
    gets text returns a list of sentences
    '''
    # tokenize the gpt2 output
    sentences = nltk.tokenize.sent_tokenize(text.lower()) # to sentences

    return sentences



def get_candidates(text, goal_word):
    '''
    this function gets a paragraph and compare each of its sentences to a goal
    word and returns a dictionary of sentences and their similarity scores
    '''
    # if input is a string, split it into sentences
    if isinstance(text, str):
        text = text_to_sents(text)
    candidates = {}
    # similarity between current sentence and goal_word (must be updated)
    current_sim = 0.0
    for sent in text:
        try:
            sim = Gmodel.n_similarity(sent_to_list(sent), [goal_word])
            if sim > current_sim:
                candidates[sent] = sim
                current_sim = sim
        except ZeroDivisionError:
            pass
    return candidates

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

def choose_sentence(candidates):
    '''
    this function for now jsut iterates over all candidates and returns
    the candidate with the highest similarity to the goal word
    TODO: make it smart
    '''
    most_similar_to_goal_value = 0.0
    most_similar_to_goal_key = "default"
    for candidate in candidates:
        if candidates[candidate] > most_similar_to_goal_value:
            most_similar_to_goal_key = candidate
            most_similar_to_goal_value = candidates[candidate]
    return most_similar_to_goal_key
