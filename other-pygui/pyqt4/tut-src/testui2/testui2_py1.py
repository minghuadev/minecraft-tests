#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
from PyQt4 import QtGui, QtCore
from testui2_ui1_gen import Ui_Form

class Ui_TestApp(QtGui.QWidget):
    def __init__(self, t):
        super(Ui_TestApp, self).__init__()

        self.ui = Ui_Form()
        self.widgt = self
        self.tmr = t
        self.tmr_touched = 0

        self.userValue = 255

        # Set up the user interface from Designer.
        self.ui.setupUi(self.widgt)

        # Make some local modifications.
        #self.colorDepthCombo.addItem("2 colors (1 bit per pixel)")

        # Connect up the buttons.
        #self.okButton.clicked.connect(self.accept)
        #self.cancelButton.clicked.connect(self.reject)
        self.ui.verticalSlider.setValue(self.userValue)
        self.ui.verticalSlider.valueChanged.connect(self.runorfail)
        self.ui.verticalSlider_3.valueChanged.connect(self.runorfail)

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
        self.ui.verticalSlider.setValue(self.userValue)

def main():

    app = QtGui.QApplication(sys.argv)
    t = QtCore.QTimer()
    w = Ui_TestApp(t)

    t.start(1000)
    t.timeout.connect(w.runcountdown)

    w.resize(250, 150)
    w.move(300, 300)
    w.setWindowTitle('Simple')
    w.show()

    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
