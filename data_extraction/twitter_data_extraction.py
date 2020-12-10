import os
import json
import zipfile
import functools
import pandas as pd
from zipfile import ZipFile
from pathlib import Path

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
Navigating ZipFIle objects (directory structures)
'''

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

'''
Utilising 'structure.json' to find the 'depth' of posts 
'''

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
            datapoint['task_A_label'] = train_labels['subtaskaenglish'][str(identifier)]
            datapoint['split'] = 'train'
            try:
                datapoint['task_B_label'] = train_labels['subtaskbenglish'][str(identifier)]
            except KeyError:
                pass
        except KeyError:
            datapoint['task_A_label'] = dev_labels['subtaskaenglish'][str(identifier)]
            datapoint['split'] = 'dev'
            try:
                datapoint['task_B_label'] = dev_labels['subtaskbenglish'][str(identifier)]
            except KeyError:
                pass
    return data

def get_twitter_data(training_data_directory, twitter_data, train_labels, dev_labels):
    # Processing
    depth, data = get_twitter_datapoints(training_data_directory, twitter_data)
    data = add_labels(data, train_labels, dev_labels)
    data = add_depth_feature(data, depth)
    df = pd.DataFrame(data)
    
    train_df = df[df['split'] == 'train']
    dev_df = df[df['split'] == 'dev']
    return train_df, dev_df


if __name__ == "__main__":

    # Copy & paste all this into iPython (or some other shell)
    # You can then explore the training data e.g. train[0] will
    # print the firt data point (i.e. a dict object)

    # Data
    training_data_zip = ('../data/rumoureval-2019-training-data.zip')
    training_data_directory = ZipFile(training_data_zip)
    training_data_contents = get_directory_structure(training_data_directory)
    twitter_english = training_data_contents['twitter-english']

    # Labels
    train_labels = json.loads(training_data_directory.read('rumoureval-2019-training-data/train-key.json'))
    dev_labels = json.loads(training_data_directory.read('rumoureval-2019-training-data/dev-key.json'))

    # Processing
    depth, train = get_twitter_datapoints(training_data_directory, twitter_english)
    train = add_labels(train, train_labels, dev_labels)
    train = add_depth_feature(train, depth)
    pass


    
