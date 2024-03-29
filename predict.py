# -*- coding: utf-8 -*-
'''
This script is for prediction
'''

import json
import sys

from numpy import sqrt
from sklearn.cross_validation import cross_val_score
from sklearn.ensemble import RandomForestRegressor
from sklearn.feature_extraction import DictVectorizer
from sklearn.linear_model import Lasso


DATA_DIR = 'data/'
LABELED_TRAIN_VEC_JSON = DATA_DIR + 'labeled_train_vec.json'
LABELED_TEST_VEC_JSON = DATA_DIR + 'labeled_test_vec.json'
RESULT_CSV = DATA_DIR + 'result.csv'


def load_dataset(labeled_train_vecs, labeled_test_vecs, filter_features=set()):
    if filter_features:
        filter_features = filter_features | {'id', 'result'}
        labeled_train_vecs = [
            {k: v for k, v in d.items() if k.split('#')[0] in filter_features}
            for d in labeled_train_vecs]
        labeled_test_vecs = [
            {k: v for k, v in d.items() if k.split('#')[0] in filter_features}
            for d in labeled_test_vecs]
    else:
        labeled_train_vecs = labeled_train_vecs.copy()
        labeled_test_vecs = labeled_test_vecs.copy()

    train_i = [d.pop('id') for d in labeled_train_vecs]
    test_i = [d.pop('id') for d in labeled_test_vecs]

    train_y = [d.pop('result') for d in labeled_train_vecs]

    dv = DictVectorizer()
    dv.fit(labeled_train_vecs + labeled_test_vecs)
    train_x = dv.transform((d for d in labeled_train_vecs))
    test_x = dv.transform((d for d in labeled_test_vecs))

    return train_i, test_i, train_x, test_x, train_y


def main(mode):
    with open(LABELED_TRAIN_VEC_JSON) as labeled_train_vec_file:
        labeled_train_vecs = json.loads(labeled_train_vec_file.read())

    with open(LABELED_TEST_VEC_JSON) as labeled_test_vec_file:
        labeled_test_vecs = json.loads(labeled_test_vec_file.read())

    filter_features = {
        #'year',
        'league',
        'season',
        #'day',
        #'month',
        'weekday',
        'holiday',
        #'hour',
        #'team',
        #'home',
        'away',
        'stadium',
        #'tv',
        #'address',
        'capacity',
        #'home_score',
        #'away_score',
        #'weather',
        #'humidity',
        #'judge',
        #'player',
    }
    train_i, test_i, train_x, test_x, train_y = load_dataset(
        labeled_train_vecs, labeled_test_vecs, filter_features)

    reg = RandomForestRegressor(
        n_estimators=50,
        max_depth=20)

    if mode == '-o':
        reg.fit(train_x.toarray(), train_y)
        test_y = reg.predict(test_x.toarray())
        with open(RESULT_CSV, 'w') as result_file:
            for i, y in zip(test_i, test_y):
                result_file.write('{},{}\n'.format(i, int(y)))

    elif mode == '-c':
        mses = cross_val_score(
            reg, train_x.toarray(), train_y,
            cv=5, scoring='mean_squared_error')
        rmses = sqrt(-mses)
        print("RMSE: {:.2f} +/- {:.2f}".format(rmses.mean(), rmses.std() * 2))


if __name__ == '__main__':
    main(sys.argv[1])
