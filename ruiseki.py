#!/usr/bin/python3

'''
ruiseki.py

「無報酬/小報酬が何回連続あった後固定報酬に移るか及びそれぞれの度数を累算する」プログラム
です！

'''

__author__ = "Qukoyk"
__contacts__ = "m172236@hiroshima-u.ac.jp"


# ファイル名
path = 'F:/実験2018/kyoku/GB-semiGB/Exp1/'
fileName = '4-GB-37'


# 初期設定
rows = 0
position = 0
renzokuCounter = 0
renzokuList = [] # 位置対応リスト → 後ろに直接追加可
renzokuList2 = [] # 位置対応しないリスト → まとめ用
renzokuListAll = [] # 位置対応リスト → 後ろに直接追加可
renzokuListAll2 = [] # 位置対応しないリスト → まとめ用
positionList = []
positionListAll = []

# csvモジュールを導入
import csv

# 行数抽出
with open(path + fileName + '.csv') as file:
    reader = csv.DictReader(file)
    for row in reader:
        rows = rows + 1
# 空き空間生成        
for i in range(rows):
    renzokuList.append('')
    renzokuListAll.append('')
    pass

print("ファイルに", rows + 1, "行検出された")

# 移行された移行を抽出 → 移行率の分子とする
with open(path + fileName + '.csv') as file:
    reader = csv.DictReader(file)
    for row in reader:
        # 小報酬試行なら累積
        if row['Big/Small'] == '0':
            renzokuCounter = renzokuCounter + 1
            pass
        # 大報酬試行なら累積をリセット
        elif row['Big/Small'] == '1' and renzokuCounter != 0 and row['Trial'] != '':
            renzokuCounter = 0
            pass
        # 固定報酬選択肢に移ると記録
        elif row['LeverSide'] == 'left' and renzokuCounter != 0 and row['Trial'] != '':
            # print("positionNow = ", position)
            renzokuList.insert(position, renzokuCounter) # 前の試行を記録　その１
            renzokuList2.append(renzokuCounter) # 前の試行を記録　その２
            positionList.append(position)
            renzokuCounter = 0
            pass
        # 試行累進
        position = position + 1
        pass

# 累進リセット
position = 0
renzokuCounter = 0

# 小報酬の連続回数を抽出 →　移行率の分母とする
with open(path + fileName + '.csv') as fileAll:
    reader = csv.DictReader(fileAll)
    for row in reader:
        # 小報酬なら累進
        if row['Big/Small'] == '0':
            renzokuCounter = renzokuCounter + 1
            pass
        
# 大報酬あるいは固定報酬に移ると記録してリセット
        elif (row['Big/Small'] == '1' or row['LeverSide'] == 'left') and renzokuCounter != 0 and row['Trial'] != '': 
            print(renzokuCounter, "回連続のposition = ", position)
            renzokuListAll.insert(position, renzokuCounter)
            renzokuListAll2.append(renzokuCounter)
            positionListAll.append(position)
            renzokuCounter = 0
            pass
        # 試行累進
        position = position + 1
        pass
        
# print(renzokuList)
# print(renzokuListAll)
print("移行された", renzokuList2)
print("position= ", positionList)
# print("　　　　全部", renzokuListAll2)
# print("position= ", positionListAll)

# 度数を累算する関数
def matome(repeat):
    a = renzokuList2.count(repeat)
    b = renzokuListAll2.count(repeat)
    if renzokuListAll2.count(repeat) != 0:
        print("無報酬", repeat, "回連続で移行することが", renzokuList2.count(repeat), "　ある",
              "移行率", round(a/b*100,2), "%", '\t', "(", a, "/", b, ")")
        pass
    pass

# 最大連続数と取って、それぞれを累算する
print('\n' + fileName, "に：")
for i in range(max(renzokuListAll2)):
    matome(i + 1)
    pass


