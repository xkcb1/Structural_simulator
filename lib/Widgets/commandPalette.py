# coding:utf-8
import getpass
import os
import typing
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import QWidget

from lib.Widgets.tooltip import ToolTipFilter, ToolTipPosition


class PureCommandPalette(QToolButton):
    def __init__(self, parent: QMainWindow | None = ...) -> None:
        super().__init__()
        self._parent_ = parent
        self.setObjectName("PureCommandPalette")
        self.setStyleSheet(
            '#PureCommandPalette {border-radius:2px;font-size:12px;}')
        self.setIcon(
            QIcon(f'img/main_3/Commands.png'))
        self.setIconSize(QSize(18, 18))
        self.setFixedHeight(23)
        self.setText('Structure Studio : '+getpass.getuser())
        self.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        self.setToolTip('''<div style="white-space: pre;">
命令面板: <a style="color:orange;">全局</a>
使用 Ctrl + Shift + C 打开命令面板''')
        self.installEventFilter(ToolTipFilter(
            self, 300, ToolTipPosition.BOTTOM))
