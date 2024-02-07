from lib.base import *


class Tools(QWidget):
    def __init__(self, parent=None, window=None, openPath=''):
        super(Tools, self).__init__()
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
        self.Mainlayout.setContentsMargins(0, 4, 0, 0)
        self.Mainlayout.setSpacing(0)
