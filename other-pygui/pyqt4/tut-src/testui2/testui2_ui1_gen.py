# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'testui2_ui1.ui'
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

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName(_fromUtf8("Form"))
        Form.resize(400, 300)
        self.horizontalLayout = QtGui.QHBoxLayout(Form)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.gridLayout_3 = QtGui.QGridLayout()
        self.gridLayout_3.setObjectName(_fromUtf8("gridLayout_3"))
        self.label_3 = QtGui.QLabel(Form)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.gridLayout_3.addWidget(self.label_3, 0, 0, 1, 1)
        self.spinBox_3 = QtGui.QSpinBox(Form)
        self.spinBox_3.setMaximum(255)
        self.spinBox_3.setObjectName(_fromUtf8("spinBox_3"))
        self.gridLayout_3.addWidget(self.spinBox_3, 1, 0, 1, 1)
        self.verticalSlider_3 = QtGui.QSlider(Form)
        self.verticalSlider_3.setMaximum(255)
        self.verticalSlider_3.setOrientation(QtCore.Qt.Vertical)
        self.verticalSlider_3.setObjectName(_fromUtf8("verticalSlider_3"))
        self.gridLayout_3.addWidget(self.verticalSlider_3, 2, 0, 1, 1)
        self.horizontalLayout.addLayout(self.gridLayout_3)
        self.gridLayout_2 = QtGui.QGridLayout()
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.label_2 = QtGui.QLabel(Form)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.gridLayout_2.addWidget(self.label_2, 0, 0, 1, 1)
        self.spinBox_2 = QtGui.QSpinBox(Form)
        self.spinBox_2.setMaximum(255)
        self.spinBox_2.setObjectName(_fromUtf8("spinBox_2"))
        self.gridLayout_2.addWidget(self.spinBox_2, 1, 0, 1, 1)
        self.verticalSlider_2 = QtGui.QSlider(Form)
        self.verticalSlider_2.setMaximum(255)
        self.verticalSlider_2.setOrientation(QtCore.Qt.Vertical)
        self.verticalSlider_2.setObjectName(_fromUtf8("verticalSlider_2"))
        self.gridLayout_2.addWidget(self.verticalSlider_2, 2, 0, 1, 1)
        self.horizontalLayout.addLayout(self.gridLayout_2)
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.label = QtGui.QLabel(Form)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.spinBox = QtGui.QSpinBox(Form)
        self.spinBox.setMaximum(255)
        self.spinBox.setObjectName(_fromUtf8("spinBox"))
        self.gridLayout.addWidget(self.spinBox, 1, 0, 1, 1)
        self.verticalSlider = QtGui.QSlider(Form)
        self.verticalSlider.setMaximum(255)
        self.verticalSlider.setOrientation(QtCore.Qt.Vertical)
        self.verticalSlider.setObjectName(_fromUtf8("verticalSlider"))
        self.gridLayout.addWidget(self.verticalSlider, 2, 0, 1, 1)
        self.horizontalLayout.addLayout(self.gridLayout)

        self.retranslateUi(Form)
        QtCore.QObject.connect(self.spinBox_3, QtCore.SIGNAL(_fromUtf8("valueChanged(int)")), self.verticalSlider_3.setValue)
        QtCore.QObject.connect(self.verticalSlider_3, QtCore.SIGNAL(_fromUtf8("valueChanged(int)")), self.spinBox_3.setValue)
        QtCore.QObject.connect(self.spinBox_2, QtCore.SIGNAL(_fromUtf8("valueChanged(int)")), self.verticalSlider_2.setValue)
        QtCore.QObject.connect(self.verticalSlider_2, QtCore.SIGNAL(_fromUtf8("valueChanged(int)")), self.spinBox_2.setValue)
        QtCore.QObject.connect(self.spinBox, QtCore.SIGNAL(_fromUtf8("valueChanged(int)")), self.verticalSlider.setValue)
        QtCore.QObject.connect(self.verticalSlider, QtCore.SIGNAL(_fromUtf8("valueChanged(int)")), self.spinBox.setValue)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(_translate("Form", "Form", None))
        self.label_3.setText(_translate("Form", "Blue", None))
        self.label_2.setText(_translate("Form", "Green", None))
        self.label.setText(_translate("Form", "Red", None))

