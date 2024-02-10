# coding:utf-8
import sys

from PyQt5.QtCore import Qt
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import QWidget

from qframelesswindow import FramelessMainWindow, FramelessDialog

from lib.Widgets.comboBox import PureLabel


class NewFramelessWindow(FramelessMainWindow):

    def __init__(self, parent):
        super().__init__()
        self._parent_ = parent
        self.setMinimumSize(400, 500)
        self.setWindowTitle("Frameless Main Window")
        from lib.Widgets.titlebar import CustomTitleBar
        self.setTitleBar(CustomTitleBar(self))
        # add menu bar
        menuBar = QMenuBar(self.titleBar)
        menuBar.setStyleSheet('QMenuBar {padding-left:2px;padding-top:4px;}')
        menuBar.setFixedWidth(150)
        menuBar.setFixedHeight(29)
        menuBar.addAction('查找(&F)')
        menuBar.addAction('帮助(&H)')
        menuBar.addAction('退出(&E)', self.close)
        self.spaceWidget = QWidget(self.titleBar)
        self.spaceWidget.move(150, 0)
        self.spaceWidgetLayout = QHBoxLayout(self.spaceWidget)
        self.spaceWidgetLayout.setContentsMargins(10, 5, 10, 2)
        # titleLabel
        titleLabel = PureLabel()
        titleLabel.setText('偏好设置')
        titleLabel.setIcon(
            QIcon('img/appIcon/dark/preferences.svg'))
        self.spaceWidgetLayout.addStretch(1)
        self.spaceWidgetLayout.addWidget(titleLabel)
        self.spaceWidgetLayout.addStretch(1)
        self.titleBar.layout().insertWidget(0, menuBar, 0, Qt.AlignLeft)
        self.titleBar.layout().insertStretch(1, 1)
        self.setMenuWidget(self.titleBar)
        #
        self.MainWidget = QWidget()
        self.MainLayout = QVBoxLayout(self.MainWidget)
        self.MainLayout.setContentsMargins(0, 0, 0, 0)
        self.setCentralWidget(self.MainWidget)
        # add status bar
        statusBar = QStatusBar(self)
        statusBar.addWidget(QLabel("Setting File : "))
        self.setStatusBar(statusBar)
        self.setPaletteTheme()

    def setPaletteTheme(self):
        # dark theme
        palette = QPalette()
        palette.setColor(QPalette.Window, QColor(29, 29, 29))
        palette.setColor(QPalette.WindowText, Qt.white)
        palette.setColor(QPalette.Base, QColor(45, 45, 46))
        palette.setColor(QPalette.AlternateBase, QColor(37, 37, 38))
        palette.setColor(QPalette.ToolTipBase, Qt.white)
        palette.setColor(QPalette.ToolTipText, Qt.white)
        palette.setColor(QPalette.Text, Qt.white)
        palette.setColor(QPalette.Button, QColor(37, 37, 38))
        palette.setColor(QPalette.ButtonText, Qt.white)
        palette.setColor(QPalette.BrightText, Qt.red)
        palette.setColor(QPalette.Link, QColor(71, 114, 179))
        palette.setColor(QPalette.Highlight, QColor(71, 114, 179))
        palette.setColor(QPalette.HighlightedText, Qt.black)
        self.setPalette(palette)
        with open('theme/Window/dark.qss', 'r', encoding='utf-8') as styleFile:
            self.setStyleSheet(styleFile.read())
        self.titleBar.setStyleSheet(
            '#CustomTitleBar{background-color: #1d1d1d;}')
        # min
        self.titleBar.minBtn.setNormalColor(Qt.white)
        self.titleBar.minBtn.setNormalBackgroundColor(
            QColor('#1d1d1d'))
        # max
        self.titleBar.maxBtn.setNormalColor(Qt.white)
        self.titleBar.maxBtn.setNormalBackgroundColor(
            QColor('#1d1d1d'))
        # clsoe
        self.titleBar.closeBtn.setNormalColor(Qt.white)
        self.titleBar.closeBtn.setNormalBackgroundColor(
            QColor('#1d1d1d'))
        self.spaceWidget.setObjectName('spaceWidget')
        self.spaceWidget.setStyleSheet(
            '#spaceWidget {background-color: #1d1d1d;}  ')

    def resizeEvent(self, e):
        self.spaceWidget.setFixedSize(
            self.width() - 150 - self.titleBar.minBtn.width()*3, 29)
        return super().resizeEvent(e)
