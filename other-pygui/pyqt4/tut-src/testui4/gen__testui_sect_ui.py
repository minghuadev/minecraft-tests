# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'testui_sect_ui.ui'
#
# Created: Tue Mar  8 15:33:59 2016
#      by: PyQt4 UI code generator 4.10.2
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_SectForm(object):
    def setupUi(self, SectForm):
        SectForm.setObjectName(_fromUtf8("SectForm"))
        SectForm.resize(480, 270)
        self.gridLayout = QtGui.QGridLayout(SectForm)
        self.gridLayout.setContentsMargins(-1, 1, -1, 1)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.checkBox = QtGui.QCheckBox(SectForm)
        self.checkBox.setObjectName(_fromUtf8("checkBox"))
        self.gridLayout.addWidget(self.checkBox, 0, 0, 1, 1)
        self.contentWidget = QtGui.QFrame(SectForm)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.contentWidget.sizePolicy().hasHeightForWidth())
        self.contentWidget.setSizePolicy(sizePolicy)
        self.contentWidget.setFrameShape(QtGui.QFrame.StyledPanel)
        self.contentWidget.setFrameShadow(QtGui.QFrame.Raised)
        self.contentWidget.setObjectName(_fromUtf8("contentWidget"))
        self.gridLayout.addWidget(self.contentWidget, 0, 1, 1, 1)

        self.retranslateUi(SectForm)
        QtCore.QObject.connect(self.checkBox, QtCore.SIGNAL(_fromUtf8("stateChanged(int)")), SectForm.callbackSectCheckBox)
        QtCore.QMetaObject.connectSlotsByName(SectForm)

    def retranslateUi(self, SectForm):
        SectForm.setWindowTitle(_translate("SectForm", "Form", None))
        self.checkBox.setText(_translate("SectForm", "CheckBox", None))

