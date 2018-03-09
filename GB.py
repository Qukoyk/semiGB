#!/usr/bin/python3

'''
GB.py

GB課題プログラム
'''

__author__ = "Qukoyk"
__contacts__ = "m172236@hiroshima-u.ac.jp"

x = 2 # FR x
iti = 30
timeMax = 70 * 60 #最大何分間
trialMax = 100 # 最大試行数

sReward = 0 # 変動小報酬の粒数
mReward = 1 # 固定中報酬の粒数
lReward = 2 # 変動大報酬の粒数

# ポート宣言
leverLeftAct = 22
leverLeftMove = 17
leverRightAct = 23
leverRightMove = 18
lightLeft = 6
lightRight = 12
houseLight = 24
feeder = 27
buzzer = 25
handShaping = 5

# import文
import RPi.GPIO as GPIO
from time import sleep
import time
import csv
import math,random
import os,sys

# ポート設定
GPIO.setmode(GPIO.BCM)
GPIO.setup(feeder, GPIO.OUT)
GPIO.setup(buzzer, GPIO.OUT)
GPIO.setup(leverLeftMove, GPIO.OUT)
GPIO.setup(leverRightMove, GPIO.OUT)
GPIO.setup(handShaping, GPIO.OUT)
GPIO.setup(houseLight, GPIO.OUT)
GPIO.setup(leverLeftAct, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(leverRightAct, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)


# データ保存先を指定
leverPressData = [] # レバーが押されたら記録をする（全反応）
leverActData = [] # 目標行動とその種類を表記（例えばFI10に10s後最初の反応）
leverData = [] # 押されたレバーは左か右かを記録
latencyData = [] # 潜時リストを記録
timeData = [] # 反応時間を記録
randomData = [] # 報酬種類を表す乱数を記録

dataTransfer = [] # 行列変換用リスト

dataPosition = 0 # leverPressDataの最後の数字を基づいて，データをほかのリストに挿入する際に順番とする

myList = []

listPosition = 0
leverPressCounter = 0


def leverIn():
    GPIO.output(leverLeftMove, GPIO.HIGH)
    GPIO.output(leverRightMove, GPIO.HIGH)
    #GPIO.output(houseLight, GPIO.HIGH)
    pass

def leverOut():
    GPIO.output(leverLeftMove, GPIO.LOW)
    GPIO.output(leverRightMove, GPIO.LOW)
    #GPIO.output(houseLight, GPIO.LOW)
    pass

def protect():
    while GPIO.input(leverLeftAct) == GPIO.HIGH or GPIO.input(leverRightAct) == GPIO.HIGH:
        sleep(0.01)
    pass

def chickenDinner():
    for i in range(9):
        GPIO.output(buzzer, GPIO.HIGH)
        sleep(0.15)
        GPIO.output(buzzer, GPIO.LOW)
        sleep(0.15)
    pass

def reinforce(rewardKind): # sReward/mReward/lReward
    for i in range(rewardKind):
        GPIO.output(feeder, GPIO.LOW)
        GPIO.output(buzzer, GPIO.HIGH)
        sleep(0.5)
        GPIO.output(feeder, GPIO.HIGH)
        GPIO.output(buzzer, GPIO.LOW)
        sleep(0.5)
    pass

def dataSaving():
    # データを保存
    dataTransfer = [leverPressData, leverData, timeData, leverActData, latencyData, randomData]
    dataTransfer = list(zip(*dataTransfer))
    with open(answer2 + '.csv', 'a+') as myfile:
        writer = csv.writer(myfile)
        writer.writerows(dataTransfer)
    # 生成された乱数列を保存
    randomList = list(zip(*myList))
    with open(answer2 + '_randomList.csv', 'a+') as myfile2:
        writer = csv.writer(myfile2)
        writer.writerow(randomList)
    pass

def bye():
    myfile.close()
    GPIO.cleanup()
    sys.exit()
    pass

# 空き空間生成
for i in range(1000):
    leverActData.append('')
    latencyData.append('')
    randomData.append('')
    pass

# 乱数生成
print("乱数生成中……")

for i in range(0,50): # 0（小報酬）を50回生成、数列になる
    myList.append(0)
    pass
    
for i in range(0,50): # 1（大報酬）を50回生成
    myList.insert(random.randint(1,50),1) # そして0の数列にランダムで挿入
    pass
    
print(myList)
            

# 実験開始プロセス
answer2 = input("今回の番号は？:\n")
print("始めますか？")
answer = input("Press y:\n")
while True:
    if answer == "y":
        print("")
        print("=======START!========")
        print("")
        break
    else:
        sleep(0.1)


# 初期化数据

os.chdir('/home/pi/Desktop/kyoku/gbData')

leftRight = 0

react = 0
reactLeft = 0
reactRight = 0

reinforceYN = 0 # （変動報酬選択肢）強化するか否か。0は不強化、1は強化 "Yes or Not"
reinforcers = 0 # 強化子の数を表す。0は小報酬、1は大報酬

leverLeftTrial = 0 # 左レバー押しのカウンター
leverRightTrial = 0 # 右レバー押しのカウンター

trial = 0
timeStart = time.time()  # 始まりの時間
timeNow = time.time()
timePast = 0
timeLatency = 0
timeTrial = time.time()
#day = time.strftime("%Y-%m-%d")

headers = ['Counter', 'LeverSide', 'Time', 'Trial', 'Latency', 'Big/Small']
with open(answer2 + '.csv', 'a+') as myfile:
    writer = csv.writer(myfile)
    writer.writerow(headers)

# ポート初期化
GPIO.output(buzzer, GPIO.LOW)
GPIO.output(feeder, GPIO.HIGH)
GPIO.output(leverLeftMove, GPIO.LOW)
GPIO.output(leverRightMove, GPIO.LOW)
GPIO.output(houseLight, GPIO.HIGH)

# メインプログラム
try:
    while timeNow - timeStart < timeMax:
        # timeNow = time.time()

        # レバー押しを測る
        if reactLeft == x or reactRight == x:
            react = x
            reactLeft = 0
            reactRight = 0
            pass
        if GPIO.input(leverLeftAct) == GPIO.HIGH:
            # 回数の累進
            leverPressCounter = leverPressCounter + 1
            reactLeft = reactLeft + 1
            # 時間を計って保存
            timeNow = time.time()
            timePast = round(timeNow - timeStart, 2)
            timeData.append(timePast)
            timeLatency = round(timeNow - timeTrial, 2)
            latencyData.insert(leverPressCounter - 1, timeLatency)
            # reactRight = 0 # 片方は不連続的なレバーを押しても認めるとコメントする
            # レバー押しの回数を保存
            leverPressData.append(leverPressCounter)
            # 左右を判明して保存
            leftRight = 'left'
            leverData.append(leftRight)
            print("第", leverPressCounter, "回", timePast)
            print("timeLatency", timeLatency, '\n')
            print("左レバー ", reactLeft, "/", x, '\n')
            protect()
            pass
        elif GPIO.input(leverRightAct) == GPIO.HIGH:
            # 回数の累進
            leverPressCounter = leverPressCounter + 1
            reactRight = reactRight + 1
            # 時間を計って保存
            timeNow = time.time()
            timePast = round(timeNow - timeStart, 2)
            timeData.append(timePast)
            timeLatency = round(timeNow - timeTrial, 2)
            latencyData.insert(leverPressCounter - 1, timeLatency)
            # reactLeft = 0 # 片方は不連続的なレバーを押しても認めるとコメントする
            # レバー押しの回数を保存
            leverPressData.append(leverPressCounter)
            # 左右を判明して保存
            leftRight = 'right'
            leverData.append(leftRight)
            print("第", leverPressCounter, "回", timePast)
            print("timeLatency", timeLatency, '\n')
            print("右レバー ", reactRight, "/", x, '\n')
            protect()
            pass
            

        # FRを達成したら：
        if leftRight == 'left': # 固定報酬選択肢
            if react == x:
                leverIn()
                react = 0
                # 乱数を累進する
                listPosition = listPosition + 1
                # 時間を測る
                timeNow = time.time()
                timePast = round(timeNow - timeStart, 2)
                # 試行を累進
                trial = trial + 1
                leverLeftTrial = leverLeftTrial + 1
                leverActData.insert(leverPressCounter - 1, leverLeftTrial)
                # モニターに表せ
                print("固定報酬", leverLeftTrial)
                print("timePast ", timePast)
                print("timeLatency", timeLatency, '\n')
                # 固定報酬ので強化文も一緒にここで書く
                reinforce(mReward)
                # レバー引き込みとITI
                sleep(iti)
                leverOut()
                protect()
                timeTrial = time.time()


        elif leftRight == 'right': #変動報酬選択肢
            if react == x:
                leverIn()
                react = 0
                # 強化
                reinforceYN = 1 # 強化する
                reinforcers = myList[listPosition] # 乱数リストから今回の報酬種類を読み取り
                # 乱数を累進する
                listPosition = listPosition + 1
                # 時間を測る
                timeNow = time.time()
                timePast = round(timeNow - timeStart, 2)
                # 試行を累進する
                trial = trial + 1
                leverRightTrial = leverRightTrial + 1
                leverActData.insert(leverPressCounter - 1, leverRightTrial)
                randomData.insert(leverPressCounter - 1 , reinforcers)
                # モニターに表せ
                print("変動報酬", leverRightTrial)
                print("timePast ", timePast)
                print("timeLatency ", timeLatency, '\n')
                
                # 変動報酬選択肢のレバー引き込み＆ITIは給餌分のあとにある

        # 変動報酬給餌文
        if reinforceYN == 1:
            if reinforcers == 0:
                print("小報酬",'\n','\n')
                reinforce(sReward)
                reinforceYN = 0
                sleep(iti)
                leverOut()
                protect()
                timeTrial = time.time()
                pass
            else:
                print("大報酬",'\n','\n')
                chickenDinner()
                reinforce(lReward)
                reinforceYN = 0
                reinforcers = 0
                sleep(iti)
                leverOut()
                protect()
                timeTrial = time.time()
                
        # 最大試行数になったか否か
        if leverLeftTrial + leverRightTrial >= trialMax:
            print("最大試行数に達して終了")
            print(timePast, "秒かかった")
            print("左レバー　", leverLeftTrial, "　回")
            print("右レバー　", leverRightTrial, "　回")
            dataSaving()
            bye()
            
        # 4試行の強制選択に間違ったレバーを選んだら"Wrong Lever"をモニターに表す
        if react == x:
            react = 0
            print("Wrong Lever", '\n')
    
    # 最大時間になったか否か
    else:
        print("最大時間に達して終了")
        print("左レバー　", leverLeftTrial, "　回")
        print("右レバー　", leverRightTrial, "　回")
        dataSaving()
        bye()
# 終了
except KeyboardInterrupt:
    pass

# ポート釈放
dataSaving()
bye()
