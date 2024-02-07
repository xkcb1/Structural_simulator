from lib.base import *


class Object(QWidget):
    def __init__(self, parent=None, window=None, openPath=''):
        super(Object, self).__init__()
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
        self.Mainlayout.setContentsMargins(0, 4, 0, 0)
        self.Mainlayout.setSpacing(7)

        MainLayout = self.Mainlayout
        self.topOptionWidget = QWidget()
        # start
        self.objectView = QTreeWidget()
        self.objectView.setColumnCount(1)

        # 设置树形控件头部的标题
        self.objectView.setHeaderLabels(['方块类型 (block type)'])
        self.objectView.setAnimated(True)
        self.objectView.setAlternatingRowColors(True)
        self.objectView.LastPickerActor = None  # 初始化状态:上一个拾取
        #
        self._parent_.objectView_list[str(
            self._parent_.objectView_listCount)] = self.objectView
        self._parent_.objectView_listCount += 1
        NewCornerWidget = QWidget()
        NewCornerWidget.setObjectName('NewCornerWidget')
        self.objectView.setCornerWidget(NewCornerWidget)
        self.objectView.setObjectName('fileTreeView')
        self.makeOptionWidget()
        #
        self.bottom_info = QLabel()
        self.bottom_info.setStyleSheet(
            'background-color: rgba(0,0,0,0);padding-left:5px;')
        self.bottom_info.setText('Blocks:0 | Types:0')
        # end
        MainLayout.addWidget(self.topOptionWidget)
        MainLayout.addWidget(self.objectView)

    def makeOptionWidget(self):
        self.topOptionWidget.setObjectName("topOptionWidget")
        self.optLayout = QHBoxLayout(self.topOptionWidget)
        self.optLayout.setContentsMargins(5, 0, 5, 0)
        self.optLayout.setSpacing(7)
        # SearchInput_1
        self.SearchInput_1 = QLineEdit()
        self.SearchInput_1.setFixedHeight(26)
        self.SearchInput_1.setPlaceholderText('Search for Item...')
        self.SearchInput_1.setObjectName('SearchPathWidget')
        self.SearchInput_1.setStyleSheet(
            '''* {
                padding-left: 15px;
                background-image: url(./img/appIcon/d_Search.png);
                background-repeat: no-repeat;
                background-position: left center;
                }''')
        # typeCombox
        buttonLayout = QHBoxLayout()
        buttonLayout.setContentsMargins(0, 0, 0, 0,)
        buttonLayout.setSpacing(0)
        self.typeCombox = QPushButton()
        self.typeCombox.setIcon(QIcon('./img/McsLib.png'))
        self.typeCombox.setFixedHeight(26)
        self.typeCombox.setFixedWidth(26)
        self.typeCombox.setStyleSheet('''*{border-top-right-radius:0px;
                           border-bottom-right-radius:0px;
                           }''')

        # worldChoose
        self.worldChoose = QPushButton()
        self.worldChoose.setIcon(QIcon('./img/Node.png'))
        self.worldChoose.setFixedHeight(26)
        self.worldChoose.setFixedWidth(26)
        self.worldChoose.setStyleSheet('''*{border-top-left-radius:0px;
                        border-bottom-left-radius:0px;
                        border-left:0px;
                           }''')

        buttonLayout.addWidget(self.typeCombox)
        buttonLayout.addWidget(self.worldChoose)

        # button_layout_2
        button_layout_2 = QHBoxLayout()
        button_layout_2.setSpacing(0)
        button_layout_2.setContentsMargins(0, 0, 0, 0)
        self.open_lock = QPushButton()
        self.open_lock.setIcon(QIcon('img/pinned_16.png'))
        self.open_lock.isLock = False
        self.open_lock.setObjectName('checkButton_1')
        self.open_lock.clicked.connect(self.changeLock)
        self.open_lock.setFixedSize(26, 26)
        self.open_lock.setStyleSheet('''*{border-top-left-radius:0px;
                        border-bottom-left-radius:0px;
                        border-left:0px;
                           }''')

        open_AllBlock = QPushButton()
        open_AllBlock.setIcon(
            QIcon(f'img/appIcon/{self._parent_.Puretheme}/augmented-reality.svg'))
        open_AllBlock.iconPath = 'augmented-reality.svg'
        self._parent_.changeIconList.append(open_AllBlock)
        open_AllBlock.setFixedSize(26, 26)
        open_AllBlock.setStyleSheet('''*{border-top-right-radius:0px;
                           border-bottom-right-radius:0px;
                           }''')

        button_layout_2.addWidget(open_AllBlock)
        button_layout_2.addWidget(self.open_lock)
        # add widget
        self.optLayout.addLayout(buttonLayout)
        self.optLayout.addWidget(self.SearchInput_1)
        self.optLayout.addLayout(button_layout_2)

    def changeLock(self):
        print(self.open_lock.objectName())
        '''
        点击锁定按钮
        '''
        if self.sender().isLock == False:
            self.sender().isLock = True
            self.sender().setIcon(QIcon('img/pinned_16_50.png'))
            self._window_.setFeatures(self._window_.features()
                                      & ~QDockWidget.DockWidgetClosable)
            self.open_lock.setObjectName('checkButton_0')
            self.open_lock.setStyleSheet('''*{border-top-left-radius:0px;
                        border-bottom-left-radius:0px;
                        border-left:0px;
                           }''')
            # 锁上

        else:
            self.sender().isLock = False
            self.sender().setIcon(QIcon('img/pinned_16.png'))
            self._window_.setFeatures(self._window_.features()
                                      | QDockWidget.DockWidgetClosable)
            self.open_lock.setObjectName('checkButton_1')
            self.open_lock.setStyleSheet('''*{border-top-left-radius:0px;
                        border-bottom-left-radius:0px;
                        border-left:0px;
                           }''')
            # 没锁
