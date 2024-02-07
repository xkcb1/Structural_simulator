from lib.Widgets.flowWidgets import PpathWidget
from lib.Widgets.minecraftObject import DataPackVersion
from lib.Widgets.treeWidget import CreateFileTree
from lib.base import *


class Assets(QWidget):
    def __init__(self, parent=None, window=None, openPath=''):
        super(Assets, self).__init__()
        openPath = openPath.replace('//', '/')
        self._parent_ = parent
        self.openPath = openPath
        self._window_ = window
        self.thisPath = openPath
        self.thread_count = 0
        self.filePath = ''

        # start
        mainLayout = QVBoxLayout(self)
        mainLayout.setContentsMargins(0, 0, 0, 0)
        self._mainwidget_ = QWidget()
        mainLayout.addWidget(self._mainwidget_)
        # set main widget
        self._mainwidget_.setObjectName('MainWidget')
        self._mainwidget_.setStyleSheet(
            '''#MainWidget{border:1px solid rgba(125,125,125,0.25);
            border-top:0px !important;
            background-color:rgba(0,0,0,0);
            border-bottom-left-radius:5px !important;
            border-bottom-right-radius:5px !important;}''')
        self.Mainlayout = QVBoxLayout(self._mainwidget_)
        self.Mainlayout.setContentsMargins(1, 0, 1, 1)
        self.Mainlayout.setSpacing(1)
        # UI initialization
        self.uiInit()

    def uiInit(self):
        self.MainWidgetSplitter = QSplitter()
        self.Mainlayout.addWidget(self.MainWidgetSplitter)
        #
        self.fileTreeView = CreateFileTree()
        self._parent_.fileTreeView = self.fileTreeView
        self.fileTreeView.setRootIndex(
            self.fileTreeView.model_.index(self.thisPath))
        self.fileTreeView.setSortingEnabled(True)
        self.fileTreeView.setAnimated(True)
        self.fileTreeView.expandAll()
        self.fileTreeView.setAlternatingRowColors(True)
        self.fileTreeView.doubleClicked.connect(self.fileTreeViewDoubleClicked)
        self.fileTreeView.setObjectName('fileTreeView')
        '''self.fileTreeView.setStyleSheet(
            'QTreeView::item:selected{background-color: rgba(39, 179, 255,1.0);}')'''
        self.fileTreeView.setAcceptDrops(True)
        self.fileTreeView.setEditTriggers(
            QtWidgets.QAbstractItemView.NoEditTriggers)
        self.fileTreeView.setDragDropMode(QtWidgets.QAbstractItemView.DragOnly)
        self.fileTreeView.setAnimated(True)
        #
        self.MainWidgetSplitter.addWidget(self.fileTreeView)
        #
        self.rightWidget = QWidget()
        self.rightWidget.setObjectName('rightWidget')
        self.rightWidget.setStyleSheet(
            '#rightWidget {border-left:1px solid rgba(175,175,175,0.2);}')
        self.MainWidgetSplitter.addWidget(self.rightWidget)
        self.rightLayout = QVBoxLayout(self.rightWidget)
        self.rightLayout.setContentsMargins(0, 0, 0, 0)
        self.rightLayout.setSpacing(1)
        #
        self.right_top_widget = QWidget()
        self.right_top_widget.setFixedHeight(70)
        self.right_top_widget.setObjectName('right_top_widget')
        self.right_top_widget.setStyleSheet(
            '''#right_top_widget {background-color:rgba(125,125,125,0.1);
            border-bottom:1px solid rgba(175,175,175,0.1);
            }''')
        self.right_top_layout = QGridLayout(self.right_top_widget)
        self.right_top_layout.setContentsMargins(5, 2, 5, 2)
        self.right_top_layout.setSpacing(2)
        #
        self.rightLayout.addWidget(self.right_top_widget)
        with open(self.openPath.replace('//', '/')+'/pack.mcmeta', 'r', encoding='utf-8') as McMeta:
            thisPack = json.load(McMeta)
        getVersion = ''
        for version in DataPackVersion:
            if DataPackVersion[version] == thisPack['pack']['pack_format']:
                getVersion = version
        getDescription = thisPack['pack']['description']
        # 1
        self.versionInt = QSpinBox()
        self.versionInt.setRange(3, 23)
        self.versionInt.setValue(int(thisPack['pack']['pack_format']))
        # 2
        self.dataVersion_input = QComboBox()
        for versionName in DataPackVersion:
            self.dataVersion_input.addItem(
                QIcon('img/Minecraft_icon_2.png'), versionName + f'  [ {str(DataPackVersion[versionName])} ]')
        self.dataVersion_input.setCurrentText(getVersion)
        # 3
        self.DescriptionInput = QLineEdit()
        self.DescriptionInput.setText(getDescription)
        #
        self.right_top_layout.addWidget(QLabel('pack_format :'), 0, 0)
        self.right_top_layout.addWidget(self.versionInt, 0, 1)
        self.right_top_layout.addWidget(QLabel('Version :'), 1, 0)
        self.right_top_layout.addWidget(self.dataVersion_input, 1, 1)
        self.right_top_layout.addWidget(QLabel('Description :'), 2, 0)
        self.right_top_layout.addWidget(self.DescriptionInput, 2, 1)
        #
        self.mainWidget = QWidget()
        main_layout = QVBoxLayout(self.mainWidget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        self.rightLayout.addWidget(self.mainWidget)
        #
        self.tabWidget = QTabWidget()
        self.pathWidget = PpathWidget(self.openPath, self.changeFunction)
        main_layout.addWidget(self.pathWidget)
        main_layout.addWidget(self.SearchInput)
        #
        self.resetTabWidget()

    def fileTreeViewDoubleClicked(self):
        pass

    def changeFunction(self, path):
        pass

    def resetTabWidget(self):
        '''
        重新生成tabwidget
        '''
