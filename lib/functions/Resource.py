from lib.NbtTree import NBTLastFileThread, NbtTreeThread
from lib.Widgets.comboBox import PureLabel
from lib.Widgets.flowWidgets import AssetWidget, PpathWidget
from lib.Widgets.panel import PureAttributePanel
from lib.Widgets.treeWidget import CreateFileTree
from lib.base import *


class Resource(QWidget):
    def __init__(self, parent=None, window=None, openPath=''):
        super(Resource, self).__init__()
        self._parent_ = parent
        self.openPath = openPath
        self._window_ = window
        self.thisPath = openPath
        self.thread_count = 0
        self.filePath = ''
        '''
        Asset Window This
        '''
        self.setObjectName('Resource')
        mainLayout = QVBoxLayout(self)
        mainLayout.setContentsMargins(0, 0, 0, 0)
        self._mainwidget_ = QWidget()
        mainLayout.addWidget(self._mainwidget_)
        # set main widget
        self._mainwidget_.setObjectName('MainWidget')
        self.Mainlayout = QVBoxLayout(self._mainwidget_)
        self.Mainlayout.setContentsMargins(0, 4, 0, 0)
        self.Mainlayout.setSpacing(0)
        #
        self.BottomWidget = QWidget()
        self.BottomWidget.setObjectName('AssetWidget')
        self.BottomWidget.setFixedHeight(18)
        self.BottomLabel_1 = QLabel('文件:0 文件夹:0')
        self.BottomLayout = QHBoxLayout(self.BottomWidget)
        self.BottomLayout.setContentsMargins(5, 0, 0, 3)
        self.BottomLayout.addWidget(self.BottomLabel_1)
        #

        pathBGwidget_layout = QVBoxLayout()
        self.PathWidget = PpathWidget(
            self.thisPath.replace('\\', '/'), self.change_path)
        pathBGwidget_layout.addWidget(self.PathWidget)
        pathBGwidget_layout.setContentsMargins(5, 0, 5, 0)

        # path widget
        pathBGwidget = QWidget()
        pathlayout = QVBoxLayout(pathBGwidget)
        pathlayout.setContentsMargins(0, 0, 0, 0)
        pathlayout.setSpacing(0)
        pathlayout.addWidget(self.PathWidget)
        ################################################################
        SearchWidget = QWidget()
        SearchWidget.setObjectName("topOptionWidget")
        SearchWidget.setStyleSheet(
            '#topOptionWidget {background-color:rgba(0,0,0,0);}')
        # SearchWidget.set
        SearchInput = QLineEdit()
        SearchInput.setFixedHeight(26)
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

        # left
        left = QPushButton()
        left.setFixedSize(26, 26)
        left.clicked.connect(self.PathLeft)
        left.setIcon(
            QIcon(f'img/appIcon/{self._parent_.Puretheme}/arrow-left-line.svg'))
        left.iconPath = 'arrow-left-line.svg'
        self._parent_.changeIconList.append(left)
        left.setIconSize(QSize(18, 18))
        left.setToolTip('后退一级目录\nPath : back')
        left.installEventFilter(ToolTipFilter(
            left, 300, ToolTipPosition.BOTTOM))
        left.setStyleSheet('''*{border-top-right-radius:0px;
                           border-bottom-right-radius:0px;
                           }''')

        # right
        right = QPushButton()
        right.setFixedSize(26, 26)
        right.setStyleSheet('''*{border-radius:0px;
                            border-left:0px;
                           }''')
        right.setIcon(
            QIcon(f'img/appIcon/{self._parent_.Puretheme}/arrow-right-line.svg'))
        right.clicked.connect(self.PathRight)
        right.iconPath = 'arrow-right-line.svg'
        self._parent_.changeIconList.append(right)
        right.setIconSize(QSize(18, 18))
        right.setToolTip('前进一级目录\nPath : next')
        right.installEventFilter(ToolTipFilter(
            right, 300, ToolTipPosition.BOTTOM))
        #
        back = QPushButton()
        back.setFixedSize(26, 26)
        back.setStyleSheet('''*{border-radius:0px;
                            border-left:0px;
                           }''')
        back.setIcon(
            QIcon(f'img/appIcon/{self._parent_.Puretheme}/corner-left-up-line.svg'))
        back.iconPath = 'corner-left-up-line.svg'
        self._parent_.changeIconList.append(back)
        back.clicked.connect(self.PathRight)
        back.setIconSize(QSize(18, 18))
        back.setToolTip('返回上一级目录\nReturn last path')
        back.installEventFilter(ToolTipFilter(
            back, 300, ToolTipPosition.BOTTOM))

        # change path
        changePath = QPushButton()
        changePath.setStyleSheet('''*{border-top-left-radius:0px;
                           border-bottom-left-radius:0px;
                            border-left:0px;
                           }''')
        changePath.setFixedSize(26, 26)
        changePath.clicked.connect(self.changeFolderPath)
        changePath.setIcon(
            QIcon(f'img/appIcon/{self._parent_.Puretheme}/folder-open-fill.svg'))
        changePath.iconPath = 'folder-open-fill.svg'
        self._parent_.changeIconList.append(changePath)
        changePath.setToolTip('更改目录 (选择一个文件夹)\nChange path (Choose a folder)')
        changePath.installEventFilter(ToolTipFilter(
            changePath, 300, ToolTipPosition.BOTTOM))
        changePath.setIconSize(QSize(18, 18))

        # new folder
        new_folder = QPushButton()
        new_folder.setFixedSize(26, 26)
        new_folder.setIcon(
            QIcon(f'img/appIcon/{self._parent_.Puretheme}/folder-add-line.svg'))
        new_folder.iconPath = 'folder-add-line.svg'
        self._parent_.changeIconList.append(new_folder)
        new_folder.setToolTip('新建文件夹\nNew folder')
        new_folder.installEventFilter(ToolTipFilter(
            new_folder, 300, ToolTipPosition.BOTTOM))
        new_folder.setStyleSheet('''*{border-top-right-radius:0px;
                           border-bottom-right-radius:0px;
                           }''')
        new_folder.setIconSize(QSize(16, 16))

        # file tree view mode
        self.fileTreeView = CreateFileTree()
        self._parent_.fileTreeView = self.fileTreeView
        self.fileTreeView.setRootIndex(
            self.fileTreeView.model_.index(self.thisPath))
        self.fileTreeView.setSortingEnabled(True)
        self.fileTreeView.setAnimated(True)
        self.fileTreeView.setAlternatingRowColors(True)
        self.fileTreeView.doubleClicked.connect(self.fileTreeViewDoubleClicked)

        self.fileTreeView.setObjectName('fileTreeView')
        self.fileTreeView.setAcceptDrops(False)
        self.fileTreeView.setEditTriggers(
            QtWidgets.QAbstractItemView.NoEditTriggers)
        self.fileTreeView.setDragDropMode(QtWidgets.QAbstractItemView.DragOnly)
        self.fileTreeView.setAnimated(True)
        NewCornerWidget = QWidget()
        NewCornerWidget.setObjectName('NewCornerWidget')
        self.fileTreeView.setCornerWidget(NewCornerWidget)

        ViewLayout = QHBoxLayout()
        ViewLayout.setContentsMargins(0, 0, 0, 0)
        ViewLayout.setSpacing(0)

        # view mode
        self.viewMode_1 = QPushButton()
        self.viewMode_1.setFixedSize(26, 26)
        self.viewMode_1.setObjectName('checkButton_1')
        self.viewMode_1.setToolTip('使用文件缩略图 视图\nUse file thumbnail view')
        self.viewMode_1.installEventFilter(ToolTipFilter(
            self.viewMode_1, 300, ToolTipPosition.BOTTOM))
        self.viewMode_1.setIcon(
            QIcon(f'img/appIcon/{self._parent_.Puretheme}/apps.svg'))
        '''self.viewMode_1.iconPath = 'apps.svg'
        self._parent_.changeIconList.append(self.viewMode_1)'''
        self.viewMode_1.clicked.connect(self.mode_1)
        self.viewMode_1.setStyleSheet('''*{border-radius:0px;
                            border-left:0px;
                           }''')
        #
        self.viewMode_2 = QPushButton()
        self.viewMode_2.setFixedSize(26, 26)
        self.viewMode_2.setToolTip('使用文件列表 视图\nUse file list view')
        self.viewMode_2.installEventFilter(ToolTipFilter(
            self.viewMode_2, 300, ToolTipPosition.BOTTOM))
        self.viewMode_2.setObjectName('checkButton_0')
        self.viewMode_2.setIcon(
            QIcon(f'img/appIcon/{self._parent_.Puretheme}/article.svg'))
        '''self.viewMode_2.iconPath = 'article.svg'
        self._parent_.changeIconList.append(self.viewMode_2)'''
        self.viewMode_2.setStyleSheet('''*{border-top-left-radius:0px;
                        border-bottom-left-radius:0px;
                        border-left:0px;
                           }''')

        self.viewMode_2.clicked.connect(self.mode_2)
        # add the view mode
        ViewLayout.addWidget(new_folder)
        ViewLayout.addWidget(self.viewMode_1)
        ViewLayout.addWidget(self.viewMode_2)

        # layout _1
        FileStructure_layout = QHBoxLayout(SearchWidget)
        #
        button_layout = QHBoxLayout()
        button_layout.setContentsMargins(0, 0, 0, 0)
        button_layout.setSpacing(0)
        button_layout.addWidget(left)
        button_layout.addWidget(right)
        button_layout.addWidget(back)
        button_layout.addWidget(changePath)

        #
        FileStructure_layout.addLayout(button_layout)
        FileStructure_layout.addWidget(SearchInput)
        FileStructure_layout.addLayout(ViewLayout)
        FileStructure_layout.setContentsMargins(5, 0, 5, 0)
        FileStructure_layout.setSpacing(7)
        #
        ################################################################

        self.AssetMainWidget = AssetWidget(
            self, self.thisPath.replace('\\', '/'), self.BottomLabel_1, self.AssetWidgetOpenFile, self.PathWidget, self.change_assetWidget)
        # layout
        self.AssetMainWidget.setStyleSheet(
            '''border-bottom-right-radius: 0px !important;
            border-bottom-left-radius: 0px !important;''')
        self.fileTreeView.setStyleSheet(
            '''border-bottom-right-radius: 0px !important;
            border-bottom-left-radius: 0px !important;''')

        self.FileViewWidget = QWidget()
        SmallLayout = QHBoxLayout(self.FileViewWidget)
        SmallLayout.setContentsMargins(0, 0, 0, 0)

        ViewWidget = QWidget()
        self.fileViewLayout = QStackedLayout(ViewWidget)
        self.fileViewLayout.setContentsMargins(0, 0, 0, 0)
        self.fileViewLayout.setSpacing(0)
        self.fileViewLayout.addWidget(self.AssetMainWidget)
        self.fileViewLayout.addWidget(self.fileTreeView)
        self.fileViewLayout.setCurrentIndex(0)

        TopWidget = QWidget()
        TopWidget.setFixedHeight(69)
        TopOptionLayout = QVBoxLayout(TopWidget)
        TopOptionLayout.setContentsMargins(0, 0, 0, 0)
        TopOptionLayout.addLayout(pathBGwidget_layout)
        TopOptionLayout.addWidget(SearchWidget)
        TopOptionLayout.setSpacing(4)
        #
        self.MainSplitter = QSplitter(Qt.Horizontal)

        self.MakeSplitter()
        self.MainSplitter.addWidget(self.FileViewWidget)
        # 调整是否隐藏侧边栏的按钮
        ButtonWidget = QWidget()
        ButtonWidget.setObjectName('AssetWidget')
        ButtonWidget.setStyleSheet(
            '#AssetWidget{border-radius:0px !important;}')
        ButtonLayout = QVBoxLayout(ButtonWidget)
        ButtonWidget.setFixedWidth(10)
        ButtonLayout.setContentsMargins(0, 5, 0, 0)
        self.IfHideLeftWidget = QPushButton()
        self.IfHideLeftWidget.setStyleSheet(
            '''background-color:rgba(0,0,0,0);
            border-top-left-radius:0px;
            border-bottom-left-radius:0px;''')
        self.IfHideLeftWidget.setIcon(
            QIcon(f'img/appIcon/{self._parent_.Puretheme}/arrow-drop-right-line.svg'))
        self.IfHideLeftWidget.iconPath = 'arrow-drop-right-line.svg'
        self._parent_.changeIconList.append(self.IfHideLeftWidget)
        self.IfHideLeftWidget.setFixedSize(10, 15)
        self.IfHideLeftWidget.IsExpend = 0
        self.IfHideLeftWidget.clicked.connect(self.clickExpendButton)
        # 绑定移动事件
        self.MainSplitter.splitterMoved.connect(self.splitterMoved)
        #
        ButtonLayout.addWidget(self.IfHideLeftWidget)
        ButtonLayout.addStretch(9999)
        SmallLayout.addWidget(ButtonWidget)
        SmallLayout.addWidget(ViewWidget)
        SmallLayout.setSpacing(0)
        #
        splitter_widget = QWidget()
        splitter_widget.setFixedHeight(7)
        self.Mainlayout.addWidget(TopWidget)
        self.Mainlayout.addWidget(splitter_widget)
        self.Mainlayout.addWidget(self.MainSplitter)
        self.Mainlayout.addWidget(self.BottomWidget)
        '''
        Asset window End
        set the path of the asset
        '''
        if self.openPath == './':
            self.openPath = os.getcwd().replace('\\', '/')
        self.AssetMainWidget.setRootPath(self.openPath)
        self.PathWidget.setRootPath(self.openPath)
        self.fileTreeView.setRootIndex(
            self.fileTreeView.model_.index(self.openPath))
        self._parent_.AssetWidgetOpenFile = self.AssetWidgetOpenFile
        self.mode_1()

    def clickExpendButton(self):
        if self.IfHideLeftWidget.IsExpend == 0:
            # 如果现在是没有展开的
            self.IfHideLeftWidget.IsExpend = 1  # 展开
            self.IfHideLeftWidget.setIcon(
                QIcon(f'img/appIcon/{self._parent_.Puretheme}/arrow-drop-left-line.svg'))
            self.IfHideLeftWidget.iconPath = 'arrow-drop-left-line.svg'
            self.MainSplitter.setSizes([1, 3])
        else:
            self.IfHideLeftWidget.IsExpend = 0  # 折叠
            self.IfHideLeftWidget.setIcon(
                QIcon(f'img/appIcon/{self._parent_.Puretheme}/arrow-drop-right-line.svg'))
            self.IfHideLeftWidget.iconPath = 'arrow-drop-right-line.svg'
            self.MainSplitter.setSizes([0, 1])

    def splitterMoved(self):
        if self.MainSplitter.sizes()[0] == 0:
            self.IfHideLeftWidget.IsExpend = 0
            self.IfHideLeftWidget.setIcon(
                QIcon(f'img/appIcon/{self._parent_.Puretheme}/arrow-drop-right-line.svg'))
            self.IfHideLeftWidget.iconPath = 'arrow-drop-right-line.svg'
        else:
            self.IfHideLeftWidget.IsExpend = 1
            self.IfHideLeftWidget.setIcon(
                QIcon(f'img/appIcon/{self._parent_.Puretheme}/arrow-drop-left-line.svg'))
            self.IfHideLeftWidget.iconPath = 'arrow-drop-left-line.svg'

    def MakeSplitter(self):
        # 创建splitter的左部分控件
        self.splitter_left_widget = QWidget()
        self.splitter_left_widget.setObjectName('AssetWidget')
        self.splitter_left_widget.setStyleSheet(
            '#AssetWidget{border-radius:0px !important;}')
        self.MainSplitter.addWidget(self.splitter_left_widget)
        #
        self.leftLayout = QVBoxLayout(self.splitter_left_widget)
        self.leftLayout.setContentsMargins(5, 5, 2, 5)
        # 用户目录
        UserPath_Widget = QWidget()
        UserPath_Layout = QVBoxLayout(UserPath_Widget)
        UserPath_Layout.setContentsMargins(5, 0, 5, 5)
        UserPathList = QListWidget()
        # 获取当前用户的文件夹路径
        user_folder_path = os.path.expanduser("~")
        # 存储获取到的文件夹路径的列表
        quick_access_folders = []
        # 在用户文件夹中列出文件和文件夹
        for item in os.listdir(user_folder_path):
            item_path = os.path.join(user_folder_path, item)
            if os.path.isdir(item_path):
                quick_access_folders.append(item_path)
                PathItem = QListWidgetItem()
                PathItem.setIcon(QIcon('img/appIcon/folder-base-svg.svg'))
                PathItem.setText(item)
                # 添加
                UserPathList.addItem(PathItem)
        NewCornerWidget_0 = QWidget()
        NewCornerWidget_0.setObjectName('NewCornerWidget')
        UserPathList.setCornerWidget(NewCornerWidget_0)
        # name
        UserPath_Widget.NameLabel = PureLabel()
        UserPath_Widget.NameLabel.setText(f'用户文件夹 ({os.getlogin()})')
        UserPath_Widget.NameLabel.setIcon(
            QIcon(f'img/appIcon/{self._parent_.Puretheme}/FolderFavorite_Icon.png'))
        UserPath_Widget.NameLabel.iconPath = 'FolderFavorite_Icon.png'
        self._parent_.changeIconList.append(UserPath_Widget.NameLabel)
        UserPath_Layout.addWidget(UserPath_Widget.NameLabel)
        UserPath_Layout.addWidget(UserPathList)
        UserPath_Panel = PureAttributePanel('用户文件夹', UserPath_Widget, True)

        # 链接
        Link_Widget = QWidget()
        Link_Layout = QVBoxLayout(Link_Widget)
        Link_Layout.setContentsMargins(5, 0, 5, 5)
        LinkList = QListWidget()
        # 获取当前用户的文件夹路径
        user_folder_path = os.path.expanduser("~")
        # 存储获取到的文件夹路径的列表
        quick_access_path = os.path.join(
            os.getenv("APPDATA"), "Microsoft", "Windows", "Recent")
        # 在用户文件夹中列出文件和文件夹
        # 获取指定目录的所有文件和子目录
        files_and_directories = os.listdir(quick_access_path)
        linkList = []
        # 打印实际文件的信息（过滤掉以 .lnk 结尾的文件）
        for item in files_and_directories:
            if not item.endswith(".lnk"):
                linkList.append(item)
                PathItem = QListWidgetItem()
                PathItem.setIcon(QIcon('img/appIcon/folder-database.svg'))
                PathItem.setText(item)
                # 添加
                LinkList.addItem(PathItem)
        NewCornerWidget_1 = QWidget()
        NewCornerWidget_1.setObjectName('NewCornerWidget')
        LinkList.setCornerWidget(NewCornerWidget_1)
        # name
        Link_Widget.NameLabel = PureLabel()
        Link_Widget.NameLabel.setText(f'链接文件夹 ({str(len(linkList))}个文件夹)')
        Link_Widget.NameLabel.setIcon(
            QIcon(f'img/appIcon/{self._parent_.Puretheme}/FolderFavorite_Icon.png'))
        Link_Widget.NameLabel.iconPath = 'FolderFavorite_Icon.png'
        self._parent_.changeIconList.append(Link_Widget.NameLabel)
        Link_Layout.addWidget(Link_Widget.NameLabel)
        Link_Layout.addWidget(LinkList)
        Link_Panel = PureAttributePanel('链接文件夹', Link_Widget, True)

        # 所有盘符
        DV_Widget = QWidget()
        DV_Layout = QVBoxLayout(DV_Widget)
        DV_Layout.setContentsMargins(5, 0, 5, 5)
        DVList = QListWidget()
        _DVList_ = [drive.device for drive in psutil.disk_partitions()]
        # 打印实际文件的信息（过滤掉以 .lnk 结尾的文件）
        for item in _DVList_:
            PathItem = QListWidgetItem()
            PathItem.setIcon(QIcon('img/appIcon/dmg.svg'))
            PathItem.setText(item)
            # 添加
            DVList.addItem(PathItem)
        NewCornerWidget_2 = QWidget()
        NewCornerWidget_2.setObjectName('NewCornerWidget')
        DVList.setCornerWidget(NewCornerWidget_2)
        # name
        DV_Widget.NameLabel = PureLabel()
        DV_Widget.NameLabel.setText(f'磁盘 ({str(len(_DVList_))}个磁盘)')
        DV_Widget.NameLabel.setIcon(
            QIcon(f'img/appIcon/{self._parent_.Puretheme}/FolderFavorite_Icon.png'))
        DV_Widget.NameLabel.iconPath = 'FolderFavorite_Icon.png'
        self._parent_.changeIconList.append(DV_Widget.NameLabel)
        DV_Layout.addWidget(DV_Widget.NameLabel)
        DV_Layout.addWidget(DVList)
        DV_Panel = PureAttributePanel('磁盘', DV_Widget, True)

        # 添加进去
        self.leftLayout.addWidget(UserPath_Panel)
        self.leftLayout.addWidget(DV_Panel)
        self.leftLayout.addWidget(Link_Panel)
        self.leftLayout.addStretch(9999)
        # 设置大小
        self.MainSplitter.setSizes([0, 5])

    def change_path(self, path):
        '''
            [3] 在pathWidget里改变目录 
            '''
        self.AssetMainWidget.setRootPath(path)
        self.fileTreeView.setRootIndex(
            self.fileTreeView.model_.index(path))
        self.thisPath = path
        self.check_edittime_file(path)

    def change_assetWidget(self, path):
        '''
            [4] 在assetWdiget里改变目录
            '''
        self.thisPath = path
        self.check_edittime_file(path)
        self.fileTreeView.setRootIndex(
            self.fileTreeView.model_.index(path))

    def AssetWidgetOpenFile(self, filePath: str) -> None:
        '''
        open file in Asset viewer Widget
        filePath:str -> Path
        '''
        fileType = filePath.split('/')[-1].split('.')[-1]
        # 如果文件类型不是nbt,mca,mcfunction 就使用外部编辑器来打开他
        if fileType != 'nbt' and fileType != 'mca':
            if filePath.split('/')[-1] not in self._parent_.file_list:
                try:
                    with open(filePath, 'r', encoding='utf-8') as openFile:
                        # name , data
                        self._parent_.add_file(
                            filePath.split('/')[-1], openFile.read(), filePath)
                        self._parent_.file_list.append(filePath.split('/')[-1])
                except:
                    print(
                        f'cannot open file <{filePath}> in encoding("utf-8")')
                    runPath = self.filePath.replace("\\", "/")
                    os.system(f'start {runPath}')

        elif fileType == 'nbt':
            self.openNbtFileWithPath(filePath)

    # function 2

    def openNbtFileWithPath(self, filePath):
        print('[open:2] : openNbtFileWithPath')
        # start
        self.filePath = filePath.replace('\\', '/')
        self._parent_.filePath = self.filePath
        fileType = self.filePath.split('/')[-1].split('.')[-1]
        ThisPath = '/'.join(self.filePath.split('/')[:-1])
        ThisName = self.filePath.split('/')[-1][:-4]
        # change title
        # step 1
        if self.filePath != '':
            # check if file exists and changed
            if fileType == 'nbt':
                if os.path.exists(ThisPath + '/'+'__NBTFileChangedTime__'):
                    print('[open:1] : file was in recorded directory')
                    with open(ThisPath + '/'+'__NBTFileChangedTime__', 'r', encoding='utf8') as record:
                        recordDict = eval(record.read())
                    getTime = os.stat(self.filePath).st_mtime
                    if recordDict[self.filePath] == getTime:
                        print(
                            '[open:1] : nbt file was not changed , use last OBJ file')
                        if os.path.exists(ThisPath+'/'+ThisName+'.obj'):
                            # 文件最后修改时间一致,并且可以找到模型文件，则直接加载模型文件
                            print('[open:1] : last OBJ was exists')
                            self.LoadLastNBTFile(
                                self.filePath, ThisPath+'/'+ThisName+'.obj')
                        else:
                            # 文件最后修改时间一致,但是找不到模型文件，则重新生成
                            self.creatModel()
                    else:
                        # 文件最后修改时间不一致，重新生成
                        self.creatModel()
            else:
                self.creatModel()

    def LoadLastNBTFile(self, filePath: str, Objpath: str):
        '''
        用来加载已有的nbt:obj模型,使用外部类LastNBTFile来调用loadNbtModelFunction
        '''
        self._parent_.filePath = self.filePath
        name = 'newLastNBTThread_'+str(self.thread_count)
        globals()[name
                  ] = NBTLastFileThread(self.filePath, Objpath, self._parent_.treeViewList, self._parent_)
        exec(name +
             '.finished.connect('+name+'.deleteLater)')
        exec(name + '.start()')
        self.thread_count += 1

    def creatModel(self):
        #
        self._parent_.filePath = self.filePath
        name = 'newThread_'+str(self.thread_count)
        globals()[name
                  ] = NbtTreeThread(self.filePath, self._parent_.treeViewList, parent=self._parent_, have_viewer=True)
        exec(name +
             '.finished.connect('+name+'.deleteLater)')
        exec(name + '.start()')
        self.thread_count += 1

    def changeFolderPath(self):
        self._parent_.filePath = self.filePath
        '''
        [1] 在按钮里改变目录
        '''
        folder_path = QFileDialog.getExistingDirectory(self, "选择目录")
        if folder_path != '':
            self.AssetMainWidget.setRootPath(folder_path)
            self.PathWidget.setRootPath(folder_path)
            self.thisPath = folder_path
            self.check_edittime_file(folder_path)
            self.fileTreeView.setRootIndex(
                self.fileTreeView.model_.index(folder_path))

    def SystemChangeFolderPath(self, path):
        '''
        系统改变目录，从外部调用
        '''
        self.AssetMainWidget.setRootPath(path)
        self.PathWidget.setRootPath(path)
        self.thisPath = path
        self.check_edittime_file(path)
        self.fileTreeView.setRootIndex(
            self.fileTreeView.model_.index(path))

    def fileTreeViewDoubleClicked(self, index):
        '''
        [2] 在fileTreeView里改变目录
        '''
        Path = self.fileTreeView.model().filePath(index)
        print(Path)
        if os.path.isdir(Path) != True:
            # 打开文件
            self.AssetWidgetOpenFile(Path)
        else:
            self.AssetMainWidget.setRootPath(Path)
            self.PathWidget.setRootPath(Path)
            self.fileTreeView.setRootIndex(
                self.fileTreeView.model_.index(Path))
            self.thisPath = Path
            self.check_edittime_file(Path)

    def check_edittime_file(self, path: str) -> None:
        '''
        检查 记录:nbt文件的最后修改时间 的文件是否存在,如果存在则尝试更新,如果不存在则创建
        '''
        if os.path.exists(path+'/'+'__NBTFileChangedTime__'):
            # 检查和更新
            print('[>] : path :', path+'/'+'__nBTFileChangedTime__',
                  'has already been recorded, try to update it')
            pass
        else:
            with open(path+'/'+'__NBTFileChangedTime__', 'w', encoding='utf8') as record:
                FileChangeTime = {}
                dir_or_files = os.listdir(path)
                for dir_file in dir_or_files:
                    dir_file_path = os.path.join(path, dir_file)
                    if dir_file_path.split('/')[-1].split('.')[-1] == 'nbt':
                        FileChangeTime[dir_file_path.replace('\\', '/')] = os.stat(
                            dir_file_path).st_mtime
                record.write(str(FileChangeTime))
            print('[>] : path :', path+'/' +
                  '__NBTFileChangedTime__', 'creat successful')

    def PathLeft(self):
        # change path
        self.thisPath = '/'.join(self.thisPath.split('/')[:-1])
        self.AssetMainWidget.setRootPath(self.thisPath)
        self.fileTreeView.setRootIndex(
            self.fileTreeView.model_.index(self.thisPath))

    def PathRight(self):
        # change path
        newpath = self.thisPath
        dir_or_files = os.listdir(self.thisPath)
        for dir_file in dir_or_files:
            dir_file_path = os.path.join(self.thisPath, dir_file)
            if os.path.isdir(dir_file_path):
                newpath = dir_file_path.replace('\\', '/')
                self.thisPath = newpath
                break

        self.AssetMainWidget.setRootPath(newpath)
        self.fileTreeView.setRootIndex(self.fileTreeView.model_.index(newpath))
        self.fileTreeView.update()

    def mode_1(self):
        print('mode 1', self.thisPath)
        self.viewMode_2.setEnabled(1)
        self.viewMode_1.setEnabled(0)

        self.viewMode_2.setObjectName('checkButton_0')
        self.viewMode_2.setStyleSheet('''*{
                                      border-top-left-radius:0px;
                        border-bottom-left-radius:0px;
                        border-left:0px;
                                      }''')
        self.viewMode_1.setObjectName('checkButton_1')
        self.viewMode_1.setStyleSheet('''*{
                                border-radius:0px !important;
                            border-left:0px;
                                      }''')
        # fileTreeView -> AssetMainWidget
        self.fileViewLayout.setCurrentIndex(0)
        self.AssetMainWidget.setRootPath(self.thisPath)
        self.fileTreeView.setRootIndex(
            self.fileTreeView.model_.index(self.thisPath))
        self.fileTreeView.update()

    def mode_2(self):
        print('mode 2', self.thisPath)
        self.viewMode_2.setEnabled(0)
        self.viewMode_1.setEnabled(1)

        self.viewMode_1.setObjectName('checkButton_0')
        self.viewMode_1.setStyleSheet('''*{
                            border-radius:0px;
                            border-left:0px;
                                      }''')
        self.viewMode_2.setObjectName('checkButton_1')
        self.viewMode_2.setStyleSheet('''*{
                        border-top-left-radius:0px;
                        border-bottom-left-radius:0px;
                        border-left:0px;}
                                      ''')
        # AssetMainWidget -> fileTreeView
        self.fileViewLayout.setCurrentIndex(1)
        self.fileTreeView.setRootIndex(
            self.fileTreeView.model_.index(self.thisPath))
        self.AssetMainWidget.setRootPath(self.thisPath)
        self.fileTreeView.update()
