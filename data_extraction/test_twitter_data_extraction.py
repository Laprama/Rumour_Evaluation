from twitter_data_extraction import *
import pytest

def test_extraction_functions():
    '''
    Data
    '''
    training_data_path = '../data/rumoureval-2019-training-data.zip'
    training_data_directory = ZipFile(training_data_path)
    training_data_contents = get_directory_structure(training_data_directory)
    twitter_english = training_data_contents['twitter-english']

    '''
    Labels
    '''
    train_labels = json.loads(training_data_directory.read('rumoureval-2019-training-data/train-key.json'))
    dev_labels = json.loads(training_data_directory.read('rumoureval-2019-training-data/dev-key.json'))

    '''
    Processing/Extraction
    '''
    depths, datapoints = get_twitter_datapoints(training_data_directory, twitter_english)
    datapoints = add_depth_feature(datapoints, depths)
    datapoints = add_labels(datapoints, train_labels, dev_labels)

    # Test that we have the correct number of datapoints in total
    assert(len(datapoints)==5568)

    reply_count = 0
    source_tweet_count = 0

    for data in datapoints:
        if(data['depth']==0):
            source_tweet_count += 1
        else:
            reply_count += 1
    # Test that we have the correct number of total 'replies' posts
    assert(reply_count == (5568-325))
    # Test that we have the correct number of 'source-tweet' posts
    assert(source_tweet_count == 325)

    # Test that source tweets match data points with depth 0
    depth_zero_count = 0
    other_depth_count = 0

    for data in datapoints:
        try:
            if(data['depth'] == 0):
                train_labels['subtaskbenglish'][str(data['id'])]
                depth_zero_count += 1
        except KeyError as e:
            if(data['depth'] == 0):
                dev_labels['subtaskbenglish'][str(data['id'])]
                depth_zero_count += 1

    assert(depth_zero_count == 325)
        












    



    


        



    
    
    


