# 【第1回】データサイエンス・カップ 2015 春

## 使用ソフトウェア

* Python3
* scikit-learn
    * `sklearn.cross_validation.cross_val_score`
    * `sklearn.ensemble.RandomForestRegressor`
    * `sklearn.feature_extraction.DictVectorizer`

## 解析手法

* Random Forest
* Cross Validation

## モデリング詳細

### 前処理

script: `join.py`

* 文字コードの修正
    * `nkf -w`
* `train.csv` および `test.csv` に `stadium.csv` と `condition.csv` を結合し、ラベルを付与
    * ラベル付きデータは `joined_train.json` , `joined_test.json`
    * ラベル一覧は `label.json`

### ベクトル化

script: `vectorize.py`

* カテゴリ特徴の二値化
* 数値特徴を [-1, +1] の範囲に正規化
* ラベル付きベクトルは `labeled_train.json` , `labeled_test.json`

### 予測

script: `predict.py`

* `-o` オプションで出力、 `-c` オプションで評価（5-fold Cross Validation）
* 変数 `filter_features` で使用する特徴を選択
    * 評価結果に基づいてリーグ・節・曜日・休日・アウェーチーム・競技場・収容量を採用
* アルゴリズムの選択
    * Random ForestとLassoを試し、よりスコアの高かったRandom Forestを採用
    * 内部的な決定木数は10, 20, 50, 100を試し、最もスコアの高かった50を採用
    * 過学習を防ぐため、木の深さは最大20に制限

### 修正

script: `adjust.py`

* 実現性の低い結果を修正
    * 競技場の収容量を超えない
    * ホームチーム・アウェーチームの過去の動員数の [最小値, 最大値] の範囲に収まる

## モデル再現手順

```
$ cd compe9`
$ source ./env/bin/activate
$ python ./join.py
$ python ./vectorize.py
$ python ./adjust.py
$ cat data/result_adjust.csv
# 結果表示
```

## 乱数の取り扱い

投稿データ出力時に `sklearn.ensemble.RandomForestRegressor` に対して乱数シード指定を忘れたため、シードが不明となってしまっている

## 各変数のモデルに対する寄与度

今回採用した特徴群から各特徴を除外した場合のスコアは次の通り

| 除外特徴 | Cross Validation結果 |
|:--------:|:---------------------|
| league   | 3979.34 +/- 1218.83  |
| season   | 3577.25 +/- 1453.31  |
| weekday  | 3410.51 +/- 1473.87  |
| holiday  | 3504.20 +/- 1407.60  |
| away     | 3684.61 +/- 1548.22  |
| stadium  | 3628.58 +/- 1450.90  |
| capacity | 3506.82 +/- 1513.94  |

## リンク

* [【第1回】データサイエンス・カップ 2015 春 | サポーターズ - 「会える」学生向けキャリア支援サービス -](https://supporterz.jp/spevents/detail/opt_datascience)
* [コンペ詳細 ビッグデータ活用ならオプトDSL](https://datasciencelab.jp/compe/9)
* [ブログ詳細 ビッグデータ活用ならオプトDSL](https://datasciencelab.jp/blog/172)

