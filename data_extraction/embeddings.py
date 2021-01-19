# preprocess tweet text
import re
import numpy as np
import gensim

def get_cleaned_tweets(data_df):
    """
    Gets rid of @s and #s and emojis for now.
    """
    tweet_list = []
    for tweet in data_df['text']:
        clean_tweet = ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())
        clean_tweet = clean_tweet.split() # Split so each word is a single unit
        tweet_list.append(clean_tweet)
    data_df['cleaned_tweet'] = tweet_list
    return data_df

# Load the pretrained Word2Vec model
def loadW2vModel():
    """LOAD PRETRAINED MODEL"""
    global model_GN
    print ("Loading the model")
    model = gensim.models.KeyedVectors.load_word2vec_format(
                    '/Users/fl20994/Documents/IAI_CDT/TB1/Dialogue_and_Narrative/Assessment/rumour_detection/LSTM_RumourEval2019/GoogleNews-vectors-negative300.bin', binary=True)
    print ("Done!")
    return model

def cosine_sim(a, b):
    """ Get the cosine similarity between two vectors"""
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

def avg_sentence(sentence, wv):
    """Average vectors for words in a sentence"""
    v = np.zeros(300)
    for w in sentence:
        if w in wv:
            v += wv[w]
    return v / len(sentence)

# Try adding the word vectors as individual columns to the dataframe

# Create a sentence embedding array for each tweet

def get_embeddings(data_df, model, vec_labels):

    vec_arr = np.empty((0,300))
    for tweet in data_df['cleaned_text']:
        vec = avg_sentence(tweet, model.wv)
        vec_arr = np.append(vec_arr, np.array([vec]), axis=0)
    return vec_arr

# add each element of the vector as an individual features to the dataframe
def insert_embedding_feature(data_df, vec_array, vec_labels):
    for i in range(0,len(vec_labels)):
        data_df[vec_labels[i]] = vec_array[:,i]
    return data_df
