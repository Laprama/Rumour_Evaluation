from preprocessing import *
import pytest

# Labels
TRAINING_LABELS = 'rumoureval-2019-training-data/train-key.json'
with open(TRAINING_LABELS, "r") as json_labels:
        labels = json.load(json_labels)


# Path to random selection of tweets in json file format - replies
test_1 = 'rumoureval-2019-training-data/twitter-english/charliehebdo/552806309540528128/replies/552806614973960192.json'
test_2 = 'rumoureval-2019-training-data/twitter-english/germanwings-crash/580340476949086208/replies/580341529870348288.json'
test_3 = 'rumoureval-2019-training-data/twitter-english/prince-toronto/529660296080916480/replies/529661510369284096.json'
test_4 = 'rumoureval-2019-training-data/twitter-english/putinmissing/576812998418939904/replies/576813541736517634.json'

# Post class tests
def test_class_instantiation():
    path_1 = 'rumoureval-2019-training-data/twitter-english/charliehebdo/552806309540528128/replies/552806614973960192.json'
    post = get_post(path_1)
    print(post.get_id())
    assert(str(post.get_id()) == '552806614973960192')


# Path to random selection of tweets in json file format - source