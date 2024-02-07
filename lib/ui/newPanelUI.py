# -*- coding: utf-8 -*-
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt, QPoint, QSize
from PyQt5.QtGui import QFont, QEnterEvent, QPixmap, QColor
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QDialog, QGraphicsDropShadowEffect
from PyQt5 import QtCore
from PyQt5.QtCore import *
from lib.base import *


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        self.verticalLayout = QtWidgets.QVBoxLayout(Form)
        self.THIS_Widget = QtWidgets.QFrame(Form)
        self.THIS_Widget.setObjectName('THIS_Widget')
        ##
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.verticalLayout.addWidget(self.THIS_Widget)
        self.THIS_Widget.setContentsMargins(7, 7, 7, 7)
        self.THIS_Widget.setAttribute(Qt.WA_TranslucentBackground)
        self.THIS_Widget.setMinimumHeight(35)
        ##
        self.VLayout2 = QtWidgets.QVBoxLayout(self.THIS_Widget)
        self.MainWidget_This = QtWidgets.QFrame(self.THIS_Widget)
        self.VLayout2.setContentsMargins(0, 0, 0, 0)
        self.VLayout2.setSpacing(0)
        self.VLayout2.addWidget(self.MainWidget_This)
        ##
        self.verticalLayout__ = QtWidgets.QVBoxLayout(self.MainWidget_This)
        self.verticalLayout__.setContentsMargins(1, 1, 1, 1)
        self.verticalLayout__.setSpacing(0)
        self.verticalLayout__.setObjectName("verticalLayout__")
        self.widget = QWidget()
        self.widget.setMaximumSize(QtCore.QSize(16777215, 25))
        self.widget.setObjectName("widget__")
        self.widget.setMaximumHeight(25)
        self.widget.setStyleSheet('')
        self.widget.setMinimumHeight(25)
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.widget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.WindowName = QtWidgets.QPushButton()
        self.WindowName.setObjectName("WindowName1")
        self.WindowName.setContentsMargins(0, 0, 0, 0)
        self.WindowName.setStyleSheet(
            '''#WindowName1{ margin:0px; padding:5px;}''')

        self.TopLayout = self.horizontalLayout
        spacerItem = QtWidgets.QSpacerItem(
            5, 20, QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.label = QtWidgets.QLabel(self.widget)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(20)
        sizePolicy.setVerticalStretch(20)
        sizePolicy.setHeightForWidth(
            self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setMaximumSize(QtCore.QSize(16, 16))
        self.label.setObjectName("label__")
        self.label.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.addWidget(self.label)
        self.horizontalLayout.addWidget(self.WindowName)
        spacerItem1 = QtWidgets.QSpacerItem(
            5, 20, QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.label_2 = QtWidgets.QLabel(self.widget)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(30)
        sizePolicy.setHeightForWidth(
            self.label_2.sizePolicy().hasHeightForWidth())
        self.label_2.setSizePolicy(sizePolicy)
        self.label_2.setObjectName("label_3")
        self.horizontalLayout.addWidget(self.label_2)
        spacerItem2 = QtWidgets.QSpacerItem(
            40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem2)
        self.pushButton = QtWidgets.QPushButton(self.widget)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(29)
        sizePolicy.setVerticalStretch(29)
        sizePolicy.setHeightForWidth(
            self.pushButton.sizePolicy().hasHeightForWidth())
        self.pushButton.setSizePolicy(sizePolicy)
        self.pushButton.setMaximumSize(QtCore.QSize(25, 25))
        self.pushButton.setObjectName("pushButton")
        self.horizontalLayout.addWidget(self.pushButton)
        self.pushButton_2 = QtWidgets.QPushButton(self.widget)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(29)
        sizePolicy.setVerticalStretch(29)
        sizePolicy.setHeightForWidth(
            self.pushButton_2.sizePolicy().hasHeightForWidth())
        self.pushButton_2.setSizePolicy(sizePolicy)
        self.pushButton_2.setMaximumSize(QtCore.QSize(25, 25))
        self.pushButton_2.setObjectName("pushButton_2")
        self.horizontalLayout.addWidget(self.pushButton_2)
        self.pushButton_3 = QtWidgets.QPushButton(self.widget)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(29)
        sizePolicy.setVerticalStretch(29)
        sizePolicy.setHeightForWidth(
            self.pushButton_3.sizePolicy().hasHeightForWidth())
        self.pushButton_3.setSizePolicy(sizePolicy)
        self.pushButton_3.setMaximumSize(QtCore.QSize(25, 25))
        self.pushButton_3.setObjectName("pushButton_3")
        self.pushButton.setMinimumWidth(25)
        self.pushButton_2.setMinimumWidth(25)
        self.pushButton_3.setMinimumWidth(25)
        self.horizontalLayout.addWidget(self.pushButton_3)
        self.verticalLayout__.addWidget(self.widget)
        self.widget_2 = QtWidgets.QWidget()
        self.widget_2.setObjectName("widget_2")
        self.verticalLayout__.addWidget(self.widget_2)
        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)
        # end

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.label.setText(_translate("Form", "图标"))
        self.label_2.setText(_translate("Form", "TextLabel"))
        self.pushButton.setToolTip(_translate(
            "Form", "<html><head/><body><p>MinimumSize</p></body></html>"))
        self.pushButton_2.setToolTip(_translate(
            "Form", "<html><head/><body><p>MaximumSize</p></body></html>"))
        self.pushButton_3.setToolTip(_translate(
            "Form", "<html><head/><body><p>Close Window</p></body></html>"))
