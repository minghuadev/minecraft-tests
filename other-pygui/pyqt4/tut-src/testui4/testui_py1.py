#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
sys.dont_write_bytecode = True
          # add to site-packages/usercustomize.py
          # may be at .local/lib/python2.6/...

from PyQt4 import QtGui, QtCore
from gen__testui_sect_ui import Ui_SectForm


class Ui_TestApp(QtGui.QWidget):
    def __init__(self, t):
        super(Ui_TestApp, self).__init__()

        self.scrollArea = QtGui.QScrollArea(self)
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QtGui.QWidget()
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.horizontalLayout = QtGui.QHBoxLayout(self)
        self.horizontalLayout.addWidget(self.scrollArea)

        self.widgt = self.scrollAreaWidgetContents
        vbox = QtGui.QVBoxLayout()
        vbox.addStretch(1)

        self.ui_node = Ui_SectForm()
        self.ui_node.refNodeType = "node"
        self.ui_node.refContainer = QtGui.QWidget()
        self.ui_node.refContainer.callbackSectCheckBox = self.callbackSectCheckBox
        self.ui_node.setupUi(self.ui_node.refContainer)
        self.ui_node.checkBox.setText("node   ")
        vbox.addWidget(self.ui_node.refContainer)

        self.ui_node.refInnerVbox = QtGui.QVBoxLayout()
        self.ui_node.refInnerList = []
        for n in range(0,2):
            iw = QtGui.QLabel(" row %d " %n)
            self.ui_node.refInnerList.append(iw)
            self.ui_node.refInnerVbox.addWidget(iw)
        self.ui_node.contentWidget.setLayout( self.ui_node.refInnerVbox )

        self._nSlots = 24
        self.ui_slots = []
        for n in range(0, self._nSlots):
            sect = Ui_SectForm()
            self.ui_slots.append(sect)
            self.ui_slots[n].refNodeType = "slot"
            self.ui_slots[n].refContainer = QtGui.QWidget()
            self.ui_slots[n].refContainer.callbackSectCheckBox = self.callbackSectCheckBox
            self.ui_slots[n].setupUi(self.ui_slots[n].refContainer)
            self.ui_slots[n].checkBox.setText("slot %2d" % n)
            vbox.addWidget(self.ui_slots[n].refContainer)

        self.widgt.setLayout(vbox)

        self.tmr = t
        self.tmr_touched = 0

        self.userValue = 255

        # Set up the user interface from Designer.

        # Make some local modifications.

        # Connect up the buttons.
        #self.okButton.clicked.connect(self.accept)
        #self.cancelButton.clicked.connect(self.reject)

    def callbackSectCheckBox(self, value):
        sdr = self.sender()
        sdrn = sdr.objectName()
        print "callbackSectCheckBox : sdrn %s value %d" % (sdrn, value)
        if self.ui_node.checkBox.checkState() == 0:
            self.ui_node.contentWidget.hide()
        else:
            self.ui_node.contentWidget.show()
        for n in range(0, self._nSlots):
            if self.ui_slots[n].checkBox.checkState() == 0:
                self.ui_slots[n].contentWidget.hide()
            else:
                self.ui_slots[n].contentWidget.show()

    def runorfail(self, value):
        print "run or fail: value type %s " % (type(value) is int)
        print "run or fail: %d " % value
        sdr = self.sender()
        sdrn = sdr.objectName()
        print "run or fail:         sdrn %s " % sdrn
        if sdrn == "verticalSlider_3":
            self.tmr_touched += 1
            print
            print "   tmr touched %d " % self.tmr_touched
            print "   tmr active  %s " % str(self.tmr.isActive())
            print "   tmr intvl   %s " % str(self.tmr.interval())
            print "   tmr single  %s " % str(self.tmr.isSingleShot())
            print
            if self.tmr_touched > 10:
                self.tmr.stop()

    def runcountdown(self):
        if self.userValue > 10:
            self.userValue -= 2
        else:
            self.userValue += 241
            if self.userValue < 1 or self.userValue > 255:
                self.userValue = 255
        #self.ui.verticalSlider.setValue(self.userValue)

def main():

    app = QtGui.QApplication(sys.argv)
    t = QtCore.QTimer()
    w = Ui_TestApp(t)

    t.start(1000)
    t.timeout.connect(w.runcountdown)

    w.resize(900, 700)
    w.move(100, 100)
    w.setWindowTitle('Simple')
    w.show()

    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
