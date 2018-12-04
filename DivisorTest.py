from psychopy import visual, core, monitors, event
import random as rd

def divisorTest():
    monitor, window = setMonitorAndWindow()

    while True:
        setDivisor(window, 2, 1)
        #window.flip()
        core.wait(1)
        detectEscape()

        #window.flip()
        core.wait(.05)
        detectEscape()

        setDots(window, 12, 1)
        window.flip()
        core.wait(5) 
        detectEscape()       

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
        print(0)
    elif divNum == 2:
        innerFlamePos = [[[0, flameSize/2], [0, -flameSize/2]], [[flameSize/2, 0], [-flameSize/2, 0]]]
    elif divNum == 4:
        innerFlamePos = [[[0, 5], [0, -5]], [[5, 0], [-5, 0]]] #放置
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
    for i in range(dotNum):
        dots.append(visual.Circle(window, radius=0.05, edges=32, pos=(rd.uniform(-area, area), rd.uniform (-area, area)), lineColor='black'))
    for d in dots:
        d.draw()

def detectEscape():
    # escapeを押すと一旦終了
        if event.getKeys(keyList='escape', modifiers=False, timeStamped=False):
            core.quit()

if __name__ == '__main__':
    divisorTest()