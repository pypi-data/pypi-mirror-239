# 高速乱択辞書 [randdic]

import sys
import fies
import math
import random
from sout import sout

# メモリ状態を表す特殊定数 (is比較した場合、他の値と重複しない)
class EMPTY: pass
class TOMBSTONE: pass

# default設定値
default_params = {
	"std_r": 0.30,	# 標準充填率 (初期化時の充填率)
	"lower_r": 0.15,	# 下限充填率
	"upper_r": 0.60,	# 上限充填率
	"lower_size": 8,	# 下限サイズ
}

# seed付きハッシュ関数 (python標準のhash関数を利用)
def seed_hash(
	obj,	# ハッシュ関数を掛ける対象のオブジェクト
	seed = 0,	# シード値
):
	return hash((seed, obj))

# 高速乱択辞書 [randdic]
class RandDic:
	# 初期化処理 [randdic]
	def __init__(self,
		init_dic_data = {},	# 初期化の原型とする辞書
		params = "default",	# 設定値 (defaultが推奨)
	):
		# default-paramsの設定
		self.params = (default_params if params == "default" else params)
		# 計数
		self.ele_n = 0	# 要素数 (墓地は含まず)
		self.tombstone_n = 0	# 墓地の数
		# 内部テーブルと初期要素の受け入れ
		self.rehash(init_dic_data)	# リハッシュ
	# 要素の取得 [randdic]
	def __getitem__(self, key):
		# keyに相当する内部indexを探し出す [randdic]
		idx, found_flag = self._get_idx(key)
		# 見つからなかった場合
		if found_flag is False: {}[key]	# keyエラー送出
		# valueを返す
		(_, value) = self.table[idx]
		return value
	# 要素の書き込み [randdic]
	def __setitem__(self, key, value):
		# keyに相当する内部indexを探し出す [randdic]
		idx, found_flag = self._get_idx(key)
		# 格納
		self.table[idx] = (key, value)
		# 要素数のインクリメント
		self.ele_n += 1
		# 拡大リハッシュ
		ex_r = (self.ele_n + self.tombstone_n) / len(self.table)	# 墓石も含む充填率
		if ex_r > self.params["upper_r"]: self.rehash(self)	# リハッシュ
	# 要素乱択 [randdic]
	def rand(self,
		rand_obj = "default",	# 乱数オブジェクト
	):
		# default乱数オブジェクトの定義
		if rand_obj == "default": rand_obj = random
		# 要素数ゼロの場合の例外
		if len(self) == 0: raise Exception("[randdic error] Cannot choose from an empty sequence.")
		# 要素を引き当てるまで乱択
		while True:
			e = rand_obj.choice(self.table)
			if e is EMPTY: continue
			if e is TOMBSTONE: continue
			key, value = e
			return key
	# 要素の存在確認 [randdic]
	def __contains__(self, key):
		# keyに相当する内部indexを探し出す [randdic]
		idx, found_flag = self._get_idx(key)
		return found_flag
	# 要素の削除 [randdic]
	def __delitem__(self, key):
		# keyに相当する内部indexを探し出す [randdic]
		idx, found_flag = self._get_idx(key)
		# 見つからなかった場合
		if found_flag is False: {}[key]	# keyエラー送出
		# 墓石を設置
		self.table[idx] = TOMBSTONE
		self.tombstone_n += 1
		# 要素数のデクリメント
		self.ele_n -= 1
		# 縮小リハッシュ
		ele_r = self.ele_n / len(self.table)	# 墓石を含まない充填率
		if ele_r < self.params["lower_r"]:
			new_size = math.ceil(self.ele_n/self.params["std_r"])	# 最低サイズ条件の確認
			if new_size >= self.params["lower_size"]: self.rehash(self)	# リハッシュ
	# 存在しない要素にも対応した要素取得 [randdic]
	def get(self, key, default_value = None):
		return (self[key] if key in self else default_value)
	# keyに相当する内部indexを探し出す [randdic]
	def _get_idx(self, key):
		# 開番地法で引き当てるまで繰り返す
		seed = -1
		while True:
			# 次の番地を探す
			seed += 1
			# hash値の計算
			hash_value = seed_hash(key, seed = seed)	# seed付きハッシュ関数 (python標準のhash関数を利用)
			# 読み出し
			idx = hash_value%len(self.table)
			res = self.table[idx]
			# 確認して返す
			if res is EMPTY: return idx, False	# not found
			if res is TOMBSTONE: continue	# 墓石はそのままスキップする
			(read_key, value) = res
			if read_key == key: return idx, True	# found
	# 要素数の参照
	def __len__(self):
		return self.ele_n
	# リハッシュ
	def rehash(self,
		init_dict_like	# 初期要素一覧 (dict()に対応したオブジェクト)
	):
		# init_dict_likeを辞書型に統一 (randdic自身もdict関数を受け付けることに注意)
		init_dict = dict(init_dict_like)
		# tableのsizeを決定
		new_size = math.ceil(len(init_dict)/self.params["std_r"])
		new_size = max(self.params["lower_size"], new_size)	# 最低サイズを確保
		# 墓石・要素数をリセット
		self.tombstone_n = 0
		self.ele_n = 0	# 下記のsetitemで再びインクリメントされる点に注意
		# tableの再定義
		self.table = [EMPTY for _ in range(new_size)]
		# 要素の格納 (この中ではリハッシュは起こらないことが想定されている)
		for k in init_dict: self[k] = init_dict[k]
	# for文での利用
	def __iter__(self):
		for e in self.table:
			if e is EMPTY: continue
			if e is TOMBSTONE: continue
			key, value = e
			yield key
	# 文字列化
	def __str__(self):
		# 計算量オーダー的にpython辞書での文字列化で問題ない
		return f"<randdic {str(dict(self))}>"
	# 第2文字列化
	def __repr__(self): return str(self)
	# 同一性演算子 [randdic]
	def __eq__(self, other):
		# まず型が違う場合はFalse
		if type(self) != type(other): return False
		# 大きさを比較する
		if len(self) != len(other): return False
		# 内容物を比較する
		for k in self:
			if self[k] != other[k]: return False
		# すべてのチェックに合格した場合は同一
		return True
	# 要素の更新 [randdic]
	def update(self, other):
		# 辞書型に統一
		dict_obj = dict(other)
		# 追加
		for k in other: self[k] = other[k]
	# python辞書に似せるための諸機能 (dict()関数対応等に必要)
	def keys(self): return [k for k in self]	# 間接的にiterを呼ぶ
	def items(self): return [(k, self[k]) for k in self]	# 間接的にiterを呼ぶ
	def values(self): return [self[k] for k in self]	# 間接的にiterを呼ぶ

# モジュールオブジェクトと「RandDic」クラスを同一視
sys.modules[__name__] = RandDic
