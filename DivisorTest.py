from psychopy import visual, core, monitors, event
import random as rd
from datetime import datetime as dd
import csv

def divisorTest(dotNum, divNum, testNum):
    monitor, window = setMonitorAndWindow()

    result = []

    #textStart = visual.TextStim(window, text='Return >> Start', font='', pos=(0.0, 0.5), rgb=None)
    #textStart.draw()
    #window.flip()

    proceedStep()
    window.flip()

    testCount = 0
    while True:
        proceedStep()

        timer = core.Clock()
        setDivisor(window, divNum, 4)
        tempDotNum = setDots(window, dotNum, 4)
        window.flip()

        proceedStep()
        detectEscape()
        window.flip()

        result.append([tempDotNum, timer.getTime()])

        testCount += 1
        if testCount == testNum:
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
    dots = []
    area = flameSize/2 - flameSize/10
    noise = rd.randint(-5, 5)

    tempNum = dotNum + noise
    for i in range(tempNum):
        dots.append(visual.Circle(window, radius=0.05, edges=32, pos=(rd.uniform(-area, area), rd.uniform (-area, area)), lineColor='black'))
    for d in dots:
        d.draw()

    return tempNum

def proceedStep() :
    while True:
        if event.getKeys(keyList='return', modifiers=False, timeStamped=False):
            break

def detectEscape():
    # escapeを押すと一旦終了
    if event.getKeys(keyList='escape', modifiers=False, timeStamped=False):
            core.quit()

def writeCSV(result):
    schedule = str(dd.now().year)+'-'+str(dd.now().month)+'-'+str(dd.now().day)+'-'+str(dd.now().minute)+'-'+str(dd.now().second)
    with open('./results/'+str(schedule)+'.csv', 'w') as f:
        writer = csv.writer(f, lineterminator='\n')
        writer.writerows(result)

if __name__ == '__main__':
    divisorTest(dotNum=41, divNum=1, testNum=2)