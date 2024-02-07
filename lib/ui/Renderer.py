from lib.base import *


class PRendererWindow(QMainWindow):
    def __init__(self, parent=None):
        super(PRendererWindow, self).__init__(parent)
        self._parent_ = parent
        self.setWindowTitle('Structure Renderer')
        self.setWindowIcon(QIcon('img/toolbar/d_SortingGroup Icon.png'))
        self.makeTopMenu()
        self.uiInit()

    def uiInit(self):
        pass

    def makeTopMenu(self):
        self.menubar_ = self.menuBar()
        self.menubar_.setContentsMargins(0, 0, 0, 0)
        self.menubar_.setObjectName('topmenu')

        '''self.menubar_.addAction(
            QAction(QIcon('./img/icon_4.png'), '', self))'''
        ################################
        FILE = ['版本', '关闭']
        FILE_FUNC = [self.version, self.close]
        FILE_KEY = ['Ctrl+V',
                    'Ctrl+Q']
        ICON_1 = ['img/toolbar/d_BuildSettings.Standalone.png',
                  'img/toolbar/d_winbtn_mac_close_h@2x.png']
        fileMenu = self.menubar_.addMenu("文件(F)")
        for i in range(len(FILE)):
            Act = QAction(FILE[i], self)
            Act.setShortcut(FILE_KEY[i])
            Act.triggered.connect(FILE_FUNC[i])
            Act.setIcon(QIcon(ICON_1[i]))
            fileMenu.addAction(Act)
        ################################
        view = self.menubar_.addMenu("视图(V)")
        VIEW = ['窗口大小可调整', '浅色主题', '深色主题']
        HVIEW_FUNC = [self.SetWindowFixSizeUsed,
                      lambda:self.changeTheme(1), lambda:self.changeTheme(0)]
        ICON_2 = ['',
                  'img/toolbar/d_winbtn_win_max.png', 'img/toolbar/winbtn_win_max.png']
        for i in range(len(VIEW)):
            if VIEW[i] == '窗口大小可调整':
                Act = QAction(VIEW[i], self, checkable=True)
                Act.setChecked(True)
            else:
                Act = QAction(VIEW[i], self)
            Act.setIcon(QIcon(ICON_2[i]))
            Act.triggered.connect(HVIEW_FUNC[i])
            view.addAction(Act)

        ################################
        setting = self.menubar_.addMenu("设置(S)")
        SETTING = ['界面较小尺寸 (650x450)', '界面适中尺寸1 (900x600)',
                   '界面适中尺寸2 (1000x650)', '界面较大尺寸 (1100x750)',
                   '软件居中', '软件全屏 (Fullscreen)', '退出全屏']
        SETTING_FUNC = [self.resizeApp, self.resizeApp_2, self.resizeApp_2_2, self.resizeApp_3,
                        self.centralApp, self.fullScreenApp, self.outFullScreen]
        ICON_3 = ['img/toolbar/d_Settings@2x.png', 'img/toolbar/d_Profiler.UIDetails@2x.png', 'img/toolbar/d_Profiler.UIDetails@2x.png',
                  'img/toolbar/d_Profiler.UIDetails@2x.png', 'img/toolbar/d_Profiler.UIDetails@2x.png', 'img/toolbar/d_winbtn_win_restore_h@2x.png',
                  'img/toolbar/d_winbtn_win_restore_h@2x.png', 'img/toolbar/d_winbtn_win_restore_h@2x.png']
        for i in range(len(SETTING)):
            Act = QAction(SETTING[i], self)
            Act.triggered.connect(SETTING_FUNC[i])
            Act.setIcon(QIcon(ICON_3[i]))
            setting.addAction(Act)
        ################################
        help = self.menubar_.addMenu("帮助(H)")
        HELP = ['我们的网站', '帮助文档', '关于PyQt5']
        HELP_FUNC = [self.our_website,
                     self.help_document, self.Tool_about_PyQt]
        # self.Tool_about_APP, self.startPage
        ICON_4 = ['img/toolbar/d_BuildSettings.Web.Small.png', 'img/toolbar/d__Help@2x.png',
                  'img/toolbar/d__Help@2x.png',]
        for i in range(len(HELP)):
            Act = QAction(HELP[i], self)
            Act.triggered.connect(HELP_FUNC[i])
            Act.setIcon(QIcon(ICON_4[i]))
            help.addAction(Act)

    def version(self):
        reply = QMessageBox.information(
            self, "版本信息", "Pure Renderer Version : 0.0.2 beta \nTest Python Version : 3.11.2 \nStructure Viewer Version : 0.0.4 beta", QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
        print(reply)

    def Tool_about_PyQt(self):
        QApplication.aboutQt()

    def centralApp(self):
        # 获取屏幕坐标系
        screen = QDesktopWidget().screenGeometry()
        # 获取窗口坐标系
        size = self.geometry()
        newLeft = int((screen.width() - size.width()) / 2)
        newTop = int((screen.height() - size.height()) / 2)
        # move
        self.move(newLeft, newTop)

    def fullScreenApp(self):
        self.showFullScreen()

    def outFullScreen(self):
        self.showNormal()

    def resizeApp(self):
        self.resize(650, 450)
        self.resize(650, 450)

    def resizeApp_2(self):
        self.resize(900, 600)
        self.resize(900, 600)

    def resizeApp_2_2(self):
        self.resize(1000, 650)
        self.resize(1000, 650)

    def resizeApp_3(self):
        self.resize(1100, 750)
        self.resize(1100, 750)

    def SetWindowFixSizeUsed(self, state):
        if state:
            self.setMaximumSize(99999, 99999)
            self.setMinimumSize(0, 0)
        else:
            self.setMaximumSize(self.width(), self.height())
            self.setMinimumSize(self.width(), self.height())

    def our_website(self):
        os.system(f"start {self.url}")

    def help_document(self):
        os.system('start StructureStudioHelpDocument.html')

    def changeTheme(self, themeIndex):
        self._parent_.changeTheme(themeIndex)
