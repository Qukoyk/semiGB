#!/usr/bin/python3

'''
autoShapingL10R10.py

行動形成用スクリプト　〜FR2左右強制交替版〜
	・FR2
	・左１０回 → 右１０回　の強制選択
	・計左５０回＆右５０回総計１００回
'''

__author__ = "Qukoyk"
__contacts__ = "m172236@hiroshima-u.ac.jp"

x = 2 # FR x
iti = 0
sideThreshold = 10 #片方最大１０回連続

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

os.chdir('/home/pi/Desktop/kyoku/autoShapingData')

react = 0

sideLeft = 0
sideRight = 0

timeTrial = 60 #1試行60秒
timeMax = timeTrial * 60 #1分間
leverLeftTrial = 0 # 左レバー押しのカウンター
leverRightTrial = 0 # 右レバー押しのカウンター
autoTrial = 0 # autoのカウンター
leverLeftMax = 50 # 左レバーの最大回数
leverRightMax = 50 # 右レバーの最大回数
trialMax = leverLeftMax + leverRightMax # 総最大回数

trial = 0
time0 = time.time()  # 始まりの時間
time1 = time.time()
timePast = 0
timeNow = time.time()
timeLast = time.time()
#day = time.strftime("%Y-%m-%d")
with open(answer2 + '.csv', 'a+') as myfile:
    writer = csv.writer(myfile)
    writer.writerow(['Trial', 'Switches', 'Time'])

# データ保存先を指定
leverData = []


GPIO.output(leverLeftMove, GPIO.LOW)
GPIO.output(leverRightMove, GPIO.LOW)
GPIO.output(houseLight, GPIO.LOW)

def bye():
    myfile.close()
    GPIO.cleanup()
    sys.exit()
    pass

# メインプログラム
try:
    while True:

        while timeNow - time0 < timeMax:
            timeNow = time.time()

            if timeNow - timeLast < timeTrial:
                if (GPIO.input(leverLeftAct) == GPIO.HIGH and leverLeftTrial < leverLeftMax and sideLeft < sideThreshold):
                    react = react + 1
                    print(react, "/", x)
                    if (react == x and sideLeft < sideThreshold):
                        react = 0
                        sideRight = 10
                        sideLeft = sideLeft + 1
                        if sideLeft == sideThreshold:
                            sideRight = 0
                            pass
                        GPIO.output(feeder, GPIO.LOW)
                        time1 = time.time()
                        timePast = round(time1 - time0, 2)
                        timeLast = time.time()
                        trial = trial + 1
                        leverLeftTrial = leverLeftTrial + 1
                        sleep(0.1)
                        GPIO.output(feeder, GPIO.HIGH)
                        print("Lever Left Trial", leverLeftTrial)
                        print("Time ", timePast, '\n')
                        leverData = [str(trial), str("Left Lever"), str(timePast)]
                        with open(answer2 + '.csv', 'a+') as myfile:
                            writer = csv.writer(myfile)
                            writer.writerow(leverData)
                        pass
                    while GPIO.input(leverLeftAct) == GPIO.HIGH:
                        sleep(0.01)

                elif (GPIO.input(leverRightAct) == GPIO.HIGH and leverRightTrial < leverRightMax and sideRight < sideThreshold):
                    react = react + 1
                    print(react, "/", x)
                    if (react == x and sideRight < sideThreshold):
                        react = 0
                        sideLeft = sideThreshold
                        sideRight = sideRight + 1
                        if sideRight == sideThreshold:
                            sideLeft = 0
                            pass
                        GPIO.output(feeder, GPIO.LOW)
                        time1 = time.time()
                        timePast = round(time1 - time0, 2)
                        timeLast = time.time()
                        trial = trial + 1
                        leverRightTrial = leverRightTrial + 1
                        sleep(0.1)
                        GPIO.output(feeder, GPIO.HIGH)
                        print("Lever Right Trial", leverRightTrial)
                        print("Time ", timePast, '\n')
                        leverData = [str(trial), str("Right Lever"), str(timePast)]
                        with open(answer2 + '.csv', 'a+') as myfile:
                            writer = csv.writer(myfile)
                            writer.writerow(leverData)
                    while GPIO.input(leverRightAct) == GPIO.HIGH:
                        sleep(0.01)
                    
                if leverLeftTrial + leverRightTrial >= trialMax:
                    print("最大試行数に達して終了")
                    print(timePast, "秒かかった")
                    bye()

            else:
                GPIO.output(feeder, GPIO.LOW)
                time1 = time.time()
                timeLast = time.time()
                timePast = round(time1 - time0, 2)
                trial = trial + 1
                autoTrial = autoTrial + 1
                sleep(0.1)
                GPIO.output(feeder, GPIO.HIGH)
                print ("Auto Trial ", autoTrial)
                print("Time ", timePast, '\n')
                leverData = [str(trial), str("Auto Trial"), str(timePast)]
                with open(answer2 + '.csv', 'a+') as myfile:
                    writer = csv.writer(myfile)
                    writer.writerow(leverData)

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
