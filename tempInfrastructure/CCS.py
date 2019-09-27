#!/usr/bin/env python3

import fire
import json
import os
import numpy as np
import tensorflow as tf

from gpt2model import model, encoder, sample

tf.compat.v1.logging.set_verbosity(tf.compat.v1.logging.ERROR)
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

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
                print(text)

### Test the GPT2 Function
# print(interact_model('Cats are cute.'))



# ================================ Google W2V ==================================
# =================================Helper Functions=============================

# deal with stopwords and punctuation marks
stopwords_list = nltk.corpus.stopwords.words('english')
tokenizer = RegexpTokenizer(r'\w+')


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
    sentences = tokenize.sent_tokenize(text.lower()) # to sentences
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
        sim = Gmodel.n_similarity(sent_to_list(sent), [goal_word])
        print(sim)
        if sim > current_sim:
            candidates[sent] = sim
            current_sim = sim

    return candidates
