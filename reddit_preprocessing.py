import os
import json
import zipfile
from pathlib import Path
import functools
from concurrent.futures import ProcessPoolExecutor

# desperately need to begin testing all functions, classes and associated methods
# do this before it's too late!

TRAINING_DATA_DIR = 'rumoureval-2019-training-data'
TRAINING_LABELS = 'rumoureval-2019-training-data/train-key.json'
DEV_LABELS = 'rumoureval-2019-training-data/dev-key.json'
DATA_SOURCE = 'reddit-training-data'
REDDIT_TYPE = 'source-tweet'

class Post:
    def __init__(self, RedditPost):

        # TODO: consider what information we need to extract from the post
        # TODO: ideas: depth, retweets, sensitive could all be used in feature engineering

        self._id = RedditPost['id']
        self._text = RedditPost['body']
        self._example_type = None

        
    def get_id(self):
        return self._id

    def get_text(self):
        return self._text
    
    def get_flag(self):
        return self._example_type

    def get_label(self, TrainingLabels, DevLabels):
        try:
            label = TrainingLabels['subtaskaenglish'][str(self._id)]
            try:
                self._train_example = True
                self._dev_eample = False
            except RuntimeError:
                print(f"{self._id}: couldn't set train flag.")
            return label 
        except KeyError as e:
            label = DevLabels['subtaskaenglish'][str(self._id)]
            try:
                self._train_example = False
                self._dev_example = True
            except RuntimeError:
                print(f"{self._id}: couldn't set dev flag.")
            return label

    def flag_train_dev(self, TrainingLabels, DevLabels):
        try:
            train = TrainingLabels['subtaskaenglish'][str(self._id)]
            self._example_type = True
        except KeyError as e:
            dev = DevLabels['subtaskaenglish'][str(self._id)]
            self._example_type = False

    def info(self, Labels):
        print('ID: {id}\nText: {text}\nLabel: {label}'.format(
            id=self.get_id(),
            text=self.get_text(),
            label=self.get_label(Labels)))


# inputs: source (i.e. twitter or reddit), 
#         subject (i.e. charliehebdo)
#         type (i.e, source or reply)

# returns a list of all the json file paths

def get_subject(source):
    if (source == DATA_SOURCE):
        try:
            subject_path = os.path.join(TRAINING_DATA_DIR, source)
            subject_list = os.listdir(subject_path)
        except RuntimeError:
            print(f"Couldn't get {subject_path} or {subject_list} train flag.")
    return subject_path, subject_list

def get_reddit_post(subject, subject_path):
    try:
        tweet_path = os.path.join(subject_path, subject)
        tweet_ids = os.listdir(tweet_path)
    except RuntimeError:
        print(f"Couldn't get {tweet_path} or {tweet_ids} train flag.")
    return tweet_path, tweet_ids

def get_ids(identifier, tweet_path):
    try:
        id_path = os.path.join(tweet_path, identifier)
        id_dir = os.listdir(id_path)
    except RuntimeError:
        print(f"Couldn't get {id_paths} or {id_dir} train flag.")
    return id_path, id_dir

def get_files(tweet_type, id_path):
    try:
        file_paths = os.path.join(id_path, tweet_type)
        file_list = os.listdir(file_paths)
    except RuntimeError:
        print(f"Couldn't get {file_paths} or {file_list} train flag.")
    return file_paths, file_list

def get_post_paths(source, type): 

    root = os.listdir(TRAINING_DATA_DIR)

    for source in root:
        file_path_list = []
        subject_path, subject_list = get_subject(source=DATA_SOURCE)
        for subject in subject_list:
            reddit_path, reddit_list = get_reddit_post(subject, subject_path)
            for identifier in reddit_list:
                if(identifier == REDDIT_TYPE):
                    file_paths, file_list = get_files(type, reddit_path)
                    for file in file_list:
                        file_path_list.append(os.path.join(file_paths, file))
    return(file_path_list)


def get_post(file_path):
    # given a path to a json file, return a Post
    with open(file_path, "r") as json_file:
        tweet_dict = json.load(json_file)
    return Post(tweet_dict)

def get_all_posts(file_path_list):
    # get a list of Post objects
    posts = []
    for file_path in file_path_list:
        post = get_post(file_path)
        posts.append(post)
    return posts

def build_dataset(posts, training_labels, dev_labels):
    
    """
    Given a list of Post objects, this function seperates
    data (i.e. text) and labels and returns them as arrays.
    """
    data = []
    labels = []
    for p in posts:
        data.append(p.get_text())
        labels.append(p.get_label(training_labels, dev_labels))
    return data, labels

def set_flag(posts, training_labels, dev_labels):
    """
    Given a list of Post objects, this function iterates
    through each of them and identifies whether the example
    is a training or development example. The output is a
    list of Post objects with the appropriate flag set.
    """
    for post in posts:
        post.flag_train_dev(training_labels, dev_labels)
    return posts

def split_train_dev(posts):
    """
    Given a list of Post objects, this function seperates 
    training and development examples into seperate lists
    and returns them.
    """
    train_posts = []
    dev_posts = []

    for post in posts:
        if(post.get_flag() == True):
            train_posts.append(post)
        elif(post.get_flag() == False):
            dev_posts.append(post)
        else:
            raise RuntimeError(f"Example type (train-test) has not been set")
    return train_posts, dev_posts


def main():
    with open(TRAINING_LABELS, "r") as json_tlabels:
        training_labels = json.load(json_tlabels)
    
    with open(DEV_LABELS, "r") as json_dlabels:
        dev_labels = json.load(json_dlabels)
    
    post_paths = get_post_paths(DATA_SOURCE, REDDIT_TYPE)

    print(len(post_paths)) # dev = 426





    



 # Keys of Twitter dictionary
# 'contributors', 'truncated', 'text', 'in_reply_to_status_id', 'id',
# 'favorite_count', 'source', 'retweeted', 'coordinates', 'entities',
# 'in_reply_to_screen_name', 'id_str', 'retweet_count', 'in_reply_to_user_id',
# 'favorited', 'user', 'geo', 'in_reply_to_user_id_str', 'possibly_sensitive', 'lang',
# 'created_at', 'in_reply_to_status_id_str', 'place', 'extended_entities']   
    
    
    

if __name__ == "__main__":
    main()
    



                    

      


