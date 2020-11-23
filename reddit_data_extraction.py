from twitter_data_extraction import *

TRAINING_DATA_ARCHIVE_FILE = ('data/rumoureval-2019-training-data.zip')
training_data_directory = ZipFile(TRAINING_DATA_ARCHIVE_FILE)
training_data_contents = get_directory_structure(training_data_directory)

reddit_training_data = training_data_contents['reddit-training-data']
reddit_dev_data = training_data_contents['reddit-dev-data']

'''
Reddit: extracting datapoints as Dict objects
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



