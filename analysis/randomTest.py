#!/usr/bin/python3

'''
randomTest.py

各セッションに生成された乱数列中試行ごとの大報酬の回数を表にまとめるスクリプト

'''

__author__ = "Qukoyk"
__contacts__ = "m172236@hiroshima-u.ac.jp"


# ファイル名
path = 'D:/Data/skinerData/box1/gbData/'
fileName = '5-GB-'
number = '23'


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

randomList = []
# csvモジュールを導入
import csv
while int(number) <= 39:

    with open(path + fileName + number + '_randomList.csv') as file:
        reader = csv.reader(file)
        for row in reader:
            randomList =row
            pass

    with open('randomTest.csv', 'a+', newline='') as myfile:
        writer = csv.writer(myfile)
        writer.writerow(randomList)
        pass

    number = int(number) + 1
    number = str(number)
