# coding:utf-8
import os
from PyQt5 import QtCore, QtGui
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import PyQt5.QtWidgets as QtWidgets
from PyQt5.QtCore import *
from lib.Widgets.menu import PureRoundedBorderMenu

'''
PureComboBox
'''


class PureComboBox(QToolButton):
    def __init__(self, title: str = '', w=220, h=300, func=print, parent=None):
        super().__init__(parent)
        self.title = title
        self._func_ = func
        self.w = w
        self.h = h
        self.UiInit()
        self.setMenu(self.ChooseMenu)

    def UiInit(self):
        self.setPopupMode(QToolButton.InstantPopup)
        self.setStyleSheet('padding-right:9px;padding-left:4px;')
        self.ChooseMenu = PureRoundedBorderMenu(self)
        self.ChooseMenu.setStyleSheet('''
                            QMenu{padding:0px !important;border-top-left-radius:0px !important;}''')
        self.setMenu(self.ChooseMenu)
        Panel = QWidget()
        Panel.setFixedSize(self.w, self.h)
        ChoosePanel_Action = QWidgetAction(self.ChooseMenu)
        ChoosePanel_Action.setDefaultWidget(Panel)
        self.ChooseMenu.addAction(ChoosePanel_Action)
        #
        PanelLayout = QVBoxLayout(Panel)
        PanelLayout.setContentsMargins(5, 3, 5, 5)
        self.TitleLabel = QLabel(self.title)
        self.TitleLabel.setFixedHeight(18)
        self.chooseList = QListWidget()
        self.SearchInput = QLineEdit()
        self.SearchInput.setFixedHeight(22)
        self.SearchInput.setPlaceholderText('Search for local Folder...')
        self.SearchInput.setObjectName('SearchPathWidget')
        self.SearchInput.setClearButtonEnabled(1)
        self.SearchInput.setStyleSheet(
            '''* {
                padding-left: 15px;
                background-image: url(./img/appIcon/d_Search.png);
                background-repeat: no-repeat;
                background-position: left center;
                }''')
        # 添加进布局
        PanelLayout.addWidget(self.TitleLabel)
        PanelLayout.addWidget(self.chooseList)
        PanelLayout.addWidget(self.SearchInput)

    def setMenuList(self, initList: list = [], iconList: list = []):
        self.chooseList.clear()
        for i in range(len(initList)):
            text = initList[i]
            # print('add item :', text)
            try:
                icon = iconList[i]
                # print('add icon :', icon)
            except:
                print('can not find icon')
                icon = ''
            Item = QListWidgetItem(QIcon(icon), text, self.chooseList)
            self.chooseList.addItem(Item)
        self.chooseList.itemClicked.connect(self._func_)

    def setFunc(self, func):
        self._func_ = func


class PureLabel(QPushButton):
    def __init__(self, style=''):
        super(PureLabel, self).__init__()
        self.setStyleSheet(
            '''background-color:rgba(0,0,0,0) !important;
                border:0px !important;
                text-align:left !important;
                '''+style)
