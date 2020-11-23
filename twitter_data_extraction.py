import os
import json
import zipfile
from pathlib import Path
import functools
from zipfile import ZipFile

def get_directory_structure(directory):
    result = {}
    for file in directory.namelist():
        if file.endswith('/'):
            continue
        d = result
        path = file.split('/')[1:]  
        for p in path[:-1]:
            if p not in d:
                d[p] = {}
            d = d[p]
        d[path[-1]] = file
    return result

def get_thread_depth(thread_structure):
    post_depths = {}
    def walk(thread, depth):
        for post_id, subthread in thread.items():
            post_depths[post_id] = depth
            if isinstance(subthread, dict):
                walk(subthread, depth + 1)
    walk(thread_structure, 0)
    return post_depths

'''
Twitter: extracting datapoints as Dict objects
'''

def get_twitter_datapoints(training_data_archive, twitter_english):
    
    depths = {}
    datapoints = []
    
    for archive, topics in [(training_data_archive, twitter_english.items())]:
        for topic, threads in topics:
            for thread in threads.values():
                    # Calculate the depth of the thread based on the structure.json file
                    post_depth = get_thread_depth(
                        json.loads(archive.read(thread['structure.json'])))
                    depths.update(post_depth)
                    # Extract Twitter post as Dict from 'replies' directory 
                    # and append to datapoints list                    
                    for reply in thread.get('replies', {}).values():
                        datapoints.append(json.loads(archive.read(reply)))
                    # Extract Twitter post as Dict from 'source-tweet' directory 
                    # and append to datapoints list                    
                    for source in thread.get('source-tweet', {}).values():
                        datapoints.append(json.loads(archive.read(source)))
    return depths, datapoints

'''
Twitter: post depths
'''
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
         add which split the data point belongs to (i.e. train or dev)
'''
def add_labels(data, train_labels, dev_labels):
    for datapoint in data:
        identifier = datapoint['id']
        try:
            datapoint['labels'] = train_labels['subtaskaenglish'][str(identifier)]
            datapoint['split'] = 'train'
        except KeyError:
            datapoint['labels'] = dev_labels['subtaskaenglish'][str(identifier)]
            datapoint['split'] = 'dev'
    return data


'''
Reddit Data...
'''

def get_reddit_datapoints(training_data_archive, reddit_training_data):
    
    depths = {}
    datapoints = []
    
    for archive, threads in [(training_data_archive, reddit_training_data.values())]:
        for thread in threads:
                # Calculate the depth of the thread based on the structure.json file
                '''
                post_depth = get_thread_depth(
                    json.loads(archive.read(thread['structure.json'])))
                depths.update(post_depth)
                '''
                # Extract Twitter post as Dict from 'replies' directory 
                # and append to datapoints list                    
                for reply in thread.get('replies', {}).values():
                    datapoints.append(json.loads(archive.read(reply)))

                # Extract Twitter post as Dict from 'source-tweet' directory 
                # and append to datapoints list                    
                for source in thread.get('source-tweet', {}).values():
                    datapoints.append(json.loads(archive.read(source)))
                
    return depths, datapoints

def join_data(train_data, dev_data):
    return train_data + dev_data

def add_rlabels(data, train_labels, dev_labels):
    for datapoint in data:
        try:
            identifier = datapoint['data']['id']
        except KeyError:
            print(datapoint['data']['children'][0]['data']['id']) # WEIRDDDD
        try:
            datapoint['data']['labels'] = train_labels['subtaskaenglish'][str(identifier)]
            datapoint['data']['split'] = 'train'
        except KeyError:
            datapoint['data']['labels'] = dev_labels['subtaskaenglish'][str(identifier)]
            datapoint['data']['split'] = 'dev'
    return data


if __name__ == "__main__":
    TRAINING_DATA_ARCHIVE_FILE = ('data/rumoureval-2019-training-data.zip')
    training_data_directory = ZipFile(TRAINING_DATA_ARCHIVE_FILE)
    training_data_contents = get_directory_structure(training_data_directory)

    reddit_training_data = training_data_contents['reddit-training-data']
    reddit_dev_data = training_data_contents['reddit-dev-data']

    train_labels = json.loads(training_data_directory.read('rumoureval-2019-training-data/train-key.json'))
    dev_labels = json.loads(training_data_directory.read('rumoureval-2019-training-data/dev-key.json'))

    depth, train = get_reddit_datapoints(training_data_directory, reddit_dev_data)
    train = add_rlabels(train, train_labels, dev_labels)
    pass


    
