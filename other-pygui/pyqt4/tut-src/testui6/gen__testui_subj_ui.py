# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'testui_subj_ui.ui'
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

class Ui_SubjForm(object):
    def setupUi(self, SubjForm):
        SubjForm.setObjectName(_fromUtf8("SubjForm"))
        SubjForm.resize(425, 41)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(SubjForm.sizePolicy().hasHeightForWidth())
        SubjForm.setSizePolicy(sizePolicy)
        self.gridLayout_2 = QtGui.QGridLayout(SubjForm)
        self.gridLayout_2.setContentsMargins(-1, 1, -1, 1)
        self.gridLayout_2.setVerticalSpacing(1)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setContentsMargins(6, -1, 6, -1)
        self.gridLayout.setHorizontalSpacing(12)
        self.gridLayout.setVerticalSpacing(1)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.subjLabel = QtGui.QLabel(SubjForm)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.subjLabel.sizePolicy().hasHeightForWidth())
        self.subjLabel.setSizePolicy(sizePolicy)
        self.subjLabel.setObjectName(_fromUtf8("subjLabel"))
        self.gridLayout.addWidget(self.subjLabel, 0, 1, 1, 1)
        self.subjEdit = QtGui.QLineEdit(SubjForm)
        self.subjEdit.setObjectName(_fromUtf8("subjEdit"))
        self.gridLayout.addWidget(self.subjEdit, 0, 2, 1, 1)
        self.subjSlider = QtGui.QSlider(SubjForm)
        self.subjSlider.setOrientation(QtCore.Qt.Horizontal)
        self.subjSlider.setObjectName(_fromUtf8("subjSlider"))
        self.gridLayout.addWidget(self.subjSlider, 0, 3, 1, 1)
        self.subjButton = QtGui.QPushButton(SubjForm)
        self.subjButton.setObjectName(_fromUtf8("subjButton"))
        self.gridLayout.addWidget(self.subjButton, 0, 4, 1, 1)
        self.subjPerm = QtGui.QLabel(SubjForm)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.subjPerm.sizePolicy().hasHeightForWidth())
        self.subjPerm.setSizePolicy(sizePolicy)
        self.subjPerm.setObjectName(_fromUtf8("subjPerm"))
        self.gridLayout.addWidget(self.subjPerm, 0, 0, 1, 1)
        self.gridLayout_2.addLayout(self.gridLayout, 0, 0, 1, 1)

        self.retranslateUi(SubjForm)
        QtCore.QObject.connect(self.subjButton, QtCore.SIGNAL(_fromUtf8("pressed()")), SubjForm.callbackSubjButton)
        QtCore.QMetaObject.connectSlotsByName(SubjForm)

    def retranslateUi(self, SubjForm):
        SubjForm.setWindowTitle(_translate("SubjForm", "Form", None))
        self.subjLabel.setText(_translate("SubjForm", "TextLabel", None))
        self.subjButton.setText(_translate("SubjForm", "Run", None))
        self.subjPerm.setText(_translate("SubjForm", "TextLabel", None))

