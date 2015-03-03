# -*- coding: utf-8 -*-
'''
This script is for vectorization.
'''

import json
import re


DATA_DIR = 'data/'
JOINED_TRAIN_JSON = DATA_DIR + 'joined_train.json'
JOINED_TEST_JSON = DATA_DIR + 'joined_test.json'
LABELED_TRAIN_VEC_JSON = DATA_DIR + 'labeled_train_vec.json'
LABELED_TEST_VEC_JSON = DATA_DIR + 'labeled_test_vec.json'

PLAYER_K = re.compile(r'(home|away)\d{2}')
SEASON_V = re.compile(r'(第\d+節)(第\d+日)')
DATE_V = re.compile(r'(\d{2})/(\d{2})\((.)((・[祝休])?)\)')
TIME_V = re.compile(r'(\d{2}):(\d{2})')

MIN_CAPACITY = 3560
MIN_TEMPERATURE = 0
MIN_HUMIDITY = 0


def numericalize(feature_dict):
    res = dict()
    for k, v in feature_dict.items():
        if k == 'id':
            res[k] = int(v)
        elif k == 'result':
            res[k] = int(v)
        elif k == 'year':
            res['year#{}'.format(v)] = 1
        elif k == 'league':
            res['league#j1'] = 1 if v == 'Ｊ１' else 0
        elif k == 'season':
            m = SEASON_V.match(v)
            res['season#{}'.format(m.group(1))] = 1
            res['day#{}'.format(m.group(2))] = 1
        elif k == 'date':
            m = DATE_V.match(v)
            res['month#{}'.format(m.group(1))] = 1
            res['weekday#{}'.format(m.group(3))] = 1
            res['holiday#'] = 1 if m.group(4) or m.group(3) in '土日' else 0
        elif k == 'time':
            m = TIME_V.match(v)
            res['hour#{}'.format(m.group(1))] = 1
        elif k == 'home_team':
            res['team#{}'.format(v)] = 1
            res['home#{}'.format(v)] = 1
        elif k == 'away_team':
            res['team#{}'.format(v)] = 1
            res['away#{}'.format(v)] = 1
        elif k == 'stadium':
            res['stadium#{}'.format(v)] = 1
        elif k == 'tv':
            for x in v.split('／'):
                res['tv#{}'.format(x)] = 1
        elif k == 'address':
            res['pref#{}'.format(v[:2])] = 1  # 住所は都道府県のみ用いる
        elif k == 'capacity':
            res['capacity'] = int(v)
        elif k == 'home_score':
            res['home_score'] = int(v)
        elif k == 'away_score':
            res['away_score'] = int(v)
        elif k == 'weather':
            res['weather#{}'.format(v)] = 1
        elif k == 'humidity':
            res['humidity'] = float(v.rstrip('%')) / 100
        elif k == 'judge':
            res['judge#{}'.format(v)] = 1
        elif k[0:5] in ('home0', 'home1', 'away0', 'away1'):
            res['player#{}'.format(v)] = 1

    return res


def main():
    with open(JOINED_TRAIN_JSON) as joined_train_file:
        train = json.loads(joined_train_file.read())

    with open(JOINED_TEST_JSON) as joined_test_file:
        test = json.loads(joined_test_file.read())

    labeled_train_vecs = [numericalize(d) for d in train]
    labeled_test_vecs = [numericalize(d) for d in test]

    with open(LABELED_TRAIN_VEC_JSON, 'w') as labeled_train_vec_file:
        labeled_train_vec_file.write(json.dumps(labeled_train_vecs))

    with open(LABELED_TEST_VEC_JSON, 'w') as labeled_test_vec_file:
        labeled_test_vec_file.write(json.dumps(labeled_test_vecs))


if __name__ == '__main__':
    main()
