#!/usr/bin/python3

'''
boxTest.py

実験箱検査スクリプト

'''

__author__ = "Qukoyk"
__contacts__ = "m172236@hiroshima-u.ac.jp"


# ポート宣言
leverLeftAct = 22
leverLeftMove = 17
leverRightAct = 23
leverRightMove = 18
houseLight = 24
feeder = 27
buzzer = 25
handShaping = 5
# LED部分のポート宣言
lightLeft = 6
lightLeftAround = 19
lightMid = 20
lightMidAround = 21
lightRight = 12
lightRightAround = 16 # 16はずですが実験台では26

leverMidMove = 13
leverMidAct = 23 # same to leverRightAct


# import文
import RPi.GPIO as GPIO
from time import sleep
import time

# ポート設定
GPIO.setmode(GPIO.BCM)
GPIO.setup(feeder, GPIO.OUT, initial=GPIO.HIGH)
GPIO.setup(buzzer, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(leverLeftMove, GPIO.OUT, initial=GPIO.HIGH)
GPIO.setup(leverRightMove, GPIO.OUT, initial=GPIO.HIGH)
GPIO.setup(handShaping, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(houseLight, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(lightLeft, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(lightLeftAround, GPIO.OUT, initial=GPIO.LOW) 
GPIO.setup(lightMid, GPIO.OUT, initial=GPIO.LOW) # 実験台はLOWがON。
GPIO.setup(lightMidAround, GPIO.OUT, initial=GPIO.LOW) # 実験台はLOWがON。
GPIO.setup(lightRight, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(lightRightAround, GPIO.OUT, initial=GPIO.LOW) # 実験台はLOWがON。

GPIO.setup(leverMidMove, GPIO.OUT, initial=GPIO.LOW)

GPIO.setup(leverLeftAct, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(leverRightAct, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

GPIO.setup(leverMidAct, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)


# 関数設定
def begin(equipmentName):
    print("\n", equipmentName, "テスト開始")
    pass


# 検査開始
print("\n" + "設備検査プログラム")
print("パーツは2回 点滅/動く のは正常状態", "\n", "\n", "\n")
print("始めますか？")
answer = input("Press y:\n")
while True:
    if answer == "y":
        print("\n", "=======START!=======", "\n")
        break
    else:
        sleep(0.1)


# メインプログラム

GPIO.output(houseLight, GPIO.HIGH)

try:
    while True:
        sleep(1)
except KeyboardInterrupt:
    pass

# ポート釈放
GPIO.output(houseLight, GPIO.LOW)
GPIO.output(leverLeftMove, GPIO.HIGH)
GPIO.output(leverRightMove, GPIO.HIGH)
GPIO.cleanup()
