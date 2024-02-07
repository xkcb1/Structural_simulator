from lib.Widgets.console import JupyterConsoleWidget
from lib.base import *


class PureBGwidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        # 设置无边框窗口、背景透明和圆角
        self.setAttribute(Qt.WA_TranslucentBackground)
        # 添加阴影效果
        # 创建一些内容，这里只是一个关闭按钮
        self.paintCount = 0

    def paintEvent(self, event):
        if self.paintCount >= 1:
            return
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        # 绘制透明圆角矩形
        rounded_rect = self.rect().adjusted(15, 15, -15, -15)  # 调整矩形大小以便留出阴影空间
        painter.setBrush(QBrush(QColor(100, 0, 0, 50)))
        painter.drawRoundedRect(rounded_rect, 15, 15)
        self.paintCount += 1

    def resizeEvent(self, event):
        self.paintCount = 0


class Terminal(QWidget):
    def __init__(self, parent=None, window=None, openPath=''):
        super(Terminal, self).__init__()
        self._parent_ = parent
        self._window_ = window
        # start
        mainLayout = QVBoxLayout(self)
        mainLayout.setContentsMargins(0, 0, 0, 0)
        self._mainwidget_ = QWidget()
        mainLayout.addWidget(self._mainwidget_)
        # set main widget
        self._mainwidget_.setObjectName('MainWidget')

        self.Mainlayout = QVBoxLayout(self._mainwidget_)
        self.Mainlayout.setContentsMargins(0, 0, 0, 3)
        self.Mainlayout.setSpacing(7)
        #
        self.ThisBGwidget = PureBGwidget(self)
        self.BGlayout = QVBoxLayout(self.ThisBGwidget)
        self.BGlayout.setContentsMargins(0, 0, 0, 0)
        self.BGlayout.setSpacing(0)
        self.Mainlayout.addWidget(self.ThisBGwidget)
        # 创建一个新的Ipython
        self.ThisTerminal = JupyterConsoleWidget()
        self.ThisTerminal.setStyleSheet(
            'border-bottom-left-radius:5px !important;border-bottom-right-radius:5px !important;')
        self.BGlayout.addWidget(self.ThisTerminal)
        if self._parent_.thisTheme == 'light':
            self.ThisTerminal.set_default_style('lightbg')
        else:
            self.ThisTerminal.set_default_style('linux')

        self._parent_.Terminal_List.append(
            [self.ThisTerminal, self._window_.page])
