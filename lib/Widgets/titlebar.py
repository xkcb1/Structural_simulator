# coding:utf-8
import sys

from PyQt5.QtCore import Qt, QEvent
from PyQt5.QtGui import QColor, QCursor
from PyQt5.QtWidgets import QLabel, QHBoxLayout, QWidget, QAction

from qframelesswindow import FramelessWindow, TitleBarBase

from lib.Widgets.menu import PureRoundedBorderMenu


class CustomTitleBar(TitleBarBase):
    """ 
    Custom title bar 
    if appMode == 'Frameless' : use CustomTitleBar
    """

    def __init__(self, parent):
        super().__init__(parent)
        # add buttons to layout
        self._parent_ = parent
        self.setObjectName('CustomTitleBar')
        self.hBoxLayout = QHBoxLayout(self)
        self.hBoxLayout.setSpacing(0)
        self.hBoxLayout.setContentsMargins(0, 0, 0, 0)
        self.hBoxLayout.setAlignment(Qt.AlignVCenter | Qt.AlignLeft)
        self.hBoxLayout.addWidget(QWidget())
        # widget

        self.hBoxLayout.addWidget(self.minBtn, 0, Qt.AlignRight)
        self.hBoxLayout.addWidget(self.maxBtn, 0, Qt.AlignRight)
        self.hBoxLayout.addWidget(self.closeBtn, 0, Qt.AlignRight)
        # size
        # min
        self.minBtn.setHoverColor(Qt.white)
        self.minBtn.setNormalColor(Qt.white)
        self.minBtn.setHoverBackgroundColor(QColor(0, 100, 182))
        self.minBtn.setPressedColor(Qt.white)
        self.minBtn.setPressedBackgroundColor(QColor(54, 57, 65))

        # max
        self.maxBtn.setHoverColor(Qt.white)
        self.maxBtn.setNormalColor(Qt.white)
        self.maxBtn.setHoverBackgroundColor(QColor(0, 100, 182))
        self.maxBtn.setPressedColor(Qt.white)
        self.maxBtn.setPressedBackgroundColor(QColor(54, 57, 65))

        # clsoe
        self.closeBtn.setNormalColor(Qt.white)

        # resize
        self.minBtn.setFixedHeight(29)
        self.maxBtn.setFixedHeight(29)
        self.closeBtn.setFixedHeight(29)
        # 给 QWidget 绑定右键菜单
