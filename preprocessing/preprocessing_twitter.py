import os
import json
import zipfile
import functools
import pandas as pd
import preprocessor as tp

'''
Twitter: extracting datapoints as Dict objects
'''

def preprocess_text(text):
    tokenised_text = tp.tokenize(text)
    return tokenised_text     

def clean_text(text):
    tp.set_options(tp.OPT.EMOJI, tp.OPT.SMILEY)
    cleaned_text = tp.clean(text)
    return cleaned_text     


'''
Features...
For a single row, to be used with df.apply()
'''

def build_hashtag_feature(text:'input: df["text"]'):
    parsed_text = tp.parse(text)
    try:
        hash_tags = [hashtag.match for hashtag in parsed_text.hashtags]
        return hash_tags
    except TypeError:
        pass

def build_url_feature(text:'input: df["text"]'):
    parsed_text = tp.parse(text)
    try:
        urls = [url.match for url in parsed_text.urls]
        return urls
    except TypeError:
        pass

'''
General function for building new features
'''

def build_feature(df, build_func, new_feature_name):
    feature = df['text'].apply(build_func)
    df.insert(df.columns.get_loc('text'), str(new_feature_name), feature)
    return df

    

