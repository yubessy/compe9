# -*- coding: utf-8 -*-
'''
This script is for adjustment.
'''

import json

DATA_DIR = 'data/'
PREDICT_CSV = DATA_DIR + 'predict_ne50md20lf.csv'
JOINED_TRAIN_JSON = DATA_DIR + 'joined_train.json'
JOINED_TEST_JSON = DATA_DIR + 'joined_test.json'


def main():
    with open(JOINED_TRAIN_JSON) as joined_train_file:
        train = json.loads(joined_train_file.read())

    with open(JOINED_TEST_JSON) as joined_test_file:
        test = json.loads(joined_test_file.read())

    with open(PREDICT_CSV) as predict_file:
        predict = [
            (i, int(v))
            for i, v in (l.rstrip().split(',') for l in predict_file)]

    max_by_home_team = dict()
    min_by_home_team = dict()
    max_by_away_team = dict()
    min_by_away_team = dict()
    for d in train:
        max_by_home_team[d['home_team']] = max(
            int(d['result']),
            max_by_home_team.get(d['home_team'], 0))
        min_by_home_team[d['home_team']] = min(
            int(d['result']),
            min_by_home_team.get(d['home_team'], int(d['capacity'])))
        max_by_away_team[d['away_team']] = max(
            int(d['result']),
            max_by_away_team.get(d['away_team'], 0))
        min_by_away_team[d['away_team']] = min(
            int(d['result']),
            min_by_away_team.get(d['away_team'], int(d['capacity'])))

    for (i, v), d in zip(predict, test):
        ma = (
            max_by_home_team[d['home_team']]
            + max_by_away_team[d['away_team']]) / 2
        mi = (
            min_by_home_team[d['home_team']]
            + min_by_away_team[d['away_team']]) / 2
        if v > ma:
            v = ma
        elif v < mi:
            v = mi
        print("{},{}".format(i, v))


if __name__ == '__main__':
    main()
