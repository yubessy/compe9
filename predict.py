# -*- coding: utf-8 -*-
'''
This script is for prediction
'''

import json

from sklearn.feature_extraction import DictVectorizer
from sklearn.linear_model import Lasso
from sklearn.preprocessing import normalize, scale


DATA_DIR = 'data/'
LABELED_TRAIN_VEC_JSON = DATA_DIR + 'labeled_train_vec.json'
LABELED_TEST_VEC_JSON = DATA_DIR + 'labeled_test_vec.json'


def main():
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

    reg = Lasso()
    reg.fit(train_x, train_y)
    test_y = reg.predict(test_x)
    for i, y in zip(test_i, test_y):
        print('{},{}'.format(i, int(y)))


if __name__ == '__main__':
    main()
