# -*- coding: utf-8 -*-
'''
This script is for prediction
'''

import json

from sklearn.feature_extraction import DictVectorizer
from sklearn.linear_model import Lasso


DATA_DIR = 'data/'
LABELED_TRAIN_VEC_JSON = DATA_DIR + 'labeled_train_vec.json'
LABELED_TEST_VEC_JSON = DATA_DIR + 'labeled_test_vec.json'


def load():
    with open(LABELED_TRAIN_VEC_JSON) as labeled_train_vec_file:
        labeled_train_vecs = json.loads(labeled_train_vec_file.read())

    with open(LABELED_TEST_VEC_JSON) as labeled_test_vec_file:
        labeled_test_vecs = json.loads(labeled_test_vec_file.read())

    train_i = [d.pop('id') for d in labeled_train_vecs]
    train_y = [d.pop('result') for d in labeled_train_vecs]

    test_i = [d.pop('id') for d in labeled_test_vecs]

    dv = DictVectorizer()
    dv.fit(labeled_train_vecs + labeled_test_vecs)
    train_x = dv.transform((d for d in labeled_train_vecs))
    test_x = dv.transform((d for d in labeled_test_vecs))

    return dict(
        train_i=train_i,
        train_y=train_y,
        test_i=test_i,
        train_x=train_x,
        test_x=test_x)


def predict(train_x, train_y, test_x):
    reg = Lasso()
    reg.fit(train_x, train_y)
    test_y = reg.predict(test_x)
    return test_y


def output(test_i, test_y):
    for i, y in zip(test_i, test_y):
        print('{},{}'.format(i, int(y)))


def main():
    data = load()
    test_y = predict(data['train_x'], data['train_y'], data['test_x'])
    output(data['test_i'], test_y)


if __name__ == '__main__':
    main()
