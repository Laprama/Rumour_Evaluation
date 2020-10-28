import os
import json
import zipfile
from pathlib import Path
import functools

TRAINING_DATA_DIR = 'rumoureval-2019-training-data'
TRAINING_LABELS = 'rumoureval-2019-training-data/train-key.json'
DATA_SOURCE = 'twitter-english'
TWITTER_SUBJECT = 'charliehebdo'
TWEET_TYPE = 'replies'

class Post:
    def __init__(self, TwitterPost):

        self._id = TwitterPost['id']
        self._text = TwitterPost['text']
        self._retweet_count = TwitterPost['retweet_count']
        self._parent_tweet = TwitterPost['in_reply_to_status_id']

    def get_id(self):
        return self._id

    def get_text(self):
        return self._text

    def get_label(self, Labels):
        return Labels['subtaskaenglish'][str(self._id)]

    def info(self, Labels):
        print('ID: {id}\nText: {text}\nLabel: {label}'.format(
            id=self.get_id(),
            text=self.get_text(),
            label=self.get_label(Labels)))


# inputs: source (i.e. twitter or reddit), 
#         subject (i.e. charliehebdo)
#         type (i.e, source or reply)

# returns a list of all the json file paths

def get_post_paths(source, subject, type): 

    root = os.listdir(TRAINING_DATA_DIR)

    for source in root:
        file_path_list = []
        if (source == DATA_SOURCE):
            subject_path = os.path.join(TRAINING_DATA_DIR, source)
            subject_list = os.listdir(subject_path)
            for subject in subject_list:
                if(subject == TWITTER_SUBJECT):
                    tweet_path = os.path.join(subject_path, subject)
                    tweet_ids = os.listdir(tweet_path)
                    for identifier in tweet_ids:
                        id_path = os.path.join(tweet_path, identifier)
                        id_dir = os.listdir(id_path)
                        for tweet_type in id_dir:
                            if(tweet_type == TWEET_TYPE):
                                file_paths = os.path.join(id_path, tweet_type)
                                file_list = os.listdir(file_paths)
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

def build_dataset(posts, labels):

    data = []

    for i in range(len(posts)):
        data.append(posts[i].get_text())
        print(posts[i].get_label(labels))
    return data


def main():
    with open(TRAINING_LABELS, "r") as json_labels:
        labels = json.load(json_labels)

    post_paths = get_post_paths(DATA_SOURCE, TWITTER_SUBJECT, TWEET_TYPE)

    posts = get_all_posts(post_paths)
    
    a = posts[0].get_label(labels)
    print(a)

    a = build_dataset(posts, labels)

    # getting KeyError when trying to return label here
    # checked the train file and looks like the entry is missing/doesnt exist
    # 552789083211460608
    # 552789083211460608
    

    
    
    
    
    



if __name__ == "__main__":
    main()
    



                    

      


