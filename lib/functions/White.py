from lib.base import *


class White(QWidget):
    def __init__(self, parent=None, window=None, openPath=''):
        super(White, self).__init__()
        self._parent_ = parent
        self._window_ = window
        self.openPath = openPath
        # start
        mainLayout = QVBoxLayout(self)
        mainLayout.setContentsMargins(0, 0, 0, 0)
        self._mainwidget_ = QWidget()
        mainLayout.addWidget(self._mainwidget_)
        # set main widget
        self._mainwidget_.setObjectName('MainWidget')
        self.Mainlayout = QVBoxLayout(self._mainwidget_)
        self.Mainlayout.setContentsMargins(0, 3, 0, 0)
        self.Mainlayout.setSpacing(0)
        #
        Hbox = QHBoxLayout()
        Hbox.setContentsMargins(0, 0, 0, 0)
        self.Mainlayout.addLayout(Hbox)
        self.IconWidget = QPushButton()
        self.IconWidget.setStyleSheet(
            'background-color:rgba(0,0,0,0) !important;border:0px !important;')
        Hbox.addWidget(self.IconWidget)
        self.IconWidget.setIcon(QIcon('img/mcEarth_black_40.png'))
        self.IconWidget.setIconSize(QSize(200, 200))
