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
GPIO.setup(leverLeftMove, GPIO.OUT)
GPIO.setup(leverRightMove, GPIO.OUT)
GPIO.setup(lightLeft, GPIO.OUT)
GPIO.setup(lightRight, GPIO.OUT)
GPIO.setup(houseLight, GPIO.OUT)
GPIO.setup(leverLeftAct, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(leverRightAct, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(handShaping, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

GPIO.output(leverLeftMove, GPIO.HIGH)
GPIO.output(leverRightMove, GPIO.HIGH)

# 関数設定
def begin(equipmentName):
    print("\n", equipmentName, "番ポートテスト開始")
    pass


def confirm(equipmentName):
    print("\n", "異常がないと y を押してください")
    answer = input("Press y:\n")
    while True:
        if answer == "y":
            print("\n", "=====", str(equipmentName), "番ポート異常なし", "=====", "\n")
            break
    pass


def test(equipmentName):
    GPIO.output(equipmentName, GPIO.LOW)
    sleep(1)
    GPIO.output(equipmentName, GPIO.HIGH)
    sleep(1)
    GPIO.output(equipmentName, GPIO.LOW)
    sleep(1)
    GPIO.output(equipmentName, GPIO.HIGH)
    sleep(1)
    pass


def test2(equipmentName):
    GPIO.output(equipmentName, GPIO.HIGH)
    sleep(1)
    GPIO.output(equipmentName, GPIO.LOW)
    sleep(1)
    GPIO.output(equipmentName, GPIO.HIGH)
    sleep(1)
    GPIO.output(equipmentName, GPIO.LOW)
    sleep(1)
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
# houseLight
begin("House Light")
test(houseLight)
confirm("House Light")

# leverLeftMove
begin("Left Lever in-out")
test(leverLeftMove)
confirm("Left Lever in-out")

# leverRightMove
begin("Right Lever in-out")
test(leverRightMove)
confirm("Right Lever in-out")

# feeder
begin("Feeder")
test(feeder)
confirm("Feeder")

print("\n", "\n", "\n", "実験箱異常ありませんでした")
# ポート釈放
GPIO.cleanup()
