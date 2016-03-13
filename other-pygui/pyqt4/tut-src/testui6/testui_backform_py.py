#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
sys.dont_write_bytecode = True
          # add to site-packages/usercustomize.py
          # may be at .local/lib/python2.6/...

from PyQt4 import QtGui, QtCore
from gen__testui_sect_ui import Ui_SectForm
from gen__testui_subj_ui import Ui_SubjForm


class Ui_TestBackform(QtGui.QWidget):
    def __init__(self, top_tmr_arg):
        super(Ui_TestBackform, self).__init__()          # top external widget

        self.chkInited = 0
        self._userValueInit = 255
        self.userValue = self._userValueInit
        self.tmr_touched = 0
        self.top_tmr = top_tmr_arg

        self._nSlots = 24

        self.scrollArea = QtGui.QScrollArea(self)   # top scroll area
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QtGui.QWidget()   # top widget
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.horizontalLayout = QtGui.QHBoxLayout(self)
        self.horizontalLayout.addWidget(self.scrollArea)

        self.widgt = self.scrollAreaWidgetContents  # top widget
        vbox = QtGui.QVBoxLayout()                  # top layout
        #vbox.addStretch(1)

        # ui node section -- sect node
        while True: # scop block, run once
            nw = Ui_SectForm()
            self.ui_node = nw
            nw.refNodeType = "node"
            nw.refContainer = QtGui.QWidget() # sect container
            nw.refContainer.callbackSectCheckBox = self.callbackSectCheckBox
            nw.setupUi(self.ui_node.refContainer)
            nw.checkBox.setText("node   ")
            nw.checkBox.refSourceType = 'node'
            nw.checkBox.refSourceIdx = 0
            vbox.addWidget(self.ui_node.refContainer)   # sect add to top vbox
            break

        # ui node sect :
        self.ui_node.refInnerVbox = QtGui.QVBoxLayout()
        self.ui_node.refInnerList = []
        for n in range(0,2):
            iw = QtGui.QLabel(" row %d " %n)
            self.ui_node.refInnerList.append(iw)
            self.ui_node.refInnerVbox.addWidget(iw)
        self.ui_node.contentWidget.setLayout( self.ui_node.refInnerVbox )

        self.ui_slots = []
        for n in range(0, self._nSlots):
            sect = Ui_SectForm()
            self.ui_slots.append(sect) # sect is self.ui_slots[n]
            sect.refNodeType = "slot"
            sect.refContainer = QtGui.QWidget()
            sect.refContainer.callbackSectCheckBox = self.callbackSectCheckBox
            sect.setupUi(self.ui_slots[n].refContainer)
            sect.checkBox.setText("slot %2d" % (n+1) )
            sect.checkBox.refSourceType = 'slot'
            sect.checkBox.refSourceIdx = n
            vbox.addWidget(sect.refContainer)
            #inner content
            sect.refInnerVbox = QtGui.QVBoxLayout()
            sect.refInnerList = []
            for m in range(0,2):
                subj = Ui_SubjForm() # subj is self.ui_slots[n].refInnerList[m]
                self.ui_slots[n].refInnerList.append(subj)
                iw = QtGui.QWidget()
                subj.refContainer = iw
                iw.callbackSubjButton = self.callbackSubjButton
                subj.setupUi(iw)
                subj.subjPerm.setText("rw")
                subj.subjLabel.setText("row %d"%(m+1))
                subj.subjEdit.setText("text %d"%(m+1))
                subj.subjButton.refSourceType = 'slot'
                subj.subjButton.refSourceIdx1 = n
                subj.subjButton.refSourceIdx2 = m
                sect.refInnerVbox.addWidget(iw)
            sect.contentWidget.setLayout( sect.refInnerVbox )


        # bottom boxes frame : check to enable slots widget
        while True: # scoping block, run once
            self.ui_slots_bottom_boxes = []
            self.ui_beats_label = QtGui.QLabel(" ... ... ")
            bbox_frame = QtGui.QFrame()
            bbox_frame.setFrameShape(QtGui.QFrame.Box)
            bbox_frame.setFrameShadow(QtGui.QFrame.Sunken)

            bbox_vlayout = QtGui.QVBoxLayout()
            bbox_frame.setLayout(bbox_vlayout)

            bbox_title_layout = QtGui.QHBoxLayout()
            bbox_vlayout.addLayout(bbox_title_layout)
            bbox_title_layout.addWidget(QtGui.QLabel("Slots: "))
            bbox_title_layout.addStretch(1)
            bbox_title_layout.addWidget(QtGui.QLabel("Timer beats: "))
            bbox_title_layout.addWidget(self.ui_beats_label)
            bbox_title_layout.addWidget(QtGui.QLabel(" :) "))

            bbox_line = None
            for n in range(0, self._nSlots):
                bchk = QtGui.QCheckBox()
                self.ui_slots_bottom_boxes.append(bchk)
                bchk.refSlotObj = self.ui_slots[n]
                bchk.setText(" %2d " %(n+1))
                bchk.refSourceType = 'bbox'
                bchk.refSourceIdx = n
                if bbox_line == None :
                    bbox_line = QtGui.QHBoxLayout()
                bbox_line.addWidget(bchk)
                bchk.stateChanged.connect(self.callbackSectCheckBox)
                if n == (self._nSlots/2-1) or n == (self._nSlots-1):
                    bbox_vlayout.addLayout(bbox_line)
                    bbox_line = None
            if bbox_line != None:
                bbox_vlayout.addLayout(bbox_line)
            break

        vbox.addStretch(1)
        vbox.addWidget(bbox_frame)

        self.widgt.setLayout(vbox)

        # Connect up the buttons.
        #self.okButton.clicked.connect(self.accept)
        #self.cancelButton.clicked.connect(self.reject)
        self.top_tmr.timeout.connect(self.runtimerbeat)

    def callbackSubjButton(self):
        sdr = self.sender()
        sdrn = sdr.objectName()
        sdrt = sdr.refSourceType
        sdri1 = sdr.refSourceIdx1
        sdri2 = sdr.refSourceIdx2
        print "callbackSubjButton : %s " % (
                    "sdrn %s sdrt %s sdri %d %d" % (sdrn, sdrt, sdri1, sdri2) )

    def callbackSectCheckBox(self, value):
        sdr = self.sender()
        sdrn = sdr.objectName()
        sdrt = sdr.refSourceType
        sdri = sdr.refSourceIdx
        print "callbackSectCheckBox : %s " % (
                "sdrn %s sdrt %s sdri %d value %d" % (sdrn, sdrt, sdri, value) )
        if type(sdrt) is str and sdrt == 'node':
            if self.ui_node.checkBox.checkState() == 0:
                self.ui_node.contentWidget.hide()
            else:
                self.ui_node.contentWidget.show()
        elif type(sdrt) == str and sdrt == 'slot':
            if type(sdri) == int and sdri < self._nSlots:
                if self.ui_slots[sdri].checkBox.checkState() == 0 and value == 0:
                    self.ui_slots[sdri].refContainer.hide()
                    if self.ui_slots_bottom_boxes[sdri].checkState() != 0:
                        self.ui_slots_bottom_boxes[sdri].setCheckState(0)
                else:
                    self.ui_slots[sdri].refContainer.show()
                    if self.ui_slots_bottom_boxes[sdri].checkState() == 0:
                        self.ui_slots_bottom_boxes[sdri].setCheckState(2)
        elif type(sdrt) == str and sdrt == 'bbox':
            # note: bbox is not really a sect box but it works here...
            if type(sdri) == int and sdri < self._nSlots:
                if self.ui_slots_bottom_boxes[sdri].checkState() == 0 and value == 0:
                    self.ui_slots[sdri].refContainer.hide()
                    if self.ui_slots[sdri].checkBox.checkState() != 0:
                        self.ui_slots[sdri].checkBox.setCheckState(0)
                else:
                    self.ui_slots[sdri].refContainer.show()
                    if self.ui_slots[sdri].checkBox.checkState() == 0:
                        self.ui_slots[sdri].checkBox.setCheckState(2)

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
            print "   tmr active  %s " % str(self.top_tmr.isActive())
            print "   tmr intvl   %s " % str(self.top_tmr.interval())
            print "   tmr single  %s " % str(self.top_tmr.isSingleShot())
            print
            if self.tmr_touched > 10:
                self.top_tmr.stop()

    def runtimerbeat(self):
        if self.userValue <= self._userValueInit and self.chkInited == 0:
            self.chkInited = 1
            if self.ui_node.checkBox.checkState() != 0:
                self.ui_node.checkBox.setCheckState(0)
            for n in range(0, self._nSlots):
                if self.ui_slots[n].checkBox.checkState() == 0:
                    self.ui_slots[n].checkBox.setCheckState(2)
            for n in range(6, self._nSlots):
                if self.ui_slots[n].checkBox.checkState() != 0:
                    self.ui_slots[n].checkBox.setCheckState(0)
            if self.ui_node.checkBox.checkState() == 0:
                self.ui_node.checkBox.setCheckState(2)

        self.userValue += 2
        if self.userValue > 0xeffe:
            self.userValue = self._userValueInit + 16
        else:
            if self.userValue < self._userValueInit:
                self.userValue = self._userValueInit

        self.ui_beats_label.setText(" %d " % self.userValue)

def main_test():

    app = QtGui.QApplication(sys.argv)
    t = QtCore.QTimer()
    w = Ui_TestBackform(t)

    t.start(1000)

    w.resize(900, 700)
    w.move(100, 100)
    w.setWindowTitle('Backform')
    w.show()

    sys.exit(app.exec_())


if __name__ == '__main__':
    main_test()
