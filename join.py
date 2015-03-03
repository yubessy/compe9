# -*- coding: utf-8 -*-
'''
This script is for joining of dataset.
'''

import json


DATA_DIR = 'data/'
LABEL_JSON = DATA_DIR + 'label.json'
TRAIN_CSV = DATA_DIR + 'train_utf8.csv'
TEST_CSV = DATA_DIR + 'test_utf8.csv'
STADIUM_CSV = DATA_DIR + 'stadium_utf8.csv'
CONDITION_CSV = DATA_DIR + 'condition_utf8.csv'
JOINED_TRAIN_JSON = DATA_DIR + 'joined_train.json'
JOINED_TEST_JSON = DATA_DIR + 'joined_test.json'


def merge_dicts(dicts):
    res = dict()
    for d in dicts:
        if d:
            res.update(d)
    return res


def main():
    with open(LABEL_JSON) as label_file:
        label = json.loads(label_file.read())

    with open(TRAIN_CSV) as train_file:
        train = [l.rstrip().split(',') for l in train_file]

    with open(TEST_CSV) as test_file:
        test = [l.rstrip().split(',') for l in test_file]

    with open(STADIUM_CSV) as stadium_file:
        stadium = [l.rstrip().split(',') for l in stadium_file]

    with open(CONDITION_CSV) as condition_file:
        condition = [l.rstrip().split(',') for l in condition_file]

    labeled_train = [dict(zip(label['train'], x)) for x in train]
    labeled_test = [dict(zip(label['test'], x)) for x in test]

    stadium_dicts = {
        x[0]: dict(zip(label['stadium'][1:], x[1:])) for x in stadium}
    condition_dicts = {
        x[0]: dict(zip(label['condition'][1:], x[1:])) for x in condition}

    joined_train = [
        merge_dicts((
            d, stadium_dicts.get(d['stadium']), condition_dicts.get(d['id'])))
        for d in labeled_train]
    joined_test = [
        merge_dicts((
            d, stadium_dicts.get(d['stadium']), condition_dicts.get(d['id'])))
        for d in labeled_test]

    with open(JOINED_TRAIN_JSON, 'w') as joined_train_file:
        joined_train_file.write(json.dumps(joined_train))

    with open(JOINED_TEST_JSON, 'w') as joined_test_file:
        joined_test_file.write(json.dumps(joined_test))


if __name__ == '__main__':
    main()
