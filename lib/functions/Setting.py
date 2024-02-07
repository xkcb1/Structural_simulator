import numpy
from lib.Widgets.comboBox import PureComboBox, PureLabel
from lib.Widgets.panel import PureAttributePanel
from lib.base import *
from lib.base import _Thread_


class Setting(QWidget):
    def __init__(self, parent=None, window=None, openPath=''):
        super(Setting, self).__init__()
        self._parent_ = parent
        self._window_ = window
        self.openPath = openPath
        '''
        生成Simulator页面的config_Window窗口
        title:Import
        '''
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
        #
        self.ThisMainWidget = QWidget()
        self.Mainlayout.addWidget(self.ThisMainWidget)
        # 使用QScrollArea
        self.mainWidget = self.ThisMainWidget
        self.setMinimumWidth(270)
        mainLayout = QVBoxLayout(self.ThisMainWidget)
        mainLayout.setContentsMargins(0, 0, 0, 0)
        mainLayout.setSpacing(0)

        self.InfoWidget_main = QWidget()
        self.InfoWidget_main.setObjectName('AssetWidget')
        self.InfoWidget_mainLayout = QVBoxLayout(self.InfoWidget_main)
        self.InfoWidget_mainLayout.setContentsMargins(5, 5, 5, 5)
        self.InfoWidget = QWidget()
        # 打开文件
        self.OpenFileButton = QPushButton()
        self.OpenFileButton.setText('选择配置文件')
        self.OpenFileButton.setFixedHeight(50)
        self.OpenFileButton.setObjectName('open_button')
        self.OpenFileButton.setIcon(
            QIcon(f'img/appIcon/{self._parent_.Puretheme}/folder-open-fill.svg'))
        self.OpenFileButton.iconPath = 'folder-open-fill.svg'
        self._parent_.changeIconList.append(self.OpenFileButton)
        self.OpenFileButton.clicked.connect(self.OpenGeneration)
        #
        self.InfoWidget_mainLayout.addWidget(self.OpenFileButton)
        self.InfoWidget_mainLayout.addWidget(self.InfoWidget)
        #
        self.infoLayout = QVBoxLayout(self.InfoWidget)
        self.infoLayout.setContentsMargins(0, 0, 0, 0)

        mainLayout.setSpacing(0)
        # start the main

        self.TopMenuWidget = QWidget()
        self.TopMenuWidget.setFixedHeight(30)
        self.topLayout = QHBoxLayout(self.TopMenuWidget)
        self.topLayout.setContentsMargins(5, 0, 5, 3)

        mainLayout.addWidget(self.TopMenuWidget)
        mainLayout.addWidget(self.InfoWidget_main)
        # 顶部栏

        # 文件路径
        self.filePath = QLineEdit()
        self.filePath.setFixedHeight(24)
        self.filePath.setPlaceholderText('Json file path')
        self.filePath.setReadOnly(1)
        self.filePath.setObjectName('SearchPathWidget')

        # 生物群落 (biomes)
        self.biomes = PureComboBox('生物群落 (biomes)')
        self.biomes.setFixedHeight(24)
        self.biomes.setFixedWidth(40)
        self.biomes.setIcon(
            QIcon(f'img/appIcon/{self._parent_.Puretheme}/TerrainToolSetheightAlt.png'))
        self.biomes.iconPath = 'TerrainToolSetheightAlt.png'
        self._parent_.changeIconList.append(self.biomes)

        # 开始解析和模拟
        self.optWidget = QWidget()
        self.optLayout = QHBoxLayout(self.optWidget)
        self.optLayout.setContentsMargins(0, 0, 0, 0)
        self.optLayout.setSpacing(0)
        # 开始按钮
        self.startButton = QPushButton()
        self.startButton.setIcon(
            QIcon(f'img/appIcon/{self._parent_.Puretheme}/play-fill.svg'))
        self.startButton.iconPath = 'play-fill.svg'
        self._parent_.changeIconList.append(self.startButton)
        self.startButton.setFixedSize(24, 24)
        self.startButton.setStyleSheet('''*{border-top-right-radius:0px;
                           border-bottom-right-radius:0px;
                           }''')
        self.startButton.setEnabled(0)
        self.startButton.clicked.connect(self.Generation_Structure)

        self.resetButton = QPushButton()
        self.resetButton.setIcon(
            QIcon(f'img/appIcon/{self._parent_.Puretheme}/refresh-line.svg'))
        self.resetButton.iconPath = 'refresh-line.svg'
        self._parent_.changeIconList.append(self.resetButton)
        self.resetButton.setFixedSize(24, 24)
        self.resetButton.setStyleSheet('''*{border-radius:0px;
                            border-left:0px;
                           }''')

        # 提示按钮
        self.whatthis = QPushButton()
        self.whatthis.setIcon(
            QIcon(f'img/appIcon/{self._parent_.Puretheme}/question-fill.svg'))
        self.whatthis.iconPath = 'question-fill.svg'
        self._parent_.changeIconList.append(self.whatthis)
        self.whatthis.setFixedSize(24, 24)
        self.whatthis.setStyleSheet('''*{border-top-left-radius:0px;
                        border-bottom-left-radius:0px;
                        border-left:0px;
                           }''')
        # 添加进操作布局
        self.optLayout.addWidget(self.startButton)
        self.optLayout.addWidget(self.resetButton)
        self.optLayout.addWidget(self.whatthis)

        # 添加进顶部布局
        self.topLayout.addWidget(self.biomes)
        self.topLayout.addWidget(self.filePath)
        self.topLayout.addWidget(self.optWidget)

    def OpenGeneration(self):
        try:
            # 尝试清除一遍之前的布局
            item_list = list(
                range(self.infoLayout.count()))
            item_list.reverse()  # 倒序删除，避免影响布局顺序
            for i in item_list:
                item = self.infoLayout.itemAt(i)
                self.infoLayout.removeItem(item)
                if item.widget():
                    item.widget().deleteLater()
        except:
            pass

        # 打开生成器配置文件
        Generation_choose = FileSelector(
            'Select the Generation Config', 'Json (*.json)')
        self.Generation = Generation_choose.fileName
        if self.Generation != '':
            fileType = self.Generation.split('/')[-1].split('.')[-1]
            ThisPath = '/'.join(self.Generation.split('/')[:-1])
            ThisName = self.Generation.split('/')[-1]
            self.filePath.setText(self.Generation)
            with open(self.Generation, 'r', encoding='utf-8') as GenerationFile:
                getGeneration = GenerationFile.read()
            with open(self.Generation, 'r', encoding='utf-8') as GenerationFile_json:
                data = json.load(GenerationFile_json)

            print('this folder is :', self.Generation)
            self.Generation_data = data
            self.Generation_data['name'] = ThisName.replace('.json', '')

            # setInfo
            # check
            self.Structure_Json_Needed = ['start_pool', 'type', 'biomes', 'max_distance_from_center',
                                          'size', 'start_height', 'step']
            for needed in self.Structure_Json_Needed:
                if needed not in data:
                    errorMessage = '<a style="color:red;">Error Generation Config</a><p style="color:indianred;"></p>'
                    QMessageBox.critical(
                        self, 'Error Chech Generation Config', errorMessage)
                    return
            # 添加title

            # self.infoLayout.addWidget(titleLabel)
            # info panel
            infoPanel = QWidget()
            infpPanelLayout = QGridLayout(infoPanel)
            infpPanelLayout.setContentsMargins(5, 0, 5, 5)

            InfoAttributePanel = PureAttributePanel(
                ThisName+' 文件信息', infoPanel, True, 'img/toolbar/CGProgram_Icon.png')
            # ====== info panel start ====== #

            # start_pool
            Json_StartPool = PureLabel()
            Json_StartPool.setText('start_pool')
            Json_StartPool.setFixedHeight(25)
            Json_StartPool.setIcon(QIcon('img/toolbar/CollabMoved_Icon.png'))
            infpPanelLayout.addWidget(Json_StartPool, 0, 0)
            StartPool = QLabel()
            StartPool.setText(data['start_pool'])
            infpPanelLayout.addWidget(StartPool, 0, 1)

            # type
            Json_Type = PureLabel()
            Json_Type.setText('type')
            Json_Type.setFixedHeight(25)
            Json_Type.setIcon(QIcon('img/toolbar/CollabChanges_Icon.png'))
            infpPanelLayout.addWidget(Json_Type, 1, 0)
            Type = QLabel()
            Type.setText(data['type'])
            infpPanelLayout.addWidget(Type, 1, 1)

            # bioms
            biomesIcon = []
            BiomsList = QListWidget()
            for _biomes_name_ in data['biomes']:
                if os.path.exists('img/biomes/java/'+_biomes_name_.replace('_', '-').replace('minecraft:', 'BiomeSprite_')+'.png'):
                    icon = 'img/biomes/java/' + \
                        _biomes_name_.replace(
                            '_', '-').replace('minecraft:', 'BiomeSprite_')+'.png'
                    biomesIcon.append(icon)
                else:
                    icon = ''
                    biomesIcon.append(icon)
                Item = QListWidgetItem(QIcon(icon), _biomes_name_, BiomsList)
                BiomsList.addItem(Item)
            NewCornerWidget = QWidget()
            NewCornerWidget.setObjectName('NewCornerWidget')
            BiomsList.setCornerWidget(NewCornerWidget)

            self.biomes.setMenuList(data['biomes'], biomesIcon)
            Json_biomes = PureLabel()
            Json_biomes.setText(
                'biomes')
            Json_biomes.setFixedHeight(25)
            Json_biomes.setIcon(
                QIcon('img/toolbar/CollabChanges_Icon.png'))
            infpPanelLayout.addWidget(Json_biomes, 2, 0)
            infpPanelLayout.addWidget(BiomsList, 2, 1)

            # max_distance_from_center
            Json_max_distance_from_center = PureLabel()
            Json_max_distance_from_center.setText(
                'max_distance_from_center')
            Json_max_distance_from_center.setFixedHeight(25)
            Json_max_distance_from_center.setIcon(
                QIcon('img/toolbar/CollabChanges_Icon.png'))
            infpPanelLayout.addWidget(Json_max_distance_from_center, 3, 0)
            max_distance_from_center = QLabel()
            max_distance_from_center.setText(
                str(data['max_distance_from_center']))
            infpPanelLayout.addWidget(max_distance_from_center, 3, 1)

            # size
            Json_Size = PureLabel()
            Json_Size.setText(
                'size')
            Json_Size.setFixedHeight(25)
            Json_Size.setIcon(
                QIcon('img/toolbar/CollabChanges_Icon.png'))
            infpPanelLayout.addWidget(Json_Size, 4, 0)
            Size = QLabel()
            Size.setText(
                str(data['size']))
            infpPanelLayout.addWidget(Size, 4, 1)

            # start_height -> absolute
            Json_start_height = PureLabel()
            Json_start_height.setText(
                'start_height')
            Json_start_height.setFixedHeight(25)
            Json_start_height.setIcon(
                QIcon('img/toolbar/CollabChanges_Icon.png'))
            infpPanelLayout.addWidget(Json_start_height, 5, 0)
            start_height = QLabel()
            start_height.setText(
                str(data['start_height']['absolute']))
            infpPanelLayout.addWidget(start_height, 5, 1)

            # Step
            Json_Step = PureLabel()
            Json_Step.setText(
                'step')
            Json_Step.setFixedHeight(25)
            Json_Step.setIcon(
                QIcon('img/toolbar/CollabChanges_Icon.png'))
            infpPanelLayout.addWidget(Json_Step, 6, 0)
            Step = QLabel()
            Step.setText(
                data['step'])
            infpPanelLayout.addWidget(Step, 6, 1)

            # enable
            self.startButton.setEnabled(1)

            # nbt panel
            self.NbtPanel = QWidget()
            self.NbtPanelLayout = QVBoxLayout(self.NbtPanel)
            self.NbtPanelLayout.setContentsMargins(5, 0, 5, 5)
            self.NbtTitle = QLabel('所有使用到的Nbt文件')
            self.NbtList = QListWidget()
            NewCornerWidget_2 = QWidget()
            NewCornerWidget_2.setObjectName('NewCornerWidget')
            self.NbtList.setCornerWidget(NewCornerWidget_2)
            self.NbtPanelLayout.addWidget(self.NbtTitle)
            self.NbtPanelLayout.addWidget(self.NbtList)

            self.NbtAttributePanel = PureAttributePanel(
                'Nbt 文件列表', self.NbtPanel, True, 'img/main_3/Nbt.png')

            self.infoLayout.addWidget(InfoAttributePanel)
            self.infoLayout.addWidget(self.NbtAttributePanel)

            self.infoLayout.addStretch(9999)

        # set the widget

    def Generation_Structure(self):
        '''
        生成器主函数
        Generation Main
        '''
        pass

    def StartGenerate(self, argv=None):
        '''
        生成器的主函数,在子线程里运行
        模板池权重在1-150(包含)之间
        '''
        # 获取参数,初始模版池以及迭代次数
        path = argv.path

    def setSTRUCTURE_RightWidget(self, generation, name):
        print(name)
        count = 0
        for item in generation:
            count += len(generation[item])
            for nbt in generation[item]:
                print(nbt['NBT_DATA'])
        print(count)
