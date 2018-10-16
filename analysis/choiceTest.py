#!/usr/bin/python3

'''
choiceTest

各セッションに大報酬への選択率を試行ごとで表にまとめるスクリプト

'''

__author__ = "Qukoyk"
__contacts__ = "m172236@hiroshima-u.ac.jp"


# ファイル名
path = 'D:/Data/skinerData/box1/semiGBData/'
fileName = '2-semiGB-'
number = '31'


# 初期設定
rows = 0
position = 0
renzokuCounter = 0
bigList = []
bigCounter = 0
variableList = []
variableCounter = 0
positionList = []
positionListAll = []

leftList = []
rightList = []

leftCounter = 0
rightCounter = 0
trialsCounter = 0

trialsList = []
allCountList = []
bigCountList = []

pVariableList = []
# csvモジュールを導入
import csv

while int(number) <= 50:
    # 行数抽出
    with open(path + fileName + number + '.csv') as file:
        reader = csv.DictReader(file)
        for row in reader:
            rows = rows + 1
            pass
        pass
    print("ファイル" + fileName + number + '.csv' + "に", rows + 1, "行検出された")


    # 変動報酬と大報酬を抽出
    with open(path + fileName + number + '.csv') as file:
        reader = csv.DictReader(file)
        for row in reader:
            # 総試行数を累進
            if row['Trial'] != '' and row['LeverSide'] == 'left':
                leftCounter = row['Trial']
                leftList.append(int(leftCounter))
            if row['Trial'] != '' and row['LeverSide'] == 'right':
                rightCounter = row['Trial']
                rightList.append(int(rightCounter))
            trialsCounter = int(leftCounter) + int(rightCounter)
            # 変動報酬なら試行の番号を記録
            if row['Big/Small'] != '':
                variableList.append(trialsCounter)
                pass
            # 大報酬なら試行の番号を記録
            if row['Big/Small'] == '1':
                bigList.append(trialsCounter)
                pass
            # 試行累進
            position = position + 1
            pass
        pass

    # 次のファイルを読み込み前に変数をリセット
    number = int(number) + 1
    number = str(number)
    position = 0
    rows = 0


else:
    # 表頭書き込み
    headers = ['Trials','bigCounter','allCounter','pVariable']
    with open('neoTest.csv', 'w', newline='') as myfile:
        writer = csv.writer(myfile)
        writer.writerow(headers)
        pass
    # リスト内各試行の回数をカウントする
    for i in range(120):
        trialsList.append(i+1)
        allCountList.append(variableList.count(i+1))
        bigCountList.append(bigList.count(i+1))
        pVariableList.append(rightList.count(i+1))
        i = i + 1
        pass

    dataTransfer = [trialsList, bigCountList, allCountList, pVariableList]
    dataTransfer = list(zip(*dataTransfer))
    with open('neoTest.csv', 'a+', newline='') as myfile:
        writer = csv.writer(myfile)
        writer.writerows(dataTransfer)
        pass


print(bigCountList)
print(allCountList)
print(pVariableList)