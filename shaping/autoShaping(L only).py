#!/usr/bin/python3

'''
autoShaping(L only).py

AutoShaping　〜左レバーのみ版〜
'''

__author__ = "Qukoyk"
__contacts__ = "m172236@hiroshima-u.ac.jp"

x = 1 # FR x
timeMax = 60 * 60 #最大何分間
trialMax = 100 # 最大試行数

# import文
import RPi.GPIO as GPIO
from time import sleep
import time
import csv
import os,sys



'''
ポート設定部分

基礎ポートがどのスクリプトも共通するものです。
中央レバーポートとLEDポートはCongruentation課題に使われたLEDを統制するものです。

20180915まで、Box3 & Box1両方とも：

 house light ON: GPIO.HIGH
      buzzer ON: GPIO.HIGH
 left lever OUT: GPIO.LOW
right lever OUT: GPIO.LOW
    feeder TURN: GPIO.LOW
                          になります。
'''
# ポート宣言
# 基礎ポート
leverLeftAct = 22
leverLeftMove = 17
leverRightAct = 23
leverRightMove = 18
houseLight = 24
feeder = 27
buzzer = 25
handShaping = 5
# 中央レバー
leverMidMove = 13
leverMidAct = 23 # 右レバーと共用
# LED関係
lightLeft = 6
lightLeftAround = 19
lightMid = 20
lightMidAround = 21
lightRight = 12
lightRightAround = 16 # 16はずですが実験台では26

# ポートモード設定
GPIO.setmode(GPIO.BCM)
# 基礎ポート
GPIO.setup(feeder, GPIO.OUT, initial=GPIO.HIGH)
GPIO.setup(buzzer, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(leverLeftMove, GPIO.OUT, initial=GPIO.HIGH)
GPIO.setup(leverRightMove, GPIO.OUT, initial=GPIO.HIGH)
GPIO.setup(handShaping, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(houseLight, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(leverLeftAct, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(leverRightAct, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
# 中央レバー
GPIO.setup(leverMidMove, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(leverMidAct, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
# LED関係
GPIO.setup(lightLeft, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(lightLeftAround, GPIO.OUT, initial=GPIO.LOW) 
GPIO.setup(lightMid, GPIO.OUT, initial=GPIO.LOW) # 実験台はLOWがON。
GPIO.setup(lightMidAround, GPIO.OUT, initial=GPIO.LOW) # 実験台はLOWがON。
GPIO.setup(lightRight, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(lightRightAround, GPIO.OUT, initial=GPIO.LOW) # 実験台はLOWがON。



'''
変数宣言部分

変数やリストなどを事前宣言、設定するところ
'''
# データ関係
leverPressData = [] # レバーが押されたら記録をする（全反応）
leverActData = [] # 目標行動とその種類を表記（例えばFI10に10s後最初の反応）
leverData = [] # 押されたレバーは左か右かを記録
latencyData = [] # 潜時リストを記録
timeData = [] # 反応時間を記録
randomData = []

dataTransfer = [] # 行列変換用リスト
dataPosition = 0 # leverPressDataの最後の数字を基づいて，データをほかのリストに挿入する際に順番とする

myList = []

listPosition = 0
leverPressCounter = 0


# ファイルの保存先（ディレクトリ）
os.chdir('/home/pi/Desktop/kyoku/shapingData')

# 変数関係
leftRight = 0

react = 0
reactLeft = 0
reactRight = 0

reinforceYN = False # （変動報酬選択肢）強化するか否か。
reinforcers = 0 # 強化子の数を表す。0は小報酬、1は大報酬

leverLeftTrial = 0 # 左レバー押しのカウンター
leverRightTrial = 0 # 右レバー押しのカウンター
autoTrial = 0 # auto-shapingのカウンター

timeStart = time.time()  # 始まりの時間
timeNow = time.time()
timePast = 0
timeLatency = 0
timeTrial = time.time()
#day = time.strftime("%Y-%m-%d")

# 実験開始プロセス
answer2 = input("今回の番号は？:\n")
print("始めますか？")
answer = input("Press Space then Enter:\n")
waiting = True
while waiting:
    if answer == " ":
        print('\n'+"========START!========"+'\n')
        waiting = False

# 表頭書き込み
headers = ['Counter', 'LeverSide', 'Time', 'Trial', 'Latency']
with open(answer2 + '.csv', 'a+') as myfile:
    writer = csv.writer(myfile)
    writer.writerow(headers)
    pass

# 空き空間生成
for i in range(1000):
    leverActData.append('')
    latencyData.append('')
    randomData.append('')
    pass



'''
関数部分

いろんな関数を事前宣言するところ
'''
# レバー格納関数
def leverIn():
    GPIO.output(leverLeftMove, GPIO.HIGH)
    #GPIO.output(houseLight, GPIO.HIGH)
    pass

# レバー引き出し関数
def leverOut():
    GPIO.output(leverLeftMove, GPIO.LOW)
    #GPIO.output(houseLight, GPIO.LOW)
    pass

# チャタリング防止関数
def protect():
    while GPIO.input(leverLeftAct) == GPIO.HIGH or GPIO.input(leverRightAct) == GPIO.HIGH:
        sleep(0.01)
    pass

# CPUの使用率を下げる関数
def coolDown():
    sleep(0.01)
    pass
'''
「CPUの使用率を下げる関数」について

whileループは
「条件が達したらずっと繰り返す」ものですので、
もし「速度制限」がないと、CPUの計算力がすべて占用してループを行っちゃって、
タスクバーのCPU使用率モニタに常に25%になります（４コアの１コアが火力全開）。
ヒートシンクがないので、過熱防止のため、この関数が加えられた。
データの精度に影響がほとんどないので、安心に使ってください。
'''

# 餌やり関数
def reinforce(rewardKind): # sReward/mReward/lReward
    for i in range(rewardKind):
        GPIO.output(feeder, GPIO.LOW)
        GPIO.output(buzzer, GPIO.HIGH)
        sleep(0.3)
        GPIO.output(feeder, GPIO.HIGH)
        GPIO.output(buzzer, GPIO.LOW)
        sleep(0.3)
    pass

# データ保存関数
def dataSaving():
    # データを保存
    dataTransfer = [leverPressData, leverData, timeData, leverActData, latencyData]
    dataTransfer = list(zip(*dataTransfer))
    with open(answer2 + '.csv', 'a+') as myfile:
        writer = csv.writer(myfile)
        writer.writerows(dataTransfer)

# 「後片付け」関数
def bye():
    myfile.close() # 保存されたデータをちゃんと閉じる
    GPIO.cleanup() # ポートをリセット
    sys.exit() # プログラム停止
    pass



# 点灯！！
GPIO.output(houseLight, GPIO.HIGH)
leverOut()

# メインプログラム
try:
    while timeNow - timeStart < timeMax:
        timeNow = time.time()

        # 最大試行数になったか否か
        if leverLeftTrial + leverRightTrial + autoTrial >= trialMax:
            print("最大試行数に達して終了")
            print(timePast, "秒かかった")
            print("レバー押し　", leverLeftTrial, "　回")
            print("Auto Shaping　", autoTrial, "　回")
            dataSaving()
            bye()
            
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
            latencyData.append(timeLatency)
            # reactRight = 0 # 片方は不連続的なレバーを押しても認めるとコメントする
            # レバー押しの回数を保存
            leverPressData.append(leverPressCounter)
            # 左右を判明して保存
            leftRight = 'left'
            leverData.append(leftRight)
            print("反応", leverPressCounter)
            print("左レバー ", reactLeft, "/", x, '\n')
            protect()
            pass
            

        # FRを達成したら：
        if leftRight == 'left' and react == x: # 固定報酬選択肢
            react = 0
            leftRight = ''
            # 試行を累進
            leverLeftTrial = leverLeftTrial + 1
            leverActData.append(leverLeftTrial)
            # モニターに表せ
            print("レバー押し", leverLeftTrial)
            print("反応時間", timePast)
            print("反応潜時", timeLatency)
            print('\n'+'===================='+'\n')
            # 固定報酬ので強化文も一緒にここで書く
            reinforce(1)
            timeTrial = time.time()
            pass

        # AutoShaping
        if timeNow - timeTrial > 60:
            react = 0
            leverData.append('auto')
            timePast = round(timeNow - timeStart, 2)
            # 試行を累進
            autoTrial = autoTrial + 1
            leverActData.append(autoTrial)
            # モニターに表せ
            print("Auto Shaping", autoTrial)
            print("反応時間", timePast)
            print('\n'+'===================='+'\n')
            # 固定報酬ので強化文も一緒にここで書く
            reinforce(1)
            # レバーを一回格納・引き出せて、注意を喚起
            #leverIn()
            #sleep(0.5)
            #leverOut()
            timeTrial = time.time()
            pass

        coolDown()
            
    
    # 最大時間になったか否か
    else:
        print("最大時間に達して終了")
        print("レバー押し　", leverLeftTrial, "　回")
        print("Auto Shaping　", autoTrial, "　回")
        dataSaving()
        bye()
# 終了
except KeyboardInterrupt:
    pass

# ポート釈放
dataSaving()
bye()
