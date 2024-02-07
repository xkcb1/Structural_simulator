# coding:utf-8
import os
from PyQt5 import QtCore, QtGui
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import PyQt5.QtWidgets as QtWidgets
from PyQt5.QtCore import *

from lib.Widgets.comboBox import PureLabel


class PureAttributePanel(QFrame):
    # 参数1：Name:str,参数2：Attribute:dict,参数3：ifopen:boolean,
    def __init__(self, Name: str, widget: QWidget, ifopen: bool = False, Icon=None):
        # ifopen默认为FALSE，就是展开
        super().__init__()
        # start
        self.Name = Name
        self.widget = widget
        self.ifopen = ifopen
        self.Icon = Icon
        # self.setMinimumHeight(20)
        self.UIinit()

    def UIinit(self) -> None:
        self.IsZoomSmall = 0
        # 25是属性框收缩后的高度
        self.setObjectName('ATTRIBUTEPanel')
        self.setStyleSheet('''
#ATTRIBUTEPanel {
    border-radius:4px;
    border:1px solid rgba(150,150,150,0.15);
    background-color:rgba(150,150,150,0.1);
}
''')
        # self.setMaximumWidth(999999)
        self.MainLayoutATTR = QVBoxLayout()
        self.setLayout(self.MainLayoutATTR)
        self.MainLayoutATTR.setContentsMargins(0, 0, 0, 0)
        self.MainLayoutATTR.setSpacing(3)
        self.OptionLayout_Widget = QWidget()
        self.OptionLayout_Widget.setFixedHeight(30)
        self.OptionLayout_Widget.setObjectName('optionWidget')
        #
        self.OptionLayout = QHBoxLayout()
        self.OptionLayout.setSpacing(0)
        self.OptionLayout.setContentsMargins(5, 0, 10, 0)
        self.MainLayoutATTR.addWidget(self.OptionLayout_Widget)
        self.OptionLayout_Widget.setLayout(self.OptionLayout)
        self.ThisName = PureLabel(style='font-weight:bold;')
        # self.ThisName.setStyleSheet('background-color:red;')
        self.ThisName.setFixedHeight(30)
        self.ThisName.clicked.connect(self.zoomPanel)
        #
        self.ThisName.setText(self.Name)
        # self.ThisName.setIcon(QIcon("./img/caret-down-filled.svg"))
        # print(self.Name)
        if self.Icon != None:
            self.ThisName.setIcon(QIcon(self.Icon))
        self.OptionLayout.addWidget(self.ThisName)
        # background-image:url("./img/panel_1.png");
        self.panel_icon = QLabel()
        panel_icon = QPixmap('./img/panel.png')
        self.panel_icon.setPixmap(panel_icon)
        self.panel_icon.setFixedSize(QSize(12, 6))

        self.OptionLayout.addWidget(self.panel_icon)
        #
        self.MainWidget = QWidget()
        self.MainWidget.setObjectName('ThisMainWidget')
        self.MainLayoutATTR.addWidget(self.MainWidget)
        self.MainLayoutEdit = QVBoxLayout()
        self.MainLayoutEdit.setContentsMargins(0, 0, 0, 0)
        self.MainWidget.setLayout(self.MainLayoutEdit)
        self.Gx = 0
        self.Gy = 0
        # self.setLayout(MainLayoutATTR)
        # make the attributes from dict
        self.makeUI()
        if self.ifopen == True:
            self.IsZoomSmall = 1
            self.toBig()
        else:
            self.IsZoomSmall = 0
            self.toSmall()

    def zoomPanel(self, mode: int) -> None:
        # mode 1 扩展
        # mode 0 收缩
        if self.IsZoomSmall == 0:  # 已经是收缩
            self.toBig()
            self.IsZoomSmall = 1  # 已经是扩展
        else:
            self.toSmall()
            self.IsZoomSmall = 0

    def toSmall(self):  # 收缩
        # self.ThisName.setIcon(QIcon("./img/caret-down-filled.svg"))
        self.setMaximumHeight(30)
        self.MainWidget.hide()

    def toBig(self):  # 扩展
        # self.ThisName.setIcon(QIcon("./img/caret-up-filled.svg"))
        self.setMaximumHeight(self.widget.maximumHeight())
        self.setMinimumHeight(30)
        self.MainWidget.show()

    def update_(self, widget):
        item_list = list(
            range(self.MainLayoutEdit.count()))
        item_list.reverse()  # 倒序删除，避免影响布局顺序
        for i in item_list:
            item = self.MainLayoutEdit.itemAt(i)
            self.MainLayoutEdit.removeItem(item)
            item.widget().deleteLater()
            if item.widget():
                item.widget().deleteLater()
        # update
        self.setMaximumHeight(self.widget.maximumHeight())
        self.MainWidget.show()

    def makeUI(self):
        self.MainLayoutEdit.addWidget(self.widget)

    def resizeEvent(self, a0: QResizeEvent | None) -> None:
        if self.height() < 60:
            self.toSmall()
        return super().resizeEvent(a0)
