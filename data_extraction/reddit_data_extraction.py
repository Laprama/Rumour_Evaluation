from twitter_data_extraction import *

'''
Reddit Data...
'''

def get_reddit_datapoints(training_data_archive, reddit_training_data):
    
    depths = {}
    datapoints = []
    
    for archive, threads in [(training_data_archive, reddit_training_data.values())]:
        for thread in threads:
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

    reddit_training_data = training_data_contents['reddit-training-data']
    reddit_dev_data = training_data_contents['reddit-dev-data']