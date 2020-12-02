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


def process_source_array(source):
    return source['data']['children']

def get_source_dict(source_array):
    return source_array[0]

def process_source_posts(data):
    for i in range(len(data)):
        if(data[i]['kind']=='Listing'):
            data[i] = process_source_array(data[i])
            data[i] = get_source_dict(data[i])
    return data

def join_data(train_data, dev_data):
    return train_data + dev_data

def add_rlabels(data, train_labels, dev_labels):
    for datapoint in data:
        try:
            identifier = datapoint['data']['id']
        except KeyError:
            print('Oops! Something went wrong...')
        try:
            datapoint['data']['task_A_label'] = train_labels['subtaskaenglish'][str(identifier)]
            datapoint['data']['split'] = 'train'
            try:
                datapoint['data']['task_B_label'] = train_labels['subtaskbenglish'][str(identifier)]
            except KeyError:
                pass
        except KeyError:
            datapoint['data']['task_A_label'] = dev_labels['subtaskaenglish'][str(identifier)]
            datapoint['data']['split'] = 'dev'
            try:
                datapoint['data']['task_B_label'] = dev_labels['subtaskbenglish'][str(identifier)]
            except KeyError:
                pass
    return data

'''
Twitter: post depths
'''
def add_depth_feature(twitter_data, depth_dict):
    for datapoint in twitter_data:
        try:
            identifier = datapoint['data']['id']
            datapoint['data']['depth'] = depth_dict[str(identifier)]
            print(datapoint['data']['depth'])
        except RuntimeError:
            print('Error: no depth assigned for this datapoint!')

    return twitter_data


if __name__ == "__main__":

    # Copy & paste all this into iPython (or some other shell)
    # You can then explore the training data e.g. train[0] will
    # print the firt data point (i.e. a dict object)

    # Data
    training_data_zip = ('../data/rumoureval-2019-training-data.zip')
    training_data_directory = ZipFile(training_data_zip)
    training_data_contents = get_directory_structure(training_data_directory)
    reddit_training_data = training_data_contents['reddit-training-data']
    reddit_dev_data = training_data_contents['reddit-dev-data']

    # Labels
    train_labels = json.loads(training_data_directory.read('rumoureval-2019-training-data/train-key.json'))
    dev_labels = json.loads(training_data_directory.read('rumoureval-2019-training-data/dev-key.json'))

    # Processing
    depth, dev = get_twitter_datapoints(training_data_directory, twitter_english)
    dev = add_rlabels(dev, train_labels, dev_labels)
    dev = add_depth_feature(dev, depth)
    pass