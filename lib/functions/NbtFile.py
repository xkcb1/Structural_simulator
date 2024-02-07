from lib.Widgets.comboBox import PureLabel
from lib.Widgets.panel import PureAttributePanel
from lib.base import *


class NbtFile(QWidget):
    def __init__(self, parent=None, window=None, openPath=''):
        super(NbtFile, self).__init__()
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
        self.Mainlayout.setContentsMargins(5, 4, 5, 5)
        self.Mainlayout.setSpacing(7)
        # SearchWidget.set
        SearchWidget = QWidget()
        SearchLayout = QHBoxLayout(SearchWidget)
        SearchLayout.setContentsMargins(0, 0, 0, 0)
        SearchLayout.setSpacing(5)
        SearchInput = QLineEdit()
        SearchInput.setFixedHeight(25)
        SearchInput.setPlaceholderText('Search for local Folder...')
        SearchInput.setObjectName('SearchPathWidget')
        SearchInput.setClearButtonEnabled(1)
        SearchInput.setStyleSheet(
            '''* {
                padding-left: 15px;
                background-image: url(./img/appIcon/d_Search.png);
                background-repeat: no-repeat;
                background-position: left center;
                }''')
        SearchLayout.addWidget(SearchInput)

        # 文件统计表
        TableWidget = QWidget()
        TableLayout = QVBoxLayout(TableWidget)
        TableLayout.setContentsMargins(2, 0, 2, 2)
        TableLayout.setSpacing(4)
        self.tableWidget = QListWidget()
        TableLayout.addWidget(self.tableWidget)
        TablePanel = PureAttributePanel(
            '文件统计列表', TableWidget, 1, QIcon('img/toolbar/d_Tilemap Icon.png'))

        # 文件信息列表
        ListWidget = QWidget()
        ListLayout = QVBoxLayout(ListWidget)
        ListLayout.setContentsMargins(2, 0, 2, 2)
        ListLayout.setSpacing(4)
        self.NbtListWidget = QListWidget()
        ListLayout.addWidget(self.NbtListWidget)
        ListPanel = PureAttributePanel('文件信息列表', ListWidget, 1, QIcon(
            'img/toolbar/d_SortingGroup Icon.png'))

        #
        self.Mainlayout.addWidget(SearchWidget)
        self.Mainlayout.addWidget(TablePanel)
        self.Mainlayout.addWidget(ListPanel)
        self.Mainlayout.addStretch(9999)
