#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
from PyQt4 import QtGui, QtCore
from testui1_ui1_gen import Ui_Form

class Ui_TestApp(Ui_Form):
    def __init__(self, widgt):
        super(Ui_TestApp, self).__init__()
        self.widg = widgt

        # Set up the user interface from Designer.
        self.setupUi(widgt)

        # Make some local modifications.
        #self.colorDepthCombo.addItem("2 colors (1 bit per pixel)")

        # Connect up the buttons.
        #self.okButton.clicked.connect(self.accept)
        #self.cancelButton.clicked.connect(self.reject)
        self.verticalSlider.valueChanged.connect(self.runorfail)

    def runorfail(self, value):
        print "run or fail: value type %s " % (type(value) is int)
        print "run or fail: %d " % value

def main():

    app = QtGui.QApplication(sys.argv)
    w = QtGui.QWidget()
    a = Ui_TestApp(w)

    w.resize(250, 150)
    w.move(300, 300)
    w.setWindowTitle('Simple')
    w.show()

    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
