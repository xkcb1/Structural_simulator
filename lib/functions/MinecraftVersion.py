from lib.Widgets.comboBox import PureLabel
from lib.Widgets.panel import PureAttributePanel
from lib.base import *
from lib.base import _Thread_


class MinecraftVersion(QWidget):
    def __init__(self, parent=None, window=None, openPath=''):
        super(MinecraftVersion, self).__init__()
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
        self.Mainlayout.setContentsMargins(5, 4, 0, 5)
        self.Mainlayout.setSpacing(0)
        #
        self.SplitterWidget = QSplitter(Qt.Horizontal)
        self.Mainlayout.addWidget(self.SplitterWidget)
        #
        self.LeftWidget = QWidget()
        self.LeftWidget.setObjectName('AssetWidget')

        self.RightWidget = QWidget()
        self.SplitterWidget.addWidget(self.LeftWidget)
        self.SplitterWidget.addWidget(self.RightWidget)
        self.SplitterWidget.setSizes([1, 2])
        #
        self.leftLayout = QVBoxLayout(self.LeftWidget)
        # 搜索框
        self.SearchInput = QLineEdit()
        self.SearchInput.setFixedHeight(24)
        self.SearchInput.setPlaceholderText('Search for Version...')
        self.SearchInput.setObjectName('SearchPathWidget')
        self.SearchInput.setClearButtonEnabled(1)
        self.SearchInput.setStyleSheet(
            '''* {
                padding-left: 15px;
                background-image: url(./img/appIcon/d_Search.png);
                background-repeat: no-repeat;
                background-position: left center;
                }''')

        self.leftLayout.addWidget(self.SearchInput)

        # 版本列表
        downloadWidget = QWidget()
        downlodeLayout = QVBoxLayout(downloadWidget)
        downlodeLayout.setContentsMargins(5, 0, 5, 5)
        downLoadLabel = PureLabel()
        downLoadLabel.setIcon(
            QIcon(f'img/appIcon/{self._parent_.Puretheme}/Folder_Icon.png'))
        downLoadLabel.iconPath = 'Folder_Icon.png'
        self._parent_.changeIconList.append(downLoadLabel)
        # 版本列表
        self.VersionList = QListWidget()
        with open('./versions.json', 'r', encoding='utf-8') as version_json:
            Versions = eval(version_json.read())
        downlodeLayout.addWidget(downLoadLabel)
        downlodeLayout.addWidget(self.VersionList)

        downLoadLabel.setText('安装游戏版本 - '+str(len(Versions))+'个可安装版本')
        Version_Panel = PureAttributePanel('安装游戏', downloadWidget, True)

        # 已安装版本
        IsdownloadWidget = QWidget()
        IsdownloadLayout = QVBoxLayout(IsdownloadWidget)
        IsdownloadLayout.setContentsMargins(5, 0, 5, 5)
        downloadVersionLabel = PureLabel()
        downloadVersionLabel.setText('已安装的游戏版本 - 0个已安装版本')
        downloadVersionLabel.setIcon(
            QIcon(f'img/appIcon/{self._parent_.Puretheme}/FolderFavorite_Icon.png'))
        downloadVersionLabel.iconPath = 'FolderFavorite_Icon.png'
        self._parent_.changeIconList.append(downloadVersionLabel)
        # 已安装版本列表
        self.downloadVersion = QListWidget()
        IsdownloadLayout.addWidget(downloadVersionLabel)
        IsdownloadLayout.addWidget(self.downloadVersion)
        DownloadVersion_Panel = PureAttributePanel(
            '已安装的游戏', IsdownloadWidget, True)

        self.leftLayout.addWidget(Version_Panel)
        self.leftLayout.addWidget(DownloadVersion_Panel)
        self.leftLayout.addStretch(9999)

        # 打印版本信息
        for version in Versions:
            versionItem = QListWidgetItem()
            versionItem.setSizeHint(QSize(200, 35))
            Name = QLabel(version['id'])
            Name.setStyleSheet(
                'font-size:13px;font-weight:bold;background-color:rgba(0,0,0,0);')
            Icon = PureLabel()
            Icon.setIconSize(QSize(24, 24))
            if version['type'] == 'snapshot':
                Icon.setIcon(QIcon('img/fileicon/MC_1.png'))
            elif version['type'] == 'release':
                Icon.setIcon(QIcon('img/fileicon/MC_4.png'))
            else:
                Icon.setIcon(QIcon('img/fileicon/MC_5.png'))

            TypeLabel = QLabel("版本类型 : "+version['type'])
            TypeLabel.setStyleSheet(
                'color:gray;background-color:rgba(0,0,0,0);')
            itemWidget = QWidget()
            itemWidget.setFixedHeight(35)
            # layout
            layout = QHBoxLayout(itemWidget)
            layout.setContentsMargins(5, 2, 0, 2)
            layout.addWidget(Icon)
            #
            vLayout = QVBoxLayout()
            vLayout.addWidget(Name)
            vLayout.addWidget(TypeLabel)
            layout.addLayout(vLayout)
            layout.addStretch(10)
            # add
            self.VersionList.addItem(versionItem)
            self.VersionList.setItemWidget(versionItem, itemWidget)
