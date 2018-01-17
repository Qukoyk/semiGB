#!/usr/bin/python3

'''
GB.py

GB課題プログラム
'''

__author__ = "Qukoyk"
__contacts__ = "m172236@hiroshima-u.ac.jp"

x = 2 # FR x
iti = 30

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

GPIO.output(leverLeftMove, GPIO.HIGH)
GPIO.output(leverRightMove, GPIO.HIGH)
GPIO.output(feeder, GPIO.HIGH)


# データ保存先を指定
leverData = []
myList = []
listPosition = 0


GPIO.output(leverLeftMove, GPIO.LOW)
GPIO.output(leverRightMove, GPIO.LOW)
GPIO.output(houseLight, GPIO.LOW)

def leverIn():
    GPIO.output(leverLeftMove, GPIO.HIGH)
    GPIO.output(leverRightMove, GPIO.HIGH)
    pass

def leverOut():
    GPIO.output(leverLeftMove, GPIO.LOW)
    GPIO.output(leverLeftMove, GPIO.HIGH)
    pass

def bye():
    myfile.close()
    GPIO.cleanup()
    sys.exit()
    pass


#乱数生成
print("乱数生成中……")

for i in range(0,50): # 0（無報酬）を50回生成、数列になる
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

#~ os.chdir('/home/pi/Desktop/kyoku/gbData')

react = 0

reinforce = 0 # （変動報酬選択肢）強化するか否か。0は不強化、1は強化
reinforcers = 0 # 強化子の数を表す。0は無報酬、1は大報酬

timeTrial = 60 #1試行60秒
timeMax = timeTrial * 60 #最大何分間
leverLeftTrial = 0 # 左レバー押しのカウンター
leverRightTrial = 0 # 右レバー押しのカウンター
autoTrial = 0 # autoのカウンター

trialMax = 100 # 最大試行数

trial = 0
time0 = time.time()  # 始まりの時間
time1 = time.time()
timePast = 0
timeLatency = 0
timeTrial = time.time()
#day = time.strftime("%Y-%m-%d")
with open(answer2 + '.csv', 'a+') as myfile:
    writer = csv.writer(myfile)
    writer.writerow(['Trial', 'Switches', 'Time'])



# メインプログラム
try:
    while True:

        while time1 - time0 < timeMax:
            time1 = time.time()


            if ((trial < 2 or trial >= 4) and GPIO.input(leverLeftAct) == GPIO.HIGH): # 固定報酬選択肢
                react = react + 1
                print(react, "/", x)
                if react == x:
                    leverIn()
                    react = 0
                    GPIO.output(feeder, GPIO.LOW) # 固定1粒
                    sleep(0.1)
                    GPIO.output(feeder, GPIO.HIGH)
                    listPosition = listPosition + 1
                    time1 = time.time()
                    timePast = round(time1 - time0, 2)
                    timeLatency = round(time1 - timeTrial, 2)
                    trial = trial + 1
                    leverLeftTrial = leverLeftTrial + 1
                    sleep(0.1)
                    GPIO.output(feeder, GPIO.HIGH)
                    print("固定報酬", leverLeftTrial)
                    print("timePast ", timePast)
                    print("timeLatency ", timeLatency, '\n')
                    leverData = [str(trial), str("Left Lever"), str(timePast)]
                    with open(answer2 + '.csv', 'a+') as myfile:
                        writer = csv.writer(myfile)
                        writer.writerow(leverData)
                    pass
                    sleep(iti)
                    leverOut()
                while GPIO.input(leverLeftAct) == GPIO.HIGH:
                    sleep(0.01)

            elif (GPIO.input(leverRightAct) == GPIO.HIGH and trial >= 2): #変動報酬選択肢
                react = react + 1
                print(react, "/", x)
                if (react == x):
                    leverIn()
                    react = 0
                    reinforce = 1
                    reinforcers = myList[listPosition]
                    listPosition = listPosition + 1
                    time1 = time.time()
                    timePast = round(time1 - time0, 2)
                    timeLatency = round(time1 - timeTrial, 2)
                    trial = trial + 1
                    leverRightTrial = leverRightTrial + 1
                    sleep(0.1)
                    GPIO.output(feeder, GPIO.HIGH)
                    print("変動報酬", leverRightTrial)
                    print("timePast ", timePast)
                    print("timeLatency ", timeLatency, '\n')
                    leverData = [str(trial), str("Right Lever"), str(timePast)]
                    with open(answer2 + '.csv', 'a+') as myfile:
                        writer = csv.writer(myfile)
                        writer.writerow(leverData)
                        pass
                while GPIO.input(leverRightAct) == GPIO.HIGH:
                    sleep(0.01)
            
            if reinforce == 1:
                if reinforcers == 0:
                    reinforce = 0
                    print("無報酬",'\n','\n')
                    sleep(iti)
                    leverOut()
                    pass
                else:
                    for i in range(2):
                        GPIO.output(feeder, GPIO.LOW)
                        sleep(0.5)
                        GPIO.output(feeder, GPIO.HIGH)
                        sleep(0.5)
                    print("大報酬",'\n','\n')
                    reinforce = 0
                    reinforcers = 0
                    sleep(iti)
                    leverOut()
                    pass
                    
            if leverLeftTrial + leverRightTrial >= trialMax:
                print("最大試行数に達して終了")
                print(timePast, "秒かかった")
                bye()

            sleep(0.1)
        else:
            print("最大時間に達して終了")
            print("左レバー　", leverLeftTrial, "　回")
            print("右レバー　", leverRightTrial, "　回")
            bye()
# 終了
except KeyboardInterrupt:
    pass

# ポート釈放
bye()
