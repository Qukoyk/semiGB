#!/usr/bin/python3

'''
ruiseki.py

「無報酬/小報酬が何回連続あった後固定報酬に移るか及びそれぞれの度数を累算する」プログラム
です！

'''

__author__ = "Qukoyk"
__contacts__ = "m172236@hiroshima-u.ac.jp"


# ファイル名
fileName = '1-GB-33'


# 初期設定
position = 0
renzokuCounter = 0
renzokuList = [] # 位置対応リスト → 後ろに直接追加可
renzokuList2 = [] # 位置対応しないリスト → まとめ用

# csvモジュールを導入
import csv

# 空き空間生成
for i in range(300):
    renzokuList.append('')
    pass


with open('F:/実験2018/kyoku/GB-semiGB/Exp1/' + fileName + '.csv') as file:
    reader = csv.DictReader(file)
    for row in reader:
        # 小報酬試行なら累積
        if row['Big/Small'] == '0':
            renzokuCounter = renzokuCounter + 1
        # 大報酬試行なら累積をリセット
        elif row['Big/Small'] == '1' and renzokuCounter != 0 and row['Trial'] != '':
            renzokuCounter = 0
        # 固定報酬選択肢に移ると記録
        elif row['LeverSide'] == 'left' and renzokuCounter != 0 and row['Trial'] != '':
            renzokuList.insert(position, renzokuCounter) # 前の試行を記録　その１
            renzokuList2.append(renzokuCounter) # 前の試行を記録　その２
            renzokuCounter = 0
        # 試行累進
        position = position + 1
        pass
        
# print(renzokuList)
# print(renzokuList2)

# 度数を累算する関数
def matome(repeat):
    a = renzokuList2.count(repeat)
    print("無報酬", repeat, "回連続で移行することが", renzokuList2.count(repeat), "　ある")
    pass

# 最大連続数と取って、それぞれを累算する
print('\n' + fileName, "に：")
for i in range(max(renzokuList2)):
    matome(i + 1)
    pass
