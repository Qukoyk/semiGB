#!/usr/bin/python3

'''
leverClean.py

レバーを清掃するためにレバーを出し放しスクリプト

'''

__author__ = "Qukoyk"
__contacts__ = "m172236@hiroshima-u.ac.jp"


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

# ポート設定
GPIO.setmode(GPIO.BCM)
GPIO.setup(feeder, GPIO.OUT)
GPIO.setup(buzzer, GPIO.OUT)
GPIO.setup(leverLeftMove, GPIO.OUT)
GPIO.setup(leverRightMove, GPIO.OUT)
GPIO.setup(lightLeft, GPIO.OUT)
GPIO.setup(lightRight, GPIO.OUT)
GPIO.setup(houseLight, GPIO.OUT)
GPIO.setup(leverLeftAct, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(leverRightAct, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(handShaping, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

# initial settings
GPIO.output(houseLight, GPIO.LOW)
GPIO.output(leverLeftMove, GPIO.HIGH)
GPIO.output(leverRightMove, GPIO.HIGH)
GPIO.output(buzzer, GPIO.LOW)
GPIO.output(feeder, GPIO.LOW)

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
GPIO.output(leverLeftMove, GPIO.LOW)
GPIO.output(leverRightMove, GPIO.LOW)
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
