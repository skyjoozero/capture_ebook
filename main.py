import os
import time
from mss.windows import MSS as mss
import mss.tools
from pynput.mouse import Button, Controller, Listener

pages = 0

MAX_X_POS = 0
MAX_Y_POS = 0

settingLeftXPos = 0
settingLeftYPos = 0

settingRightXPos = 0
settingRightYPos = 0

nextButtonXPos = 0
nextButtonYPos = 0

workingDir = ''

def settingSaveDir(bookName):
    global workingDir
    workingDir = os.path.join(os.getcwd(), bookName)
    if not os.path.exists(workingDir):
        os.makedirs(workingDir)

def on_click(x, y, button, pressed):
    if pressed:
        print('start')
    if not pressed:
        # Stop listener
        return False

if __name__ == '__main__':

    mouse = Controller()

    bookName = input('book name: ')
    settingSaveDir(bookName)

    pages = int(input('페이지 입력: ').strip())

    input('left upper position')
    settingLeftXPos, settingLeftYPos = mouse.position

    input('right lower position')
    settingRightXPos, settingRightYPos = mouse.position

    input('next button')
    nextButtonXPos, nextButtonYPos = mouse.position

    print('창을 최소화')
    with Listener(on_click=on_click) as listener:
        listener.join()

    with mss.mss() as sct:
        size = {'top': settingLeftYPos, 'left': settingLeftXPos, 'width': settingRightXPos - settingLeftXPos, 'height': settingRightYPos - settingLeftYPos}
        time.sleep(1)
        for i in range(pages):
            output = os.path.join(workingDir, str(i + 1) + '.png')
            sctImg = sct.grab(size)
            mss.tools.to_png(sctImg.rgb, sctImg.size, output=output)
            mouse.position = (nextButtonXPos, nextButtonYPos)
            mouse.scroll(0, -1)
            time.sleep(0.1)

    print('finish')