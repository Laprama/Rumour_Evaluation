import os
import json
import zipfile
import functools

DATA_DIR = '../data'
TRAINING_DATA_ZIP = 'data/rumoureval-2019-training-data.zip'
TRAINING_DATA_DIR = 'rumoureval-2019-training-data'

# Unzip training data into directory of same name

def unzip_data(TRAINING_DATA_DIR, TRAINING_DATA_ZIP):
    if os.path.isdir(TRAINING_DATA_DIR):
        raise IsADirectoryError("Directory already exists!")
    elif(os.path.isfile(TRAINING_DATA_ZIP)):
        with zipfile.ZipFile(TRAINING_DATA_ZIP, 'r') as zip:
            zip.extractall()
    else:
        raise FileDoesNotExist
