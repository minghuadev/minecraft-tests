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
        SectForm.resize(800, 600)
        self.horizontalLayout = QtGui.QHBoxLayout(SectForm)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.checkBox = QtGui.QCheckBox(SectForm)
        self.checkBox.setObjectName(_fromUtf8("checkBox"))
        self.horizontalLayout.addWidget(self.checkBox)
        self.tableWidget = QtGui.QTableWidget(SectForm)
        self.tableWidget.setObjectName(_fromUtf8("tableWidget"))
        self.tableWidget.setColumnCount(0)
        self.tableWidget.setRowCount(0)
        self.horizontalLayout.addWidget(self.tableWidget)

        self.retranslateUi(SectForm)
        QtCore.QObject.connect(self.checkBox, QtCore.SIGNAL(_fromUtf8("stateChanged(int)")), SectForm.callbackSectCheckBox)
        QtCore.QMetaObject.connectSlotsByName(SectForm)

    def retranslateUi(self, SectForm):
        SectForm.setWindowTitle(_translate("SectForm", "Form", None))
        self.checkBox.setText(_translate("SectForm", "CheckBox", None))

