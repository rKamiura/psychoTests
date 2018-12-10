from psychopy import visual, core, monitors, event
import random as rd
from datetime import datetime as dd
import csv
import itertools as itl

from dot import Dot
        
# 私はクラス縛りでもしてるの？
def experimentalProtocol():
    # プロトコール

    # ドット数の種類
    dotNums  = [13, 20, 27, 34, 41]
    # ドット数に与えるノイズ幅（任意）
    dotNoise = 1

    # 分画数の種類
    dividerNums = [1, 2, 4] # 1は分画しない

    # ドット数と分画の組み合わせ
    testCombination = []
    for dot, div in itl.product(dotNums, dividerNums):
        testCombination.append([dot+rd.randint(-dotNoise, dotNoise), div])
    # 組み合わせのランダマイズ
    rd.shuffle(testCombination)
    #print(testCombination)

    ## 以下プロトコル実行 ##
    monitor, window = setMonitorAndWindow()

    textStart = visual.TextStim(window, text='Return >> Start', font='', pos=(0.0, 0.5), rgb=None)
    textStart.draw()
    window.flip()

    # 雑〜〜〜〜
    while True:
        if event.getKeys(keyList='return', modifiers=False, timeStamped=False):
            window.flip()
            break

    # ループプロセス
    state = 0 # 開始は0
    testCount = 0 # 何回めの試行か
    result = [] # 結果の格納庫
    answer = '' # 入力させるカウントの結果の格納庫
    while True:
        keys = event.getKeys()

        if state == 0:
            timer = core.Clock()

            state = 1

        elif state == 1: # カウンティング開始
            setDivisor(window, testCombination[testCount][1], 4)
            dots = setDots(window, testCombination[testCount][0], 4)
            window.flip()
            state = 2

        elif state == 2: # カウンティング開始後，ドット等の更新用に．
            setDivisor(window, testCombination[testCount][1], 4)
            updateDots(dots, timer.getTime())
            window.flip()

            if proceedStep() :
                state = 3

        elif state == 3: # カウント終了
            textEnd = visual.TextStim(window, text='Answer the number of Dot.', font='', pos=(0.0, 0.5), rgb=None)
            textEnd.draw()
            textAns = visual.TextStim(window, text=answer, font='', pos=(0.0, -0.5), rgb=None)
            textAns.draw()
            window.flip()

            if len(keys) > 0:
                if keys[0] in [str(i) for i in range(10)]:
                    answer += keys[0]

            if len(answer) > 0:
                if 'return' in keys:
                    #print(answer)
                    result.append([testCombination[testCount][0], testCombination[testCount][1], int(answer), timer.getTime()])
                    answer = ''
                    state = 4

        elif state == 4: # 1周分の最終処理
            testCount += 1
            if testCount == len(testCombination):
                break
            
            state = 0

    print(result)
    writeCSV(result)
    core.quit() 


def setMonitorAndWindow():
    # モニター情報の設定
    widthPix        = 1440 # screen width in px
    heightPix       = 900 # screen height in px
    monitorwidth    = 24 # monitor width in cm
    viewdist        = 60. # viewing distance in cm

    monitorname = 'Socially-Unfit'
    monitor = monitors.Monitor(monitorname, width=monitorwidth, distance=viewdist)
    monitor.setSizePix((widthPix, heightPix))

    # Windowの設定
    window = visual.Window(
    monitor=monitor, 
    size=(widthPix,heightPix),
    color='Gray',
    colorSpace='rgb',
    units='deg',
    screen=0, # 0はメインモニタ，1は外部モニタ
    allowGUI=False,
    fullscr=False) # フルスクリーンにするかどうか

    monitor.save()
    return monitor, window

def setDivisor(window, divNum, flameSize):
    # 外枠の設定
    outerFlame = visual.Rect(window, width=flameSize, height=flameSize, lineColor='black')
    outerFlame.draw()

    # 内枠の設定(面倒臭いので自動化とかループ最適化とかしてやせん)
    if divNum == 1:
        return
    elif divNum == 2:
        innerFlamePos = [[[0, flameSize/2], [0, -flameSize/2]], [[flameSize/2, 0], [-flameSize/2, 0]]]
    elif divNum == 4:
        innerFlamePos = [[[0, flameSize/2], [0, -flameSize/2]],
                          [[flameSize/4, flameSize/2], [flameSize/4, -flameSize/2]],
                          [[-flameSize/4, flameSize/2], [-flameSize/4, -flameSize/2]],
                          [[flameSize/2, 0], [-flameSize/2, 0]],
                          [[flameSize/2, flameSize/4], [-flameSize/2, flameSize/4]],
                          [[flameSize/2, -flameSize/4], [-flameSize/2, -flameSize/4]]]
    else:
        print("KOMATTA")
        exit()

    innerFlames = []
    for pos in innerFlamePos:
        innerFlames.append(visual.Line(window, start=pos[0], end=pos[1], lineColor='black'))
    for inner in innerFlames:
        inner.draw()

def setDots(window, dotNum, flameSize):
    # ドットのセット（位置，速度，加速度）
    dots = []
    area = flameSize/2 - flameSize/10
    noise = 0

    # ポジション生成
    pos = [[rd.uniform(-area, area), rd.uniform (-area, area)] for i in range(dotNum)]
    # 速度設定
    velocity = [[.001, .001] for i in range(dotNum)]
    # 加速度設定
    acceleration = [[-0.001, .001] for i in range(dotNum)]

    for i in range(dotNum):
        dots.append(Dot(window, radius=0.05, lineWidth=1, pos=pos[i], velocity=velocity[i], acceleration=acceleration[i]))
    for d in dots:
        d.draw()

    return dots

def updateDots(dots, dt):
    for ds in dots:
        ds.update(dt)

def inputAnswer():
    while True:
        textStart = visual.TextStim(window, text='Answer the number of dots', font='', pos=(0.0, 0.5), rgb=None)
        textStart.draw()
        window.flip()

def proceedStep() :
    if event.getKeys(keyList='return', modifiers=False, timeStamped=False):
        return True
    elif event.getKeys(keyList='escape', modifiers=False, timeStamped=False):
        core.quit()
    else:
        return False

def detectEscape():
    # escapeを押すと一旦終了
    if event.getKeys(keyList='escape', modifiers=False, timeStamped=False):
            core.quit()

def writeCSV(result):
    schedule = str(dd.now().year)+'-'+str(dd.now().month)+'-'+str(dd.now().day)+'-'+str(dd.now().hour)+'-'+str(dd.now().minute)+'-'+str(dd.now().second)
    with open('./results/'+str(schedule)+'.csv', 'w') as f:
        writer = csv.writer(f, lineterminator='\n')
        writer.writerows(result)

if __name__ == '__main__':
    experimentalProtocol()