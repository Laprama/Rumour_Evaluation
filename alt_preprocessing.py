import os
import json
import zipfile
from pathlib import Path
import functools
from zipfile import ZipFile

def get_archive_directory_structure(archive: ZipFile):
    result = {}
    for file in archive.namelist():
        # Skip directories in archive.
        if file.endswith('/'):
            continue

        d = result
        path = file.split('/')[1:]  # [1:] to skip top-level directory.
        for p in path[:-1]:  # [:-1] to skip filename
            if p not in d:
                d[p] = {}
            d = d[p]
        d[path[-1]] = file
    return result

def calc_post_depths_from_thread_structure(thread_structure):
    post_depths = {}
    def walk(thread, depth):
        for post_id, subthread in thread.items():
            post_depths[post_id] = depth
            if isinstance(subthread, dict):
                walk(subthread, depth + 1)
    walk(thread_structure, 0)
    return post_depths


'''
Data
'''
TRAINING_DATA_ARCHIVE_FILE = ('data/rumoureval-2019-training-data.zip')
training_data_archive = ZipFile(TRAINING_DATA_ARCHIVE_FILE)
training_data_contents = get_archive_directory_structure(training_data_archive)

twitter_english = training_data_contents['twitter-english']
reddit_training_data = training_data_contents['reddit-training-data']
reddit_dev_data = training_data_contents['reddit-dev-data']

'''
Labels
'''
train_labels = json.loads(training_data_archive.read('rumoureval-2019-training-data/train-key.json'))
dev_labels = json.loads(training_data_archive.read('rumoureval-2019-training-data/dev-key.json'))

'''
Twitter: extracting datapoints as Dict objects
'''

def get_twitter_datapoints(training_data_archive, twitter_english):
    
    datapoints = []

    for archive, topics in [(training_data_archive, twitter_english.items())]:
        for topic, threads in topics:
            for thread in threads.values():
                    for reply in thread.get('replies', {}).values():
                        datapoints.append(json.loads(archive.read(reply)))
                    for source in thread.get('source-tweet', {}).values():
                        datapoints.append(json.loads(archive.read(source)))
    return datapoints

'''
Twitter: post depths
'''

def get_thread_depth(training_data_archive, twitter_english):

    depths = {}

    for archive, topics in [(training_data_archive, twitter_english.items())]:
        for topic, threads in topics:
            for thread in threads.values():
                    post_depth = calc_post_depths_from_thread_structure(
                        json.loads(archive.read(thread['structure.json'])))
                    depths.update(post_depth)
    return depths

def add_depth_feature(twitter_data, depth_dict):
    for datapoint in twitter_data:
        identifier = datapoint['id']
        try:
            datapoint['depth'] = depth_dict[str(identifier)]
        except RuntimeError:
            print('Error: no depth assigned for this datapoint!')

    return twitter_data

'''
Twitter: add Twitter labels to the training and development datasets
'''
def add_twitter_labels(twitter_data, train_labels, dev_labels):
    for datapoint in twitter_data:
        identifier = datapoint['id']
        try:
            datapoint['labels'] = train_labels['subtaskaenglish'][str(identifier)]
            datapoint['split'] = 'train'
        except KeyError:
            datapoint['labels'] = dev_labels['subtaskaenglish'][str(identifier)]
            datapoint['split'] = 'dev'
    return twitter_data