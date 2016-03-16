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
    def __init__(self, top_tmr_arg, top_tmr_itvl_arg, model1=None, model2=None):
        super(Ui_TestApp, self).__init__()          # top external widget

        self.top_tmr = top_tmr_arg
        self.top_tmr_intvl = top_tmr_itvl_arg
        self._model2 = model2

        self.form1 = Ui_TestBackform('form1', self.top_tmr, self.top_tmr_intvl)
        self.form2 = Ui_TestBackform('form2', self.top_tmr, self.top_tmr_intvl,
                                     self._model2)

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

    def updateDataView(self, data):
        self.form1.updateDataView(data)
        self.form2.updateDataView(data)

class TestUi:
    def __init__(self, model1=None, model2=None):

        self._model1 = model1
        self._model2 = model2

        self._app = QtGui.QApplication(sys.argv)
        t = QtCore.QTimer()
        w = Ui_TestApp(t, 1000, model1, model2)
        self._w = w

        t.start(1000)

        w.resize(1256, 800)
        w.move(8, 136)
        w.setWindowTitle('Front Simple')
        w.show()

    def testui_mainloop(self):
        sys.exit(self._app.exec_())

class TestDataModel:
    def __init__(self, uiref=None):
        self._uiref = uiref
        self._nodedata = ["node_data_1", "node_data_2"]
        self._slotdata = ["slot_data_11", "slot_data_22"]
        self._eval_count = 0

    def setView(self, uiref):
        self._uiref = uiref

    def get_node_names(self):
        return [x.replace("node_","") for x in self._nodedata[:]]
    def get_slot_names(self):
        return [x.replace("slot_","") for x in self._slotdata[:]]

    def eval_from_top(self):
        self._eval_count += 1
        if self._uiref != None:
            self._uiref.updateDataView(self._eval_count)


if __name__ == '__main__':
    testdata = TestDataModel()
    testui = TestUi(model1=None, model2=testdata)
    testdata.setView(testui._w)
    testui.testui_mainloop()

