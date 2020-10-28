import os
import json
import zipfile
from pathlib import Path
import functools


DATA_DIR = Path('data')

TRAINING_DATA_ZIP = DATA_DIR / 'rumoureval-2019-training-data.zip'
TRAINING_DATA_DIR = 'rumoureval-2019-training-data'
TRAINING_LABELS = Path(TRAINING_DATA_DIR) / 'train-key.json'

# UNZIP TRAINING DATA
def unzip_data(TRAINING_DATA_DIR, TRAINING_DATA_ZIP):
    if os.path.isdir(TRAINING_DATA_DIR):
        raise IsADirectoryError("Directory already exists!")
    elif(os.path.isfile(TRAINING_DATA_ZIP)):
        with zipfile.ZipFile(TRAINING_DATA_ZIP, 'r') as zip:
            zip.extractall()
    # else:
    #     raise FileDoesNotExist

test_file = Path(TRAINING_DATA_DIR) / 'twitter-english/charliehebdo/552783667052167168/source-tweet/552783667052167168.json'
labels = Path(TRAINING_DATA_DIR) / 'train-key.json'


with open(test_file, "r") as json_file:
    tweet_dict = json.load(json_file)

with open(labels, "r") as json_labels:
    label_dict = json.load(json_labels)

class Post:
    def __init__(self, TwitterPost, Labels):

        self._id = TwitterPost['id']
        self._post_id = TwitterPost['text']

        # Check if tweet is a source or reply
        if(TwitterPost['in_reply_to_user_id'] == None):
            self._source = True
        else:
            self._reply = True

        self._retweet_count = TwitterPost['retweet_count']

        # TODO: add some conditions here for sources, reply etc.

        self._parent_tweet = TwitterPost['in_reply_to_status_id']
        self._sensitive = TwitterPost['possibly_sensitive']
        self._language = TwitterPost['lang']

    def get_id(self):
        return self._id

    def get_label(self, Labels):
        if(self._source):
            return Labels['subtaskbenglish'][str(self._id)]
        elif(self._reply):
            return Labels['subtaskaenglish'][str(self._id)]

def get_directory_structure(rootdir):
    """
    Creates a nested dictionary that represents the folder structure of rootdir
    """
    dir = {}
    rootdir = rootdir.rstrip(os.sep)
    start = rootdir.rfind(os.sep) + 1
    for path, dirs, files in os.walk(rootdir):
        folders = path[start:].split(os.sep)
        subdir = dict.fromkeys(files)
        parent = functools.reduce(dict.get, folders[:-1], dir)
        parent[folders[-1]] = subdir
    return dir

dir_dict = get_directory_structure('rumoureval-2019-training-data/twitter-english')
print(dir_dict['twitter-english']['charliehebdo']['552783667052167168'])


post = Post(tweet_dict, label_dict)
print(post.get_id())

    # Keys of Twitter dictionary
    # 'contributors', 'truncated', 'text', 'in_reply_to_status_id', 'id',
    # 'favorite_count', 'source', 'retweeted', 'coordinates', 'entities',
    # 'in_reply_to_screen_name', 'id_str', 'retweet_count', 'in_reply_to_user_id',
    # 'favorited', 'user', 'geo', 'in_reply_to_user_id_str', 'possibly_sensitive', 'lang',
    # 'created_at', 'in_reply_to_status_id_str', 'place', 'extended_entities']
