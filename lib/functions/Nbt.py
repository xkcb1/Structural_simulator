from lib.Widgets.treeWidget import PTreeWidget
from lib.base import *


class Nbt(QWidget):
    def __init__(self, parent=None, window=None, openPath=''):
        super(Nbt, self).__init__()
        self._parent_ = parent
        self._window_ = window
        self.thread_count = 0
        # left widget
        # nbt tree
        mainLayout = QVBoxLayout(self)
        mainLayout.setContentsMargins(0, 0, 0, 0)
        self._mainwidget_ = QWidget()
        mainLayout.addWidget(self._mainwidget_)
        # set main widget
        self._mainwidget_.setObjectName('MainWidget')

        self.Mainlayout = QVBoxLayout(self._mainwidget_)
        self.Mainlayout.setContentsMargins(0, 4, 0, 0)
        self.Mainlayout.setSpacing(7)

        self.ThisLayout = self.Mainlayout
        # TopWidget
        self.TopWidget = QWidget()
        self.TopWidget.setObjectName('TopWidget_1')

        self.ThisLayout.addWidget(self.TopWidget)
        topLayout = QVBoxLayout(self.TopWidget)
        topLayout.setContentsMargins(5, 0, 5, 0)
        topLayout.setSpacing(3)
        #
        self.ThisTopLayout = QHBoxLayout()
        self.ThisTopLayout.setContentsMargins(0, 0, 0, 0)
        self.ThisTopLayout.setSpacing(7)
        topLayout.addLayout(self.ThisTopLayout)
        # treeView
        self.treeView = PTreeWidget(self)
        self.treeView.setContentsMargins(0, 0, 0, 0)
        self.treeView.setSortingEnabled(True)
        self.treeView.setAnimated(True)
        self.treeView.setAlternatingRowColors(True)
        self._parent_.treeViewList[str(
            self._parent_.treeViewListCount)] = self.treeView
        NewCornerWidget = QWidget()
        NewCornerWidget.setObjectName('NewCornerWidget')
        self.treeView.setCornerWidget(NewCornerWidget)
        self.treeView.setObjectName('fileTreeView')
        # OpenButton
        self.SearchInput = QLineEdit()
        self.SearchInput.setFixedHeight(26)
        self.SearchInput.setPlaceholderText('Search for NBT(Tag)...')
        self.SearchInput.setObjectName('SearchPathWidget')
        self.SearchInput.setClearButtonEnabled(1)
        self.SearchInput.setStyleSheet(
            '''* {
                padding-left: 15px;
                background-image: url(./img/appIcon/d_Search.png);
                background-repeat: no-repeat;
                background-position: left center;
                }''')

        # 3种不同风格的图标选择，使用checkButton
        # icon mode
        iconLayout = QHBoxLayout()
        iconLayout.setContentsMargins(0, 0, 0, 0)
        iconLayout.setSpacing(0)
        self.icon_1 = QPushButton()
        self.icon_1.setFixedSize(26, 26)
        self.icon_1.setObjectName('checkButton_1')
        self.icon_1.setToolTip('使用图标集 1\nUse icon set 1')
        self.icon_1.installEventFilter(ToolTipFilter(
            self.icon_1, 300, ToolTipPosition.BOTTOM))
        self.icon_1.setIcon(
            QIcon(f'img/appIcon/COM_1.png'))
        self.icon_1.clicked.connect(self.icon_1_func)
        self.icon_1.setStyleSheet('''*{border-top-right-radius:0px;
                           border-bottom-right-radius:0px;
                           }''')
        #
        self.icon_2 = QPushButton()
        self.icon_2.setFixedSize(26, 26)
        self.icon_2.setToolTip('使用图标集 2\nUse icon set 2')
        self.icon_2.installEventFilter(ToolTipFilter(
            self.icon_2, 300, ToolTipPosition.BOTTOM))
        self.icon_2.setObjectName('checkButton_0')
        self.icon_2.setIcon(
            QIcon(f'img/appIcon/COM_2.png'))
        self.icon_2.setStyleSheet('''*{border-radius:0px;
                            border-left:0px;
                           }''')
        self.icon_2.clicked.connect(self.icon_2_func)
        #
        self.icon_3 = QPushButton()
        self.icon_3.setFixedSize(26, 26)
        self.icon_3.setToolTip('使用图标集 3\nUse icon set 3')
        self.icon_3.installEventFilter(ToolTipFilter(
            self.icon_3, 300, ToolTipPosition.BOTTOM))
        self.icon_3.setObjectName('checkButton_0')
        self.icon_3.setIcon(
            QIcon(f'img/appIcon/COM_3.png'))
        self.icon_3.setStyleSheet('''*{border-top-left-radius:0px;
                        border-bottom-left-radius:0px;
                        border-left:0px;
                           }''')
        self.icon_3.clicked.connect(self.icon_3_func)
        iconLayout.addWidget(self.icon_1)
        iconLayout.addWidget(self.icon_2)
        iconLayout.addWidget(self.icon_3)
        # add widget
        self.ThisTopLayout.addWidget(self.SearchInput)
        self.ThisTopLayout.addLayout(iconLayout)
        # self.ThisTopLayout.addWidget(self.chooseIconStyle)
        # treeView.clicked.connect(onTreeClicked)
        self.ThisLayout.addWidget(self.treeView)
        self.treeView.setColumnCount(2)
        self.treeView.setHeaderLabels(['Key', 'Value'])

    def icon_1_func(self):
        pass

    def icon_2_func(self):
        pass

    def icon_3_func(self):
        pass
