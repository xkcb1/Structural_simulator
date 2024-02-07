# coding:utf-8
import os
from PyQt5 import QtCore, QtGui
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import PyQt5.QtWidgets as QtWidgets
from PyQt5.QtCore import *

# 自定义菜单控件


class PureRoundedBorderMenu(QMenu):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        try:
            self.setAttribute(Qt.WA_TranslucentBackground)
            self.setWindowFlags(self.windowFlags(
            ) | Qt.FramelessWindowHint | Qt.NoDropShadowWindowHint)
        except:
            # 某些系统不支持背景透明和无边框
            pass
