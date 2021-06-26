#

import threading

class MyApp():

    def __init__(self):
        self._ch_cnt = 0

    def my_cb(self, ch):
        if type(ch) is list:
            vc = ch
            print(" one ch: ", ch, vc, end="")
        elif type(ch) is str:
            if len(ch) == 1:
                vc = ord(ch)
                if vc == 8: # backspace
                    prt = ch + ch + ch + ch + ch + ch
                    print(prt, end="")
                else:
                    print(" one ch: ", ch, vc , end="")
            else:
                print(" one line: ", ch, end="")
        self._ch_cnt += 1

    def run(self):

        while True:
            r = input("\nEnter your command: ")
            self.my_cb(r)
            if self._ch_cnt > 12:
                break
        print(" ch_cnt ", self._ch_cnt)

app = MyApp()
app.run()
print("app done")

