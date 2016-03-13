#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
sys.dont_write_bytecode = True
          # add to site-packages/usercustomize.py
          # may be at .local/lib/python2.6/...

from PyQt4 import QtGui, QtCore
from testui_backform_py import Ui_TestBackform

import time as Ui_TestTime

class Ui_TestApp(QtGui.QWidget):
    def __init__(self, top_tmr_arg):
        super(Ui_TestApp, self).__init__()          # top external widget

        self.top_tmr = top_tmr_arg

        self.form1 = Ui_TestBackform(self.top_tmr)
        self.form2 = Ui_TestBackform(self.top_tmr)

        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.addWidget(self.form1)
        #self.horizontalLayout.addStretch(1)
        self.horizontalLayout.addWidget(self.form2)

        self.horizontalLayout.setContentsMargins(-1, -1, -1, -1)

        self.widgt = self                           # top widget
        vbox = QtGui.QVBoxLayout()                  # top layout
        vbox.addLayout(self.horizontalLayout)

        self.widgt.setLayout(vbox)

        self.ui_beats_label = QtGui.QLabel

        # bottom line:
        while True: # scoping block, run once
            bline_layout = QtGui.QHBoxLayout()
            self.ui_beats_label = QtGui.QLabel(" ... ... ")
            vbox.addLayout(bline_layout)
            bline_layout.addWidget(QtGui.QLabel("Front bottom line: "))
            bline_layout.addStretch(1)
            bline_layout.addWidget(QtGui.QLabel("Started at "))
            tmstr = " %02d:%02d:%02d " % Ui_TestTime.localtime()[3:6]
            bline_layout.addWidget(QtGui.QLabel(tmstr))
            bline_layout.addWidget(QtGui.QLabel("Timer beats: "))
            bline_layout.addWidget(self.ui_beats_label)
            bline_layout.addWidget(QtGui.QLabel(" :) "))
            break

        self.top_tmr.timeout.connect(self.runtimerbeat)

    def runtimerbeat(self):
        tmnow = " now %02d:%02d:%02d " % Ui_TestTime.localtime()[3:6]
        self.ui_beats_label.setText(tmnow)

def main():

    app = QtGui.QApplication(sys.argv)
    t = QtCore.QTimer()
    w = Ui_TestApp(t)

    t.start(1000)

    w.resize(1256, 800)
    w.move(8, 136)
    w.setWindowTitle('Front Simple')
    w.show()

    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
