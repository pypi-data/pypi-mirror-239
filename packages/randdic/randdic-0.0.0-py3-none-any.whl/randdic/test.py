# 高速乱択辞書 [randdic]
# 【動作確認 / 使用例】

import sys
from sout import sout
from tqdm import tqdm
from ezpip import load_develop
# 高速乱択辞書 [randdic]
randdic = load_develop("randdic", "../", develop_flag = True)


## 辞書のような使い方が可能

# 初期化 [randdic]
rd = randdic({"hoge": 23, "fuga": 47})
# 要素読み出し [randdic]
print(rd["hoge"])	# -> 23


## メイン機能: ランダムなkeyを1つ選ぶ (動作が非常に高速)
print(rd.rand())	# ランダムなキーを1つ選ぶ [randdic]


## その他、辞書が持っている機能は一通り持っている

# 表示 [randdic]
print(rd)
# default値つき要素読み出し
print(rd.get("moo", 0))	# -> 0
# 要素書き込み [randdic]
rd["k"] = "some_value"
# for文での利用
for k in rd:
	print(f"key = {k}, value = {str(rd[k])}")
# 要素数の参照 [randdic]
print(len(rd))
# 要素の削除 [randdic]
del rd["hoge"]
# 要素の存在確認 [randdic]
print("hoge" in rd)
# python辞書に似せるための諸機能 (dict()関数対応等に必要)
print(rd.keys())
print(rd.items())
print(rd.values())
# 同一性確認
print(rd == randdic())	# -> False
# 要素のupdate [randdic]
rd.update({"fuga": 48})	# 引数はranddic型でも良いし、通常の辞書でも良い


## 発展的用法: 内部で持っているハッシュテーブルを操作できる

# 内部のハッシュテーブルを見る
print(rd.table)
# keyに相当する内部indexを探し出す [randdic]
idx, found_flag = rd._get_idx("hoge")	# そのkeyが存在しない場合は、「それを追加するとしたらどこが良いか」を表す空き番地を返す
# keyの乱択は、localな乱数発生器等を渡すことができる
import random
r = random.Random()
print(rd.rand(r))

## 辞書要素管理一括テスト
import random
random.seed(23)
rand = random.random
# 適当な数
def rand_n():
	r = rand()*3
	return int(10 ** r)
# いくつかの要素を追加
def add_ele(d, rd):
	for _ in range(rand_n()):	# 適当な数
		k, v = rand(), rand()
		d[k], rd[k] = v, v
# いくつかの要素を削除
def del_ele(d, rd):
	for _ in range(rand_n()):	# 適当な数
		if len(d) == 0: return None
		k = random.choice(list(d))
		del d[k]
		del rd[k]
# 要素同一性のチェック
def check(d, rd):
	assert d == dict(rd)
	assert len(d) == len(rd)
	assert set(d) == set(rd)	# for文のチェック
	for k in d:
		assert d[k] == rd[k]
d = {}
rd = randdic()
n = 200
for i in range(n):
	add_ele(d, rd)	# いくつかの要素を追加
	check(d, rd)	# 要素同一性のチェック
	del_ele(d, rd)	# いくつかの要素を削除
	check(d, rd)
	# debug
	ele_n = len(rd)
	table_size = len(rd.table)
	print(f"[#{i}/{n}] ratio = {ele_n / table_size}, ele_n = {ele_n}, table_size = {table_size}")
