#!/usr/bin/python3

'''
semiGB.py

semiGB課題プログラム
'''

__author__ = "Qukoyk"
__contacts__ = "m172236@hiroshima-u.ac.jp"

x = 2 # FR x
iti = 30
timeMax = 70 * 60 #最大何分間
trialsMax = 100 # 最大試行数

sReward = 1 # 変動小報酬の粒数
mReward = 2 # 固定中報酬の粒数
lReward = 3 # 変動大報酬の粒数

# import文
import RPi.GPIO as GPIO
from time import sleep
import time
import csv
import math,random, numpy
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

randList = []

listPosition = 0
leverPressCounter = 0


# ファイルの保存先（ディレクトリ）
os.chdir('/home/pi/Desktop/kyoku/semiGBData')

# 変数関係
leftRight = 0

react = 0
reactLeft = 0
reactRight = 0

reinforceYN = False # （変動報酬選択肢）強化するか否か。
reinforcers = 0 # 強化子の数を表す。0は小報酬、1は大報酬

leverLeftTrial = 0 # 左レバー押しのカウンター
leverRightTrial = 0 # 右レバー押しのカウンター

trial = 0
timeStart = time.time()  # 始まりの時間
timeNow = time.time()
timePast = 0
timeLatency = 0
timeTrial = time.time()

randPosition = 0
randCounter = 0
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
headers = ['Counter', 'LeverSide', 'Time', 'Trial', 'Latency', 'Big/Small']
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
# 乱数生成関数
def ransu():
    sum0 = 0
    # 初期的乱数列を生成
    for i in range(trialsMax):
        randList.append(random.randint(0,1))
        i = i + 1
        pass
    # 4連以上しないように次の項目を調整
    for i in range(trialsMax - 3):
        sum0 = randList[i] + randList[i+1] + randList[i+2]
        if sum0 == 0: # 0が3連になると次の項目を1に変わる
            randList[i+3] = 1
            pass
        if sum0 == 3: # 1が3連になると次の項目を0に変わる
            randList[i+3] = 0
            pass
        pass
    pass

# 0と1が「半々」であるか否かを検証
def ransuTest():
    sumRand = 0
    global randList
    # 「半々」じゃないとずっと繰り返す
    while sumRand != trialsMax/2:
        # リセット
        randList = []
        sumRand = 0
        # 新しい乱数列を再生成
        ransu()
        for i in range(trialsMax):
            sumRand = sumRand + randList[i]
            pass
        pass
    pass


# レバー格納関数
def leverRetract():
    GPIO.output(leverLeftMove, GPIO.HIGH)
    GPIO.output(leverRightMove, GPIO.HIGH)
    #GPIO.output(houseLight, GPIO.HIGH)
    pass

# レバー引き出し関数
def leverOut():
    GPIO.output(leverLeftMove, GPIO.LOW)
    GPIO.output(leverRightMove, GPIO.LOW)
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
データの精度に影響がほとんどないので、
どうしても気になれば0.01を0.001や0.0001に替えても大丈夫です。
（0.01の時よりCPUの使用率が2%ぐらい上がる）

'''

# 餌やり関数
def reinforce(rewardKind): # sReward/mReward/lReward
    for i in range(rewardKind):
        GPIO.output(feeder, GPIO.LOW)
        GPIO.output(buzzer, GPIO.HIGH)
        sleep(0.5)
        GPIO.output(feeder, GPIO.HIGH)
        GPIO.output(buzzer, GPIO.LOW)
        sleep(0.5)
    pass

# 大報酬の特別提示音を流せる関数
def chickenDinner():
    for i in range(9):
        GPIO.output(buzzer, GPIO.HIGH)
        sleep(0.15)
        GPIO.output(buzzer, GPIO.LOW)
        sleep(0.15)
    pass

# ITI関数
def ITI(time):
    print("ITI中")
    for i in range(iti,0,-1):
        print(i,"秒")
        sleep(1)
        i = i - 1
        pass
    print('\n'+'===================='+'\n')
    pass

# データ保存関数
def dataSaving():
    # データを保存
    dataTransfer = [leverPressData, leverData, timeData, leverActData, latencyData, randomData]
    dataTransfer = list(zip(*dataTransfer))
    with open(answer2 + '.csv', 'a+') as myfile:
        writer = csv.writer(myfile)
        writer.writerows(dataTransfer)
    # 生成された乱数列を保存
    # randomList = list(zip(*randList))
    with open(answer2 + '_randomList.csv', 'a+') as myfile2:
        writer = csv.writer(myfile2)
        writer.writerow(randList)
    pass

# 「後片付け」関数
def bye():
    myfile.close() # 保存されたデータをちゃんと閉じる
    GPIO.cleanup() # ポートをリセット
    sys.exit() # プログラム停止
    pass

# 乱数生成・大報酬が3連以上存在しないか否かを検証
print("乱数生成中")
ransu()
while True:
    if randList[randPosition] == 1 and randList[randPosition+1] == 1 and randPosition < 99:
        randCounter = randCounter + 1
    if randList[randPosition] == 0:
        randCounter = 0
    randPosition = randPosition + 1
    if randCounter >= 3:
        print("大報酬3連以上あり　やり直し中")
        randList = []
        ransu()
        randPosition = 0
        randCounter = 0
    if randPosition >= 99:
        break
print("生成されました", '\n', randList)

# 点灯！！
GPIO.output(houseLight, GPIO.HIGH)
leverOut()

# メインプログラム
try:
    while timeNow - timeStart < timeMax:
        timeNow = time.time()
        
        # 最大試行数になったか否か
        if leverLeftTrial + leverRightTrial >= trialsMax:
            print("最大試行数に達して終了")
            print(timePast, "秒かかった")
            print("左レバー　", leverLeftTrial, "　回")
            print("右レバー　", leverRightTrial, "　回")
            dataSaving()
            bye()
            
        # レバー押しを測る
        while react != x: # 加速ループ → この部分に絞る
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
                print("反応", leverPressCounter)
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
                print("反応", leverPressCounter)
                print("右レバー ", reactRight, "/", x, '\n')
                protect()
                pass
            coolDown()
            

        # FRを達成したら：
        if leftRight == 'right' and react == x: # 固定報酬選択肢
            leverRetract()
            react = 0
            leftRight = ''
            # 乱数を累進する
            listPosition = listPosition + 1
            # 試行を累進
            trial = trial + 1
            leverRightTrial = leverRightTrial + 1
            leverActData.insert(leverPressCounter - 1, leverRightTrial)
            # モニターに表せ
            print("固定報酬", leverRightTrial)
            print("反応時間", timePast)
            print("反応潜時", timeLatency)
            print('\n'+'===================='+'\n')
            # 固定報酬ので強化文も一緒にここで書く
            reinforce(mReward)
            # レバー引き込みとITI
            ITI(iti)
            leverOut()
            timeTrial = time.time()
            pass
        elif leftRight == 'left' and react == x: #変動報酬選択肢
            leverRetract()
            react = 0
            leftRight = ''
            # 強化
            reinforceYN = True # 強化する
            reinforcers = randList[listPosition] # 乱数リストから今回の報酬種類を読み取り
            # 乱数を累進する
            listPosition = listPosition + 1
            # 試行を累進する
            trial = trial + 1
            leverLeftTrial = leverLeftTrial + 1
            leverActData.insert(leverPressCounter - 1, leverLeftTrial)
            randomData.insert(leverPressCounter - 1, reinforcers)
            # モニターに表せ
            print("変動報酬", leverLeftTrial)
            print("反応時間", timePast)
            print("反応潜時", timeLatency)
            print('\n'+'===================='+'\n')
            pass
            # 変動報酬選択肢のレバー引き込み＆ITIは給餌分のあとにある

        # 変動報酬給餌文
        if reinforceYN == True:
            if reinforcers == 0:
                print("小報酬",'\n','\n')
                reinforce(sReward)
                reinforceYN = False
                ITI(iti)
                leverOut()
                timeTrial = time.time()
                pass
            else:
                print("大報酬",'\n','\n')
                chickenDinner()
                reinforce(lReward)
                reinforceYN = False
                reinforcers = 0
                ITI(iti)
                leverOut()
                timeTrial = time.time()
                pass
            pass


    
    # 最大時間になったか否か
    else:
        print("最大時間に達して終了")
        print("左レバー　", leverLeftTrial, "　回")
        print("右レバー　", leverRightTrial, "　回")
        dataSaving()
        bye()
        pass

# 終了
except KeyboardInterrupt:
    pass

# ポート釈放
dataSaving()
bye()
