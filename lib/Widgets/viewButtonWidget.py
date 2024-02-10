# coding:utf-8
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *


class viewButtonWidget(QFrame):
    def __init__(self, MainParent=None):
        super().__init__()
        self._parent_ = MainParent
        self.setObjectName('viewButtonWidget')
        self.setFrameShadow(QFrame.Sunken)
        self.setStyleSheet(f'''
#viewButtonWidget {{
    background-color: {self._parent_.BgColor};
    border-radius: 0px !important;
    border:2px solid {self._parent_.BorderColor} !important;
}}
''')
        # 在构造函数中进行初始化等操作

    def enterEvent(self, event):
        # 当鼠标进入控件时触发
        # 可以在这里添加你希望执行的操作
        # 例如改变控件的样式
        self.setStyleSheet(f'''
#viewButtonWidget {{
    background-color: {self._parent_.BgColor};
    border-radius: 0px !important;
    border:2px solid {self._parent_.ThemeColor} !important;
}}
''')
        super().enterEvent(event)  # 调用基类的实现

    def leaveEvent(self, event):
        # 当鼠标离开控件时触发
        # 可以在这里添加你希望执行的操作
        # 例如恢复控件的原始样式
        self.setStyleSheet(f'''
#viewButtonWidget {{
    background-color: {self._parent_.BgColor};
    border-radius: 0px !important;
    border:2px solid {self._parent_.BorderColor} !important;
}}
''')
        self.update()
        super().leaveEvent(event)  # 调用基类的实现

    def _update_(self):
        # 更新样式
        self.setStyleSheet(f'''
#viewButtonWidget {{
    background-color: {self._parent_.BgColor};
    border-radius: 0px !important;
    border:2px solid {self._parent_.BorderColor} !important;
}}
''')
