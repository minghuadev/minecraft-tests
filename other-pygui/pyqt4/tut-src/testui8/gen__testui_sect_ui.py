# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'testui_sect_ui.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
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
        SectForm.resize(480, 19)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(SectForm.sizePolicy().hasHeightForWidth())
        SectForm.setSizePolicy(sizePolicy)
        self.gridLayout = QtGui.QGridLayout(SectForm)
        self.gridLayout.setContentsMargins(-1, 1, -1, 1)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.checkBox = QtGui.QCheckBox(SectForm)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.checkBox.sizePolicy().hasHeightForWidth())
        self.checkBox.setSizePolicy(sizePolicy)
        self.checkBox.setObjectName(_fromUtf8("checkBox"))
        self.gridLayout.addWidget(self.checkBox, 0, 0, 1, 1)
        self.contentWidget = QtGui.QFrame(SectForm)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.contentWidget.sizePolicy().hasHeightForWidth())
        self.contentWidget.setSizePolicy(sizePolicy)
        self.contentWidget.setFrameShape(QtGui.QFrame.Box)
        self.contentWidget.setFrameShadow(QtGui.QFrame.Sunken)
        self.contentWidget.setObjectName(_fromUtf8("contentWidget"))
        self.gridLayout.addWidget(self.contentWidget, 0, 1, 1, 1)

        self.retranslateUi(SectForm)
        QtCore.QObject.connect(self.checkBox, QtCore.SIGNAL(_fromUtf8("stateChanged(int)")), SectForm.callbackSectCheckBox)
        QtCore.QMetaObject.connectSlotsByName(SectForm)

    def retranslateUi(self, SectForm):
        SectForm.setWindowTitle(_translate("SectForm", "Form", None))
        self.checkBox.setText(_translate("SectForm", "CheckBox", None))

