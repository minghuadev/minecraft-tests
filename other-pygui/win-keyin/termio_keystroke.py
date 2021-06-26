#
# https://stackoverflow.com/questions/13207678/whats-the-simplest-way-of-detecting-keyboard-input-in-a-script-from-the-termina

import threading
from win32api import STD_INPUT_HANDLE
from win32console import GetStdHandle, KEY_EVENT, ENABLE_ECHO_INPUT, ENABLE_LINE_INPUT, ENABLE_PROCESSED_INPUT


class KeyAsyncReader():
    def __init__(self):
        self.stopLock = threading.Lock()
        self.stopped = True
        self.capturedChars = ""

        self.readHandle = GetStdHandle(STD_INPUT_HANDLE)
        self.readHandle.SetConsoleMode(ENABLE_LINE_INPUT|ENABLE_ECHO_INPUT|ENABLE_PROCESSED_INPUT)

    def startReading(self, readCallback):
        self.stopLock.acquire()

        try:
            if not self.stopped:
                raise Exception("Capture is already going")

            self.stopped = False
            self.readCallback = readCallback

            backgroundCaptureThread = threading.Thread(target=self.backgroundThreadReading)
            backgroundCaptureThread.daemon = True
            backgroundCaptureThread.start()
        except:
            self.stopLock.release()
            raise
        self.stopLock.release()


    def backgroundThreadReading(self):
        curEventLength = 0
        curKeysLength = 0
        while True:
            eventsPeek = self.readHandle.PeekConsoleInput(10000)
            self.stopLock.acquire()
            if self.stopped:
                self.stopLock.release()
                return
            self.stopLock.release()
            if len(eventsPeek) == 0:
                continue
            if not len(eventsPeek) == curEventLength:
                if self.getCharsFromEvents(eventsPeek[curEventLength:]):
                    self.stopLock.acquire()
                    self.stopped = True
                    self.stopLock.release()
                    break
                curEventLength = len(eventsPeek)

    def getCharsFromEvents(self, eventsPeek):
        callbackReturnedTrue = False
        for curEvent in eventsPeek:
            if curEvent.EventType == KEY_EVENT:
                if curEvent.VirtualKeyCode in [39, 37, 38, 40, 46] and curEvent.KeyDown:
                    # http://cherrytree.at/misc/vk.htm
                    vkdec = { 39:"right", 37:"left", 38:"up", 40:"down", 46:"del" }
                    vk = vkdec.get(curEvent.VirtualKeyCode, None)
                    if self.readCallback([vk]) == True:
                        callbackReturnedTrue = True
                elif ord(curEvent.Char) == 0 or not curEvent.KeyDown:
                    pass
                else:
                    curChar = str(curEvent.Char)
                    if self.readCallback(curChar) == True:
                        callbackReturnedTrue = True
        return callbackReturnedTrue

    def stopReading(self):
        self.stopLock.acquire()
        self.stopped = True
        self.stopLock.release()


class MyApp():

    def __init__(self):
        self._ch_cnt = 0

    def my_cb(self, ch):
        if type(ch) is list:
            vc = ch
            print(" one ch: ", ch, vc, end="")
        elif type(ch) is str:
            vc = ord(ch)
            if vc == 8: # backspace
                prt = ch + ch + ch + ch + ch + ch
                print(prt, end="")
            else:
                print(" one ch: ", ch, vc , end="")
        self._ch_cnt += 1

    def run(self):
        klgr = KeyAsyncReader()
        klgr.startReading(self.my_cb)
        while True:
            if self._ch_cnt > 24:
                break
        klgr.stopReading()
        print(" ch_cnt ", self._ch_cnt)

app = MyApp()
app.run()
print("app done")

