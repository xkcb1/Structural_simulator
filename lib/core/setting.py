import sys
from lib.base import *
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication


class SettingWindow:

    def __init__(self, mainwindow: QMainWindow, app):
        super().__init__()
        self.mainwindow = mainwindow
        self.app = app

        # window
        self.Window = QMainWindow(self.mainwindow)

        if platform.system() == 'Windows':
            from win32mica import ApplyMica, MicaTheme, MicaStyle
            import win32mica

            def callbackFunction(NewTheme):
                if NewTheme == MicaTheme.DARK:
                    print("Theme has changed to dark!")

                else:
                    print("Theme has changed to light!")
            hwnd = self.Window.winId().__int__()
            mode = MicaTheme.AUTO

            style = MicaStyle.DEFAULT
            win32mica.ApplyMica(HWND=hwnd, Theme=mode, Style=style,
                                OnThemeChange=callbackFunction)
        else:
            print(
                f'System : {platform.system()} cannot use Mica Style in {self.Window.winId()}')

        self.Window.setWindowTitle("Preference")
        self.Window.setWindowIcon(
            QIcon('img/RemixIcon/icons/System/settings-4-fill.svg'))
        self.Window.resize(715, 440)
        self.Window.setMinimumSize(715, 440)

        # make window
        self.makeWindow()

        # show
        self.Window.show()

    def makeWindow(self):
        self.Window.MainWidget = QWidget()
        self.Window.setContentsMargins(0, 0, 0, 0)
        self.Window.setCentralWidget(self.Window.MainWidget)

        self.Window.layout = QHBoxLayout(self.Window.MainWidget)
        self.Window.layout.setContentsMargins(0, 0, 0, 0)

        self.leftDiv_main = QWidget()
        self.leftDiv_main.setFixedWidth(150)
        self.leftDiv_main_layout = QVBoxLayout(self.leftDiv_main)
        self.leftDiv_main_layout.setContentsMargins(5, 5, 0, 5)
        self.leftDiv_main_layout.setSpacing(3)

        self.leftDiv = QTreeWidget(self.leftDiv_main)
        self.rightDiv = QWidget()
        self.rightDiv.setObjectName('rightDiv')
        self.rightDiv.setContentsMargins(0, 0, 0, 0)

        self.Stacked = QStackedLayout(self.rightDiv)
        self.Stacked.setContentsMargins(0, 5, 5, 5)
        # add widget
        self.makePage()

        self.Window.layout.addWidget(self.leftDiv_main)
        self.Window.layout.addWidget(self.rightDiv)

        SearchInput = QLineEdit()
        SearchInput.setPlaceholderText('Search for options...')
        SearchInput.setObjectName('SearchPathWidget')

        self.leftDiv.header().hide()
        self.leftDiv_main_layout.addWidget(SearchInput)
        self.leftDiv_main_layout.addWidget(self.leftDiv)

        Editor = QTreeWidgetItem()
        Editor.setText(0, 'Editor')
        Editor.setIcon(0, QIcon('./img/svg/app-window-filled.svg'))
        self.leftDiv.addTopLevelItem(Editor)

        Simple = QTreeWidgetItem()
        Simple.setText(0, 'Simple')
        Simple.setIcon(0, QIcon('./img/settings.svg'))
        Theme = QTreeWidgetItem()
        Theme.setIcon(0, QIcon('./img/brightness.svg'))
        Theme.setText(0, 'Theme')
        Three_D = QTreeWidgetItem()
        Three_D.setText(0, '3d viewer')
        Three_D.setIcon(0, QIcon('./img/table-options.svg'))

        Editor.addChildren([Simple, Theme, Three_D])
        Editor.setExpanded(True)

        System = QTreeWidgetItem()
        System.setText(0, 'System')
        System.setIcon(0, QIcon('./img/device-desktop.svg'))
        self.leftDiv.addTopLevelItem(System)
        System.setExpanded(True)

        Python = QTreeWidgetItem()
        Python.setText(0, 'Python')
        Python.setIcon(0, QIcon('./img/brand-python.svg'))
        system_ = QTreeWidgetItem()
        system_.setText(0, 'Platform')
        system_.setIcon(0, QIcon('./img/brand-windows.svg'))

        System.addChildren([Python, system_])

        Config = QTreeWidgetItem()
        Config.setText(0, 'Config')
        Config.setIcon(0, QIcon('./img/text-caption.svg'))
        self.leftDiv.addTopLevelItem(Config)
        Config.setExpanded(True)

        def TreeClicked(index):
            item = self.leftDiv.currentItem()
            getOptions = item.text(0)
            # make right
            if getOptions == 'Editor':
                self.Stacked.setCurrentIndex(0)
            elif getOptions == 'Simple':
                self.Stacked.setCurrentIndex(1)
            elif getOptions == 'Theme':
                self.Stacked.setCurrentIndex(2)
            elif getOptions == '3d viewer':
                self.Stacked.setCurrentIndex(3)
            elif getOptions == 'System':
                self.Stacked.setCurrentIndex(4)
            elif getOptions == 'Python':
                self.Stacked.setCurrentIndex(5)
            elif getOptions == 'Platform':
                self.Stacked.setCurrentIndex(6)
            elif getOptions == 'Config':
                self.Stacked.setCurrentIndex(7)

        self.leftDiv.selectionModel().currentChanged.connect(TreeClicked)

    def makePage(self):
        self.page_0 = QWidget()
        self.page_0.setObjectName('page_x')
        # make page 0
        layout_main_0 = QVBoxLayout(self.page_0)
        layout_main_0.setContentsMargins(0, 40, 0, 0)
        layout_widget_0 = QWidget()
        layout_widget_0.setObjectName('page_0')
        layout_0 = QGridLayout(layout_widget_0)
        layout_main_0.addWidget(layout_widget_0)
        layout_main_0.addStretch(999)
        #
        label_0 = QLabel(self.page_0)
        label_0.setText('Editor')
        label_0.setStyleSheet('font-weight:bold;font-size:17px;')
        label_0.move(10, 10)
        #
        appIconName = QLabel('app Icon :')
        appIcon = QPushButton()
        appIcon.setIcon(QIcon('./img/appIcon_2.png'))
        appIcon.setIconSize(QSize(64, 64))
        appIcon.setFixedSize(64, 64)
        #
        appIcon2 = QPushButton()
        appIcon2.setIcon(QIcon('./img/mcEarth_2.png'))
        appIcon2.setIconSize(QSize(64, 64))
        appIcon2.setFixedSize(64, 64)
        #
        appIcon3 = QPushButton()
        appIcon3.setIcon(QIcon('./img/mcEarthImage.png'))
        appIcon3.setIconSize(QSize(64, 64))
        appIcon3.setFixedSize(64, 64)
        #
        self.title = QLabel()
        self.title.setText('app Title :')
        self.title_input = QLineEdit()
        self.title_input.setText(self.mainwindow.windowTitle())
        self.title_input.textChanged.connect(
            lambda: self.mainwindow.setWindowTitle(self.title_input.text()))
        #
        layout_0.addWidget(appIconName, 0, 0)
        layout_0.addWidget(appIcon, 0, 1)
        #
        layout_0.addWidget(self.title, 1, 0)
        layout_0.addWidget(self.title_input, 1, 1)
        #
        layout_0.addWidget(QLabel('app Version :'), 2, 0)
        layout_0.addWidget(QLabel('0.0.2 beta'), 2, 1)
        #
        layout_0.addWidget(QLabel('app use Lib :'), 3, 0)
        layout_0.addWidget(
            QLabel('PyQt5 , nbtlib , qdarktheme , qdarkstyle , qtvscodestyle'), 3, 1)
        #
        layout_0.addWidget(QLabel('app Name :'), 4, 0)
        layout_0.addWidget(QLabel('Structure viewer'), 4, 1)
        #
        layout_0.addWidget(QLabel('app Author :'), 5, 0)
        layout_0.addWidget(
            QLabel('Pure.project | Xin Yuan IT | McEarth'), 5, 1)
        #
        layout_0.addWidget(QLabel('app Copyright :'), 6, 0)
        layout_0.addWidget(QLabel(
            'Copyright© 2023 Pure.project | Xin Yuan IT ,All rights reserved.'), 6, 1)
        #
        layout_0.addWidget(QLabel('app Made by :'), 7, 0)
        layout_0.addWidget(QLabel(''.join(platform._sys_version())), 7, 1)
        #
        layout_0.addWidget(QLabel('app Run in :'), 8, 0)
        layout_0.addWidget(
            QLabel(platform.system()+' '+platform.version()), 8, 1)
        #
        layout_0.addWidget(QLabel('app User :'), 9, 0)
        layout_0.addWidget(QLabel(getpass.getuser()), 9, 1)
        #
        layout_0.addWidget(QLabel('app Website :'), 10, 0)
        self.website1 = QLabel()
        self.website1.setText(
            '<a href="http://www.xinyuanit.top">xinyuanit.top</a>')
        self.website1.setOpenExternalLinks(True)
        self.website1.setTextInteractionFlags(Qt.LinksAccessibleByMouse)
        layout_0.addWidget(self.website1, 10, 1)

        self.page_1 = QWidget()
        self.page_1.setObjectName('page_x')
        # make page 1
        layout_main_1 = QVBoxLayout(self.page_1)
        layout_main_1.setContentsMargins(0, 40, 0, 0)
        layout_widget_1 = QWidget()
        layout_widget_1.setObjectName('page_0')
        layout_1 = QGridLayout(layout_widget_1)
        layout_main_1.addWidget(layout_widget_1)
        layout_main_1.addStretch(999)
        #
        label_1 = QLabel(self.page_1)
        label_1.setText('Simple')
        label_1.move(10, 10)
        label_1.setStyleSheet('font-weight:bold;font-size:17px;')

        # column,row

        self.page_2 = QWidget()
        self.page_2.setObjectName('page_x')
        # make page 1
        layout_main_2 = QVBoxLayout(self.page_2)
        layout_main_2.setContentsMargins(0, 40, 0, 0)
        #
        self.ThemeWidget = FlowWidget(self.page_2)

        label_2 = QLabel(self.page_2)
        label_2.setText('Theme')
        label_2.setStyleSheet('font-weight:bold;font-size:17px;')
        label_2.move(10, 10)

        layout_main_2.addWidget(self.ThemeWidget)
        #
        # get png file name
        self.Theme_button_group = QButtonGroup(self.ThemeWidget)
        dir_or_files = os.listdir('./img/new_theme_img/')
        pngList = []
        for dir_file in dir_or_files:
            # 获取目录或者文件的路径
            dir_file_path = os.path.join('./img/new_theme_img/', dir_file)
            if dir_file_path[-1] != '_':
                pngList.append(dir_file_path)
        # value
        self.LastTheme = 0
        self.nameList = []
        self.Qss = ['AMOLED.qss', 'Aqua.qss',
                    'ConsoleStyle.qss', 'ElegantDark.qss', 'MacOS.qss',
                    'ManjaroMix.qss', 'MaterialDark.qss', 'NeonButtons.qss', 'Ubuntu.qss', 'darkstyle.qss']
        self.VsLib = {'Light(Visual Studio)': 'LIGHT_VS',
                      'Quiet Light': 'QUIET_LIGHT',
                      'Solarized Light': 'SOLARIZED_LIGHT',
                      'Abyss': 'ABYSS',
                      'Dark(Visual Studio)': 'DARK_VS',
                      'Kimbie Dark': 'KIMBIE_DARK',
                      'Monokai': ' MONOKAI',
                      'Monokai Dimmed': 'MONOKAI_DIMMED',
                      'Red': 'RED',
                      'Solarized Dark': 'SOLARIZED_DARK',
                      'Tomorrow Night Blue': 'TOMORROW_NIGHT_BLUE',
                      'Dark High Contrast': 'DARK_HIGH_CONTRAST'}
        self.darkTheme = ['qdarktheme_dark', 'qdarktheme_light']
        self.darkStyle = ['qdarkstyle_light', 'qdarkstyle_dark']
        # function
        # (1) : changeTheme

        def changeTheme(themeIndex):
            chooseTheme = self.nameList[int(themeIndex)]
            for theme in self.VsLib:
                if self.VsLib[theme] == chooseTheme:
                    stylesheet = qtvscodestyle.load_stylesheet(
                        eval(f'qtvscodestyle.Theme.{self.VsLib[theme]}'))
                    # stylesheet = load_stylesheet(qtvscodestyle.Theme.LIGHT_VS)
                    self.mainwindow.resetStyle()
                    self.mainwindow.app.setStyleSheet(stylesheet)
                    self.mainwindow.Config_theme = chooseTheme
                    return
            for theme in self.Qss:
                if theme.split('.')[0] == chooseTheme:
                    qssStyle = StyleReader.readQSS(
                        './style/QSS-master/'+theme)
                    self.mainwindow.resetStyle()
                    self.mainwindow.setStyleSheet(qssStyle)
                    self.mainwindow.Config_theme = chooseTheme
                    return
            for theme in self.darkTheme:
                if theme == chooseTheme:
                    qdarktheme.setup_theme(
                        chooseTheme.replace('qdarktheme_', ''))
                    self.mainwindow.Config_theme = chooseTheme
                    return

            if chooseTheme == 'qdarkstyle_dark':
                self.mainwindow.app.setStyleSheet(qdarkstyle.load_stylesheet())
                self.mainwindow.Config_theme = chooseTheme
                return
            else:
                self.mainwindow.app.setStyleSheet(qdarkstyle.load_stylesheet(
                    qt_api='pyqt5', palette=LightPalette()))
                self.mainwindow.Config_theme = chooseTheme
                return

        # (2) : click_QRadioButton
        def click_QRadioButton():
            clickedButton = self.Window.sender()
            pngIndex = clickedButton.objectName()
            globals()['themeButton_'+str(self.LastTheme)
                      ].setStyleSheet('border: 2px solid rgba(0,0,0,0);border-radius:5px;')
            globals()['themeButton_'+str(pngIndex)
                      ].setStyleSheet('border: 2px solid #2cc5e4;border-radius:5px;')
            self.LastTheme = pngIndex
            # change Theme
            changeTheme(int(pngIndex))

        # (3) : click_ThemeButton
        def click_ThemeButton():
            # clear the last theme style
            globals()['themeButton_'+str(self.LastTheme)
                      ].setStyleSheet('border: 2px solid rgba(0,0,0,0);border-radius:5px;')
            # set button
            clickedButton = self.Window.sender()
            pngIndex = clickedButton.objectName()
            # set this theme style
            globals()['themeButton_'+str(pngIndex)
                      ].setStyleSheet('border: 2px solid #2cc5e4;border-radius:5px;')
            thisButton = globals()['button_'+str(pngIndex)]  # QRadioButton
            thisButton.setChecked(True)
            self.LastTheme = pngIndex
            # change Theme
            changeTheme(int(pngIndex))

        # add theme to ui
        self.thisTheme = self.mainwindow.Config_theme
        # 'qdarktheme_light'
        # self.thisTheme = 'qdarktheme_dark'

        # main code for displaying the theme name and the theme icon
        for pngIndex in range(len(pngList)):
            # card widget
            ThemeCard = QWidget()
            ThemeCard.setFixedSize(int(232*0.5) + 14, int(172*0.5) + 50)
            ThemeCard_layout = QVBoxLayout(ThemeCard)
            ThemeCard_layout.setContentsMargins(5, 7, 5, 7)
            #
            name = pngList[pngIndex].split('/')[-1].split('.')[0]
            self.nameList.append(name)
            #
            globals()['button_'+str(pngIndex)
                      ] = QRadioButton(name, self.ThemeWidget)
            this_button = globals()['button_'+str(pngIndex)]  # QRadioButton
            this_button.clicked.connect(click_QRadioButton)
            this_button.setObjectName(str(pngIndex))
            #
            self.Theme_button_group.addButton(this_button, pngIndex)
            globals()['themeButton_'+str(pngIndex)] = QPushButton()
            IconLabel = globals()['themeButton_'+str(pngIndex)]
            #
            icon = QIcon(pngList[pngIndex])
            IconLabel.setIcon(icon)
            IconLabel.setIconSize(QSize(int(232*0.5), int(172*0.5)))
            IconLabel.setFixedSize(int(232*0.5) + 4, int(172*0.5) + 4)
            IconLabel.setContentsMargins(2, 2, 2, 2)
            IconLabel.setObjectName(str(pngIndex))
            IconLabel.clicked.connect(click_ThemeButton)
            IconLabel.setStyleSheet(
                'border: 2px solid rgba(0,0,0,0);border-radius:5px;')
            # add to layout
            ThemeCard_layout.addWidget(this_button)
            ThemeCard_layout.addWidget(IconLabel)
            self.ThemeWidget.ThisLayout.addWidget(ThemeCard)
            # set checked theme:
            if name == self.thisTheme:
                this_button.setChecked(True)
                IconLabel.setStyleSheet(
                    'border: 2px solid #2cc5e4;border-radius:5px;')
                self.LastTheme = int(pngIndex)

        # layout_2.addWidget()

        self.page_3 = QWidget()
        self.page_3.setObjectName('page_x')

        self.page_4 = QWidget()
        self.page_4.setObjectName('page_x')

        self.page_5 = QWidget()
        self.page_5.setObjectName('page_x')

        self.page_6 = QWidget()
        self.page_6.setObjectName('page_x')

        self.page_7 = QWidget()
        self.page_7.setObjectName('page_x')

        self.Stacked.addWidget(self.page_0)
        self.Stacked.addWidget(self.page_1)
        self.Stacked.addWidget(self.page_2)
        self.Stacked.addWidget(self.page_3)
        self.Stacked.addWidget(self.page_4)
        self.Stacked.addWidget(self.page_5)
        self.Stacked.addWidget(self.page_6)
        self.Stacked.addWidget(self.page_7)
