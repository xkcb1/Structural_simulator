from qframelesswindow import FramelessMainWindow, FramelessDialog
from PyQt5.QtCore import Qt
from lib.NbtTree import AddItemThread
from lib.Widgets.commandPalette import PureCommandPalette
from lib.Widgets.menu import PureRoundedBorderMenu
from lib.Widgets.dockWidget import Pure_QDockWidget
from lib.Widgets.newFramelessWindow import NewFramelessWindow
from lib.Widgets.startPanel import PAboutWidget, PStartWidget
from lib.base import *
from lib.base import _Thread_
from lib.core.About import AboutWidget, AboutWindow
from lib.functions.Console import Console
from lib.functions.Map import MapViewer
from lib.functions.MinecraftVersion import MinecraftVersion
from lib.functions.NbtFile import NbtFile
from lib.functions.Output import OutPutWidget
from lib.functions.PythonEditor import PythonEditor
from lib.functions.Resource import Resource
from lib.functions.Object import Object
from lib.functions.Nbt import Nbt
from lib.functions.Setting import Setting
from lib.functions.Simulator import Simulator
from lib.functions.Terminal import Terminal
from lib.functions.Viewer import Viewer
from lib.functions._Setting import _Settings
from lib.functions.White import White
from lib.core.setting import *
import sys
import cProfile
import pstats
import psutil
import os
import time
#

QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
QApplication.setHighDpiScaleFactorRoundingPolicy(
    Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)

App = QApplication(sys.argv)
window_count = 0
SELF = None
'''
From <BC project - Pure(4)>
2023.11.16
'''


class Color:
    # 颜色
    BLACK = '\033[30m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    MAGENTA = '\033[35m'
    CYAN = '\033[36m'
    WHITE = '\033[37m'
    LIGHT_GRAY = '\033[90m'  # 浅灰色
    LIGHT_RED = '\033[91m'  # 浅红色
    LIGHT_GREEN = '\033[92m'  # 浅绿色
    LIGHT_YELLOW = '\033[93m'  # 浅黄色
    LIGHT_BLUE = '\033[94m'  # 浅蓝色
    LIGHT_MAGENTA = '\033[95m'  # 浅洋红色
    LIGHT_CYAN = '\033[96m'  # 浅青色
    LIGHT_WHITE = '\033[97m'  # 浅白色
    # 字体样式
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'


class LoadMcaModel(QObject):
    '''MCA model'''
    # 定义一种信号,用来传递model文件的path
    mcaSignal = pyqtSignal(nbtlib.tag.Compound)


class LoadNbtModel(QObject):
    '''NBT model'''
    # 定义一种信号,用来传递model文件的path
    nbtSignal = pyqtSignal(nbtlib.tag.Compound)


class LoadLastNbtModel(QObject):
    '''NBT model'''
    # 定义一种信号,用来传递已有的nbt的obj模型文件的path
    LastNbtSignal = pyqtSignal(LastNBTFile)


class ChangeTheme_(QObject):
    '''NBT model'''
    # 定义一种信号,用来传递model文件的path
    changeSingal = pyqtSignal(str)


class ExpendNodes(QObject):
    '''展开节点'''
    expendSingal = pyqtSignal(QTreeWidgetItem)


class LoadObjectWindow(QObject):
    '''通过信号加载object窗口'''
    loadSingal = pyqtSignal(nbtlib.tag.Compound, str, QTreeWidget)


class MemoryThread(QThread):
    memory_update = pyqtSignal(float)

    def run(self):
        while True:
            # 获取当前系统的物理内存占用（字节为单位）
            memory_bytes = psutil.Process().memory_info().rss
            # 转换为 MB 单位
            memory_mb = memory_bytes / (1024 * 1024)
            self.memory_update.emit(memory_mb)
            time.sleep(5)  # 每隔5秒获取一次内存占用


class StructureViewer(QMainWindow):
    '''
StructureViewer Main Window

__init__():
    if appMode == 'Frameless':
        super(FramelessMainWindow, self).__init__()
    else:
        super(StructureViewer, self).__init__()
    '''

    def __init__(self, app, appMode, openPath, openFile):
        if appMode == 'Frameless':
            super(FramelessMainWindow, self).__init__()
            self.setContentsMargins(2, 0, 2, 0)
            self._isResizeEnabled = True
            from lib.Widgets.titlebar import CustomTitleBar
            self.setTitleBar(CustomTitleBar(self))
        else:
            super(StructureViewer, self).__init__()
            self.setContentsMargins(1, 0, 1, 0)
        self.appMode = appMode
        print(Color.GREEN, 'open Application in mode:', self.appMode, Color.END)
        self.app = app
        self.openPath = openPath
        self.openFile_ = openFile
        self._font_ = '微软雅黑'
        self._font_size_ = '11'
        self.themeIndex = 0
        self.UseDefaultBG = False
        self.ThisPageIndex_int = 1
        # 图标颜色修改列表
        self.changeIconList = []
        # 文件树结构信息dictionary
        self.treeViewList = {}
        self.treeViewListCount = 0
        # 终端列表
        self.Terminal_List = []
        # 结构信息dictionary
        self.objectView_list = {}
        self.objectView_listCount = 0
        # 所有vtk列表(3个)
        self.VtkWinClose = []
        self.VtkRender = []
        self.VtkIren = []
        # 3D视图vtkwidget
        self.vtkWindow = {}
        self.vtkWindowCount = 0
        self._mainVtk_ = []
        # NBT文件列表dictionary
        self.NBT_LIST_Dict = {}
        self.NBT_LIST_DictCount = 0
        # 模拟器3D视图列表
        self.Simulator_vtk = []
        # 其他文件列表
        self.file_list = []
        # 输出列表
        self.OutPutList = {}
        self.OutPutListCount = 0
        # 页面索引
        self.Page_Index = {str(i+1): [] for i in range(5)}
        # 启动页面标识
        self.startWindowClickEvent = False
        # 3D预览视图的Actor映射表
        self.Actor_Block_Dict = {}  # 加载Actor的映射表
        # 网站地址
        self.url = 'https://xkcb1.github.io/StructureViewerWebSite/'
        self.version = '0.0.1 beta'
        # 主题色和面板色
        self.ThemeColor = ''
        self.BgColor = ''
        self.BorderColor = ''
        self.ChangePanelColor = []  # 面板颜色改变列表
        # 自动设置主题列表
        self.changeTheme_list = []
        # Mac2 Mac3 Graph风格样式表
        self.macOs_2_style = '''
QDockWidget {
    titlebar-close-icon: url("./img/macButton/winbtn_mac_close_h@2x.png");
    titlebar-normal-icon: url("./img/macButton/winbtn_mac_max_h@2x.png");
}
QDockWidget::close-button {
    subcontrol-position: top right;
    subcontrol-origin: margin;
    position: absolute;
    top: 2px;
    left: 0px;
    right: 2px;
    bottom: 0px;
    width: 18px;
    height: 18px;
}
QDockWidget::float-button {
    subcontrol-position: top right;
    subcontrol-origin: margin;
    position: absolute;
    top: 2px;
    left: 16px;
    bottom: 0px;
    right: 19px;
    width: 18px;
    height: 18px;
}
        '''
        self.macOs_3_style = '''
QDockWidget {
    titlebar-close-icon: url("./img/macButton/winbtn_mac_close@2x.png");
    titlebar-normal-icon: url("./img/macButton/winbtn_mac_max@2x.png");
}
QDockWidget::close-button {
    subcontrol-position: top right;
    subcontrol-origin: margin;
    position: absolute;
    top: 2px;
    left: 0px;
    right: 2px;
    bottom: 0px;
    width: 18px;
    height: 18px;
}
QDockWidget::float-button {
    subcontrol-position: top right;
    subcontrol-origin: margin;
    position: absolute;
    top: 2px;
    left: 16px;
    bottom: 0px;
    right: 19px;
    width: 18px;
    height: 18px;
}
        '''
        self.graph_style = '''
QDockWidget {
    titlebar-close-icon: url("./img/graphButton/winbtn_graph_close_h.png");
    titlebar-normal-icon: url("./img/graphButton/winbtn_graph_max_h.png");
}
QDockWidget::close-button {
    subcontrol-position: top right;
    subcontrol-origin: margin;
    position: absolute;
    top: 2px;
    left: 0px;
    right: 4px;
    bottom: 2px;
    width: 18px;
    height: 18px;
}
QDockWidget::float-button {
    subcontrol-position: top right;
    subcontrol-origin: margin;
    position: absolute;
    top: 2px;
    left: 16px;
    bottom: 2px;
    right: 21px;
    width: 18px;
    height: 18px;
}'''
        # 窗口类型
        self.windowType = {
            '3D视图': ['img/main_3/GameEngine.png', Viewer],
            'NBT视图': ['img/main_3/Node.png', Nbt],
            '文件浏览器': ['img/main_3/Resource.png', Resource],
            '结构信息': ['img/main_3/HexEditor.png', Object],
            'Python终端': ['img/main_3/Terminal.png', Terminal],
            '信息输出': ['img/main_3/ItemList.png', OutPutWidget],
            '空白页面': ['img/main_3/White.png', White],
            '导入设置': ['img/main_3/Attribute.png', Setting],
            '模拟视图': ['img/main_3/Model.png', Simulator],
            'Minecraft版本管理': ['img/main_3/MinecraftVersion.png', MinecraftVersion],
            '编辑器': ['img/main_3/Editor.png', PythonEditor],
            '控制台': ['img/main_3/Designer.png', Console],
            'Nbt文件列表': ['img/main_3/Nbt.png', NbtFile],
            '模拟器分析视图': ['img/main_3/TerrainMaker.png', MapViewer],
            '偏好设置': ['img/main_3/settings_7.png', _Settings],
        }
        self.Window_Save_Widget = {}  # 窗口储存字典
        for _dock_window_ in self.windowType:
            self.Window_Save_Widget[_dock_window_] = []
        # 初始化储存字典
        self.base_Windows = {'3D视图': ['img/main_3/GameEngine.png', Viewer],
                             'NBT视图': ['img/main_3/Node.png', Nbt],
                             '文件浏览器': ['img/main_3/Resource.png', Resource],
                             '结构信息': ['img/main_3/HexEditor.png', Object],
                             }
        self.tool_Windows = {'Minecraft版本管理': [
            'img/main_3/MinecraftVersion.png', MinecraftVersion],
            '编辑器': ['img/main_3/Editor.png', PythonEditor], }
        self.debug_Windows = {'Python终端': ['img/main_3/Terminal.png', Terminal],
                              '信息输出': ['img/main_3/ItemList.png', OutPutWidget],
                              '空白页面': ['img/main_3/White.png', White],
                              '控制台': ['img/main_3/Designer.png', Console],
                              '偏好设置': ['img/main_3/settings_7.png', _Settings],
                              }
        self.simulator_Windows = {
            '导入设置': ['img/main_3/Attribute.png', Setting],
            '模拟视图': ['img/main_3/Model.png', Simulator],
            'Nbt文件列表': ['img/main_3/Nbt.png', NbtFile],
            '模拟器分析视图': ['img/main_3/TerrainMaker.png', MapViewer],
        }
        # Name : [icon,widget]
        # signal
        self.lastNBT = LoadLastNbtModel()
        self.lastNBT.LastNbtSignal.connect(self.loadNbtModelFunction)
        # singal 2
        self.expendFunc = ExpendNodes()
        self.expendFunc.expendSingal.connect(self.expend_singal)
        # singal 3
        self.objectLoader = LoadObjectWindow()
        self.objectLoader.loadSingal.connect(self.LoadObjectInOneWindow)
        # set title
        self.setWindowTitle('Structure Studio')
        self.setWindowIcon(QIcon('img/earth_30_24.png'))
        '''
        some attitudes and setting or use mica style (windows)
        '''
        self.origPalette = QApplication.palette()
        # load configuration
        self.thisTheme = 'default'
        self.loadConfig()
        self.setWindowStyle_mica()
        palette = QPalette()
        palette.setColor(QPalette.Window, QColor(51, 52, 53))
        self.setStyleSheet('''
QMainWindow {
    background-color:rgb(51, 52, 53);
    background-image:url(img/mcEarth_black_40_300px.png);
    background-position:center center;
    background-repeat:no-repeat;
}
                           ''')
        self.setPalette(palette)
        self.show()
        self.app.processEvents()
        self.makeTopMenu()
        self.makeTabMenu()
        # 加载窗口
        self.makeDockWindow()
        # page 1
        self.resizeDocks([self.Resource_window, self.Viewer_window], [
                         1, 3], Qt.Horizontal)
        # page 2
        self.resizeDocks([self.Setting_window, self.Simulator_window], [
                         1, 3], Qt.Horizontal)
        # page 4
        # page 2
        self.resizeDocks([self.Terminal_window, self.Editor_window], [
                         1, 3], Qt.Horizontal)
        self.makeStatus()
        # 安装事件过滤器
        self.start_w = 520
        self.start_h = 470
        qApp.installEventFilter(self)
        self.changeTheme(self.themeIndex)
        # 进入测试页面
        for i in range(5):
            for hide_Window in self.Page_Index[str(i+1)]:
                hide_Window.hide()
        # 全部隐藏
        self.MenuTabWidget.setCurrentIndex(self.ThisPageIndex_int - 1)
        self.ClickMenuTab()

    def showStartWindow(self):
        # 创建一个菜单
        self.startWindow = PStartWidget(self, self.start_w, self.start_h)
        # 将对话框移动到主窗口的中央
        main_window_rect = self.geometry()
        self.startWindow.move(main_window_rect.center() -
                              self.startWindow.rect().center())
        self.startWindow.show()

    def moveEvent(self, event):
        # 主窗口移动时更新对话框位置
        try:
            if self.startWindowClickEvent == False:
                try:
                    main_window_rect = self.geometry()
                    self.startWindow.move(main_window_rect.center() -
                                          self.startWindow.rect().center())
                except:
                    pass
        except:
            pass

    def resizeEvent(self, event):
        try:
            # 主窗口移动时更新对话框位置
            if self.startWindowClickEvent == False:
                try:
                    main_window_rect = self.geometry()
                    self.startWindow.move(main_window_rect.center() -
                                          self.startWindow.rect().center())
                except:
                    pass
            if self.appMode == 'Frameless':
                self.spaceWidget.setFixedSize(
                    self.width() - 550 - self.titleBar.minBtn.width()*3, 29)

        except:
            pass

    def eventFilter(self, obj, event):
        try:
            if event.type() == QEvent.MouseButtonPress and self.startWindowClickEvent == False:
                global_pos = event.globalPos()
                local_pos = self.mapFromGlobal(global_pos)
                if QRegion(int((self.width() - self.start_w) /
                               2), int((self.height() - self.start_h)/2),
                           self.start_w, self.start_h).contains(local_pos):
                    # 如果点击在区域内，则不处理
                    pass
                else:
                    # 如果在区域外，则修改标识，并且隐藏启动界面
                    self.startWindowClickEvent = True
                    self.startWindow.hide()
                    print('close start window')
            if self.appMode == 'Frameless':

                return super(FramelessMainWindow, self).eventFilter(obj, event)
            else:
                return super(StructureViewer, self).eventFilter(obj, event)
        except:
            if self.appMode == 'Frameless':

                return super(FramelessMainWindow, self).eventFilter(obj, event)
            else:
                return super(StructureViewer, self).eventFilter(obj, event)

    def PostValueToTerminal(self):
        global_vars = globals()
        for terminal in self.Terminal_List:
            ipython_instance = terminal[0].kernel_manager.kernel.shell
            # 将变量添加到 IPython 的用户命名空间中
            for var_name, var_value in global_vars.items():
                ipython_instance.user_ns[var_name] = var_value

    def loadNbtModelFunction(self, nbtData):
        for vtkWidget in self.vtkWindow:
            try:
                self.vtkWindow[vtkWidget].loadNbtModelFunction(nbtData)
            except:
                pass

    def loadConfig(self):
        try:
            with open('SS_config.ini', 'r', encoding='utf-8') as config:
                self.config = eval(config.read())
            self.resize(self.config['w'], self.config['h'])
            self.move(self.config['x'], self.config['y'])
            # self.changeTheme(self.config['ThemeIndex'])
            if self.config['ThemeIndex'] == 0:
                # dark
                self.Puretheme = 'dark'
                self.ThemeColor = '#4772B3'
                self.BgColor = '#202020'
                self.BorderColor = '#4a4a4a'
            elif self.config['ThemeIndex'] == 1:
                # light
                self.Puretheme = 'light'
                self.ThemeColor = '#5F85C1'
                self.BgColor = '#ddd'
                self.BorderColor = '#777'
            else:
                # gray
                self.Puretheme = 'gray'
                self.ThemeColor = '#C85130'
                self.BgColor = '#333'
                self.BorderColor = '#4a4a4a'

            self.themeIndex = self.config['ThemeIndex']
            if self.config['windowStyle'] == 0:
                # 0
                self.DockStyle = 'Window'
            else:
                # 1
                self.DockStyle = 'MacOs_2'
        except:
            self.config = {}
            QMessageBox.warning(None, "Warning - config",
                                traceback.format_exc())

        try:
            with open('recent.ini', 'r', encoding='utf-8') as recent:
                self.recent = recent.readlines()
        except:
            self.recent = []

    def closeEvent(self, event):
        self.memory_thread.exit()
        self.config['w'] = self.width()
        self.config['h'] = self.height()
        self.config['x'] = self.x()
        self.config['y'] = self.y()
        self.config['ThemeIndex'] = self.themeIndex
        # self.config['theme'] = self.Config_theme
        if self.DockStyle == 'Window':
            # Window
            self.config['windowStyle'] = 0
        else:
            # MacOs
            self.config['windowStyle'] = 1

        with open('SS_config.ini', 'w') as config_write:
            config_write.write(str(self.config))
        # 关闭渲染窗口,否则会vtk报错 <- Important
        for vtkWidget in self.VtkWinClose:
            vtkWidget.Finalize()

    def SystemThemeChange(self, argv=''):
        pass

    def setWindowStyle_mica(self):
        if self.appMode == 'native':
            if platform.system() == 'Windows':
                try:
                    # self.setAttribute(QtCore.Qt.WA_TranslucentBackground, True)
                    hwnd = self.winId().__int__()
                    mode = MicaTheme.DARK
                    style = MicaStyle.DEFAULT
                    win32mica.ApplyMica(HWND=hwnd, Theme=mode, Style=style,
                                        OnThemeChange=self.SystemThemeChange)
                    self.app.processEvents()
                except:
                    print(f'cannot use Mica Style in {self.winId()}')
            else:
                print(Color.YELLOW,
                      f'System : {platform.system()} cannot use Mica Style in {self.winId()}', Color.END)
        else:
            print(
                Color.YELLOW, f'[system] : {platform.system()} Use appMode : {self.appMode}', Color.END)

    def makeDockWindow(self):
        self.setDockOptions(self.dockOptions() | QMainWindow.AllowTabbedDocks)
        self.setDockNestingEnabled(True)
        '''
        Page 1
        '''
        # 3D视图
        self.Viewer_window = Pure_QDockWidget(self, Wtype='3D视图', page=1)
        self.Viewer_window.setObjectName('3D视图')
        self.Page_Index['1'].append(self.Viewer_window)
        self.Viewer_window.page = 1
        # NBT视图
        self.NBT_window = Pure_QDockWidget(self, Wtype='NBT视图', page=1)
        self.NBT_window.setObjectName('NBT视图')
        self.Page_Index['1'].append(self.NBT_window)
        self.NBT_window.page = 1
        # 文件浏览器
        self.Resource_window = Pure_QDockWidget(self, Wtype='文件浏览器', page=1)
        self.Resource_window.setObjectName('文件浏览器')
        self.Page_Index['1'].append(self.Resource_window)
        self.Resource_window.page = 1
        # 结构信息
        self.Object_window = Pure_QDockWidget(self, Wtype='结构信息', page=1)
        self.Object_window.setObjectName('结构信息')
        self.Page_Index['1'].append(self.Object_window)
        self.Object_window.page = 1

        '''
        Page 2
        '''
        # 导入设置
        self.Setting_window = Pure_QDockWidget(self, Wtype='导入设置', page=2)
        self.Setting_window.setObjectName('导入设置')
        self.Page_Index['2'].append(self.Setting_window)
        self.Setting_window.page = 2
        # 模拟视图
        self.Simulator_window = Pure_QDockWidget(self, Wtype='模拟视图', page=2)
        self.Simulator_window.setObjectName('模拟视图')
        self.Page_Index['2'].append(self.Simulator_window)
        self.Simulator_window.page = 2
        # Nbt文件列表
        self.NbtFile_window = Pure_QDockWidget(self, Wtype='Nbt文件列表', page=2)
        self.NbtFile_window.setObjectName('Nbt文件列表')
        self.Page_Index['2'].append(self.NbtFile_window)
        self.NbtFile_window.page = 2
        # 模拟器分析视图
        self.MapViewrt_window = Pure_QDockWidget(self, Wtype='模拟器分析视图', page=2)
        self.MapViewrt_window.setObjectName('模拟器分析视图')
        self.Page_Index['2'].append(self.MapViewrt_window)
        self.MapViewrt_window.page = 2
        '''
        Page 3
        '''
        '''# 我的世界版本管理
        self.MinecraftVersion_window = Pure_QDockWidget(
            self, Wtype='Minecraft版本管理', page=3)
        self.MinecraftVersion_window.setObjectName('Minecraft版本管理')
        self.Page_Index['3'].append(self.MinecraftVersion_window)
        self.MinecraftVersion_window.page = 3'''
        # 信息输出
        self.Output_window = Pure_QDockWidget(self, Wtype='信息输出', page=3)
        self.Output_window.setObjectName('信息输出')
        self.Page_Index['3'].append(self.Output_window)
        self.Output_window.page = 3
        '''
        Page 4
        '''
        # Python终端
        self.Terminal_window = Pure_QDockWidget(
            self, Wtype='Python终端', page=4)
        self.Terminal_window.setObjectName('Python终端')
        self.Page_Index['4'].append(self.Terminal_window)
        self.Terminal_window.page = 4
        # 编辑器
        self.Editor_window = Pure_QDockWidget(self, Wtype='编辑器', page=4)
        self.Editor_window.setObjectName('编辑器')
        self.Page_Index['4'].append(self.Editor_window)
        self.Editor_window.page = 4
        # 控制台
        self.Console_window = Pure_QDockWidget(self, Wtype='控制台', page=4)
        self.Console_window.setObjectName('控制台')
        self.Page_Index['4'].append(self.Console_window)
        self.Console_window.page = 4
        '''
        Page 1 布局
        '''
        self.addDockWidget(Qt.RightDockWidgetArea, self.Resource_window)
        self.splitDockWidget(self.Resource_window,
                             self.Viewer_window, Qt.Horizontal)
        self.splitDockWidget(self.Resource_window,
                             self.NBT_window, Qt.Vertical)
        self.splitDockWidget(self.NBT_window,
                             self.Object_window, Qt.Vertical)

        '''
        Page 2 布局
        '''
        self.addDockWidget(Qt.RightDockWidgetArea, self.Setting_window)
        self.splitDockWidget(self.Setting_window,
                             self.Simulator_window, Qt.Horizontal)
        self.splitDockWidget(self.Setting_window,
                             self.NbtFile_window, Qt.Vertical)
        self.splitDockWidget(self.Simulator_window,
                             self.MapViewrt_window, Qt.Horizontal)

        '''
        Page 3 布局
        '''
        self.addDockWidget(Qt.RightDockWidgetArea,
                           self.Output_window)
        '''
        Page 4 布局
        '''
        self.addDockWidget(Qt.RightDockWidgetArea, self.Terminal_window)
        self.splitDockWidget(self.Terminal_window,
                             self.Editor_window, Qt.Horizontal)
        self.splitDockWidget(self.Terminal_window,
                             self.Console_window, Qt.Vertical)

    def PopupStartPage(self):
        self.start_w = 520
        self.start_h = 470
        self.startWindowClickEvent = False  # 回复标识
        self.showStartWindow()

    def USE_WINDOW_STYLE(self):
        # 新增一个属性，标识浮动窗口的标题栏样式
        self.DockStyle = 'Window'
        self.changeTheme(self.themeIndex)

    def USE_MACOS_STYLE(self):
        # 新增一个属性，标识浮动窗口的标题栏样式
        self.DockStyle = 'MacOs'
        self.changeTheme(self.themeIndex)

    def USE_MACOS_STYLE_2(self):
        # 新增一个属性，标识浮动窗口的标题栏样式
        self.DockStyle = 'MacOs_2'
        self.changeTheme(self.themeIndex)

    def USE_MACOS_STYLE_3(self):
        # 新增一个属性，标识浮动窗口的标题栏样式
        self.DockStyle = 'MacOs_3'
        self.changeTheme(self.themeIndex)

    def USE_GRAPH_STYLE(self):
        # 新增一个属性，标识浮动窗口的标题栏样式
        self.DockStyle = 'Graph'
        self.changeTheme(self.themeIndex)

    def TopCommandPalette_init_(self, layout):
        '''
        显示顶部命令面板
        '''
        self.CommandPalette = PureCommandPalette(self)
        layout.addWidget(self.CommandPalette)

    def makeTabMenu(self):
        '''
        顶部菜单栏tabWidget
        '''
        if self.appMode == 'native':
            self.tabLayout = QHBoxLayout(self.menubar_)
            self.menubar_.move(20, 20)
            self.tabLayout.setContentsMargins(325, 0, 0, 0)
            self.ThisPage = 0
            #
            self.MenuTabWidget = QTabWidget()
            self.MenuTabWidget.setFixedWidth(250)
            self.MenuTabWidget.setMovable(True)
            self.MenuTabWidget.setContentsMargins(0, 0, 0, 0)
            self.tabLayout.addWidget(self.MenuTabWidget)
            #
            self.spaceWidget = QWidget()
            self.spaceWidget.setObjectName('spaceWidget')
            self.tabLayout.addWidget(self.spaceWidget)

            self.spaceWidget_layout = QHBoxLayout(self.spaceWidget)
            self.spaceWidget_layout.setContentsMargins(10, 1, 10, 1)
            # 加载顶部命令面板
            self.spaceWidget_layout.addStretch(1)
            self.TopCommandPalette_init_(self.spaceWidget_layout)
            self.spaceWidget_layout.addStretch(2)
            #
            self.MenuTabWidget.setFixedHeight(24)
        else:
            # self.appMode == 'Frameless'
            self.tabWidget = QWidget(self.titleBar)
            self.tabWidget.setFixedWidth(250)
            self.tabWidget.setFixedHeight(29)
            self.tabWidget.move(300, 0)
            self.tabWidget.show()
            self.tabLayout = QHBoxLayout(self.tabWidget)
            self.tabLayout.setContentsMargins(0, 3, 0, 0)
            self.ThisPage = 0
            #
            self.MenuTabWidget = QTabWidget()
            self.MenuTabWidget.setMovable(True)
            self.MenuTabWidget.setContentsMargins(0, 0, 0, 0)
            self.tabLayout.addWidget(self.MenuTabWidget)
            #
            self.spaceWidget = QWidget(self.titleBar)
            self.spaceWidget.setObjectName('spaceWidget')
            self.spaceWidget.move(300+250, 0)
            self.spaceWidget.setFixedSize(
                self.width() - 550 - self.titleBar.minBtn.width()*3, 29)
            self.spaceWidget_layout = QHBoxLayout(self.spaceWidget)
            self.spaceWidget_layout.setContentsMargins(10, 5, 10, 2)
            # 加载顶部命令面板
            self.spaceWidget_layout.addStretch(1)
            self.TopCommandPalette_init_(self.spaceWidget_layout)
            self.spaceWidget_layout.addStretch(2)
            self.spaceWidget.show()
            #
            self.MenuTabWidget.setFixedHeight(26)
            self.titleBar.layout().setContentsMargins(0, 0, 0, 2)
            # 间隔控件

            self.titleBar.layout().insertStretch(0, 999)

        # add tab 1
        self.MenuTabWidget.addTab(QWidget(), QIcon(), '视图')
        self.MenuTabWidget.setTabToolTip(
            0, '预设窗口类型选项卡 : 视图\nPreset Window Type Tab: View')
        # add tab 2
        self.MenuTabWidget.addTab(QWidget(), QIcon(), '模拟器')
        self.MenuTabWidget.setTabToolTip(
            1, '预设窗口类型选项卡 : 模拟器\nPreset Window Type Tab: Simulator')
        # add tab 3
        self.MenuTabWidget.addTab(QWidget(), QIcon(), '工具')
        self.MenuTabWidget.setTabToolTip(
            2, '预设窗口类型选项卡 : 工具\nPreset Window Type Tab: Tools')
        # add tab 4
        self.MenuTabWidget.addTab(QWidget(), QIcon(), '调试')  # 终端
        self.MenuTabWidget.setTabToolTip(
            3, '预设窗口类型选项卡 : 调试\nPreset Window Type Tab: Debug')
        # add tab +
        self.MenuTabWidget.addTab(QWidget(), QIcon(), ' + ')
        self.MenuTabWidget.setTabToolTip(
            4, '新建窗口选项卡\nNew window tab')
        self.MenuTabWidget.installEventFilter(ToolTipFilter(
            self.MenuTabWidget, 300, ToolTipPosition.BOTTOM))
        # connect
        self.MenuTabWidget.currentChanged.connect(self.ClickMenuTab)

    def ClickMenuTab(self):
        '''
        在主页面上切换选项卡
        只在切换选项卡的时候检测现在页面上所有的窗口
        '''
        last_index = self.ThisPageIndex_int
        getIndex = self.MenuTabWidget.currentIndex() + 1
        self.ThisPageIndex_int = getIndex

        # 获取现在的所有存在的窗口
        if self.startWindowClickEvent:
            dock_widgets = self.findChildren(QDockWidget)
            for dock_widget in dock_widgets:
                if dock_widget.isVisible() == False:
                    # 如果这个窗口不可见
                    try:
                        # 尝试删除
                        self.Page_Index[str(last_index)].remove(dock_widget)
                    except:
                        pass
                else:
                    # 如果有现在还可见的窗口
                    if dock_widget not in self.Page_Index[str(last_index)]:
                        self.Page_Index[str(last_index)].append(dock_widget)

        print('change page :', getIndex)
        # 隐藏
        for hide_Window in self.Page_Index[str(last_index)]:
            hide_Window.hide()
        # 显示
        for show_Window in self.Page_Index[str(getIndex)]:
            show_Window.show()

    def makeTopMenu(self):  # 菜单栏部分
        if self.appMode == 'Frameless':
            self.menubar_ = QMenuBar(self.titleBar)
            self.menubar_.move(0, 0)
            self.menubar_.setFixedSize(302, 31
                                       )
            self.menubar_.setStyleSheet('padding-top:5px;')
            self.menubar_.show()
            self.setMenuWidget(self.titleBar)

        else:
            self.menubar_ = self.menuBar()
            self.menubar_.setFixedHeight(28)
            self.menubar_.setContentsMargins(0, 0, 0, 0)
        # start menu bar
        if self.appMode == 'native':
            pass
        else:
            firstAction = QAction(
                QIcon(f'img/appIcon_1.png'), '', self)

            firstAction.setToolTip('Structure Studio 0.0.1')
            firstAction.installEventFilter(ToolTipFilter(
                firstAction, 300, ToolTipPosition.BOTTOM))
            self.changeIconList.append(firstAction)
            self.menubar_.addAction(firstAction)
            APP_menu = PureRoundedBorderMenu(self.menubar_)
            APP_menu.setFixedWidth(200)
            startPage = QAction('开始页面', self)
            startPage.triggered.connect(self.PopupStartPage)
            #
            APP_menu.addAction(startPage)
            aboutPage = QAction('关于 Structure Studio', self)
            aboutPage.triggered.connect(self.AboutPage)
            APP_menu.addAction(aboutPage)
            APP_menu.addSeparator()
            SysPage = QAction('系统设置', self)
            SysPage.setIcon(
                QIcon(f'img/appIcon/{self.Puretheme}/preferences.svg'))
            SysPage.iconPath = 'preferences.svg'
            self.changeIconList.append(SysPage)
            APP_menu.addAction(SysPage)
            firstAction.setMenu(APP_menu)

        ################################
        FILE = ['新建',  '打开', '近期文件', '资源管理器', '自动保存', None, '关闭']
        FILE_FUNC = [self.openFile, print, print,
                     print, print, print, self.close]
        FILE_KEY = ['Ctrl+N', 'Ctrl+O', 'Ctrl+Shift+R', '', '', '', 'Ctrl+Q']
        ICON_1 = [f'img/appIcon/{self.Puretheme}/file.svg',
                  f'img/appIcon/{self.Puretheme}/file_folder.svg',
                  f'img/appIcon/{self.Puretheme}/file_folder.svg',
                  f'img/appIcon/{self.Puretheme}/asset_manager.svg',
                  f'img/appIcon/{self.Puretheme}/file_hidden.svg',
                  '',
                  f'img/appIcon/{self.Puretheme}/quit.svg']
        fileMenu = PureRoundedBorderMenu('文件(&F)', self.menubar_)

        if self.appMode == 'native':
            startPage = QAction('开始页面', self)
            startPage.triggered.connect(self.PopupStartPage)
            #
            fileMenu.addAction(startPage)
            aboutPage = QAction('关于 Structure Studio', self)
            aboutPage.triggered.connect(self.AboutPage)
            fileMenu.addAction(aboutPage)
            SysPage = QAction('系统设置', self)
            SysPage.setIcon(
                QIcon(f'img/appIcon/{self.Puretheme}/preferences.svg'))
            SysPage.iconPath = 'preferences.svg'
            self.changeIconList.append(SysPage)
            fileMenu.addAction(SysPage)
            fileMenu.addSeparator()

        for i in range(len(FILE)):
            if FILE[i] == None:
                fileMenu.addSeparator()
            else:
                Act = QAction(FILE[i], self)
                Act.setShortcut(FILE_KEY[i])
                Act.triggered.connect(FILE_FUNC[i])
                Act.setIcon(QIcon(ICON_1[i]))
                Act.iconPath = ICON_1[i].split('/')[-1]
                self.changeIconList.append(Act)
                fileMenu.addAction(Act)
        fileMenu.setFixedWidth(250)
        self.menubar_.addMenu(fileMenu)

        ################################
        view = PureRoundedBorderMenu('视图(&V)', self.menubar_)
        view.setFixedWidth(250)
        VIEW = ['窗口大小可调整', None,
                '亮色主题', '深灰色主题', '暗色主题']
        HVIEW_FUNC = [self.SetWindowFixSizeUsed, None,
                      lambda:self.changeTheme(1), lambda:self.changeTheme(2), lambda:self.changeTheme(0)]
        ICON_2 = ['', None,
                  'img/toolbar/d_winbtn_win_max.png',
                  'img/toolbar/gray_win.png',
                  'img/toolbar/winbtn_win_max.png']
        for i in range(len(VIEW)):
            if VIEW[i] == None:
                view.addSeparator()
            else:
                if VIEW[i] == '窗口大小可调整':
                    Act = QAction(VIEW[i], self, checkable=True)
                    Act.setChecked(True)
                else:
                    Act = QAction(VIEW[i], self)
                Act.setIcon(QIcon(ICON_2[i]))
                Act.triggered.connect(HVIEW_FUNC[i])
                view.addAction(Act)
        # 使用mac或者window风格的dockwidget
        view.addSeparator()
        # Window风格
        Window_Style_Check = QAction(QIcon(
            f'img/appIcon/{self.Puretheme}/sys_Window.svg'), 'Window 风格 (浮动窗口)', self)
        Window_Style_Check.iconPath = 'sys_Window.svg'
        self.changeIconList.append(Window_Style_Check)
        Window_Style_Check.triggered.connect(self.USE_WINDOW_STYLE)
        view.addAction(Window_Style_Check)

        # Mac风格
        Mac_Style_Check = QAction(QIcon(
            f'img/appIcon/{self.Puretheme}/apple-fill.svg'), 'MacOs 风格 1 (浮动窗口)', self)
        Mac_Style_Check.iconPath = 'apple-fill.svg'
        self.changeIconList.append(Mac_Style_Check)
        Mac_Style_Check.triggered.connect(self.USE_MACOS_STYLE)
        view.addAction(Mac_Style_Check)

        # Mac风格2
        Mac_Style_Check_2 = QAction(QIcon(
            f'img/appIcon/{self.Puretheme}/apple-fill.svg'), 'MacOs 风格 2 (浮动窗口)', self)
        Mac_Style_Check_2.iconPath = 'apple-fill.svg'
        self.changeIconList.append(Mac_Style_Check_2)
        Mac_Style_Check_2.triggered.connect(self.USE_MACOS_STYLE_2)
        view.addAction(Mac_Style_Check_2)

        # Mac风格3
        Mac_Style_Check_3 = QAction(QIcon(
            f'img/appIcon/{self.Puretheme}/apple-fill.svg'), 'MacOs 风格 3 (浮动窗口)', self)
        Mac_Style_Check_3.iconPath = 'apple-fill.svg'
        self.changeIconList.append(Mac_Style_Check_3)
        Mac_Style_Check_3.triggered.connect(self.USE_MACOS_STYLE_3)
        view.addAction(Mac_Style_Check_3)

        # Graph 风格
        Graph_Style_Check = QAction(QIcon(
            f'img/appIcon/{self.Puretheme}/radio-button-line.svg'), 'Graph 风格 (浮动窗口)', self)
        Graph_Style_Check.iconPath = 'radio-button-line.svg'
        self.changeIconList.append(Graph_Style_Check)
        Graph_Style_Check.triggered.connect(self.USE_GRAPH_STYLE)
        view.addAction(Graph_Style_Check)
        # End style view
        self.menubar_.addMenu(view)

        ################################
        tools = PureRoundedBorderMenu('工具(&T)', self.menubar_)
        tools.setFixedWidth(250)
        TOOL = ['渲染窗口', '方块列表',
                '查看源代码 (python)', 'bat脚本', 'Mineways (./scripts)']
        HVIEW_FUNC = [print, print,
                      print, print, self.openMineWays]
        ICON_tool = [f'img/appIcon/{self.Puretheme}/camera_data.svg',
                     f'img/appIcon/{self.Puretheme}/cube.svg',
                     f'img/appIcon/{self.Puretheme}/text.svg',
                     f'img/appIcon/{self.Puretheme}/text.svg',
                     f'img/appIcon/{self.Puretheme}/experimental.svg',]
        for i in range(len(TOOL)):
            Act = QAction(TOOL[i], self)
            Act.setIcon(QIcon(ICON_tool[i]))
            Act.iconPath = ICON_tool[i].split('/')[-1]
            self.changeIconList.append(Act)
            Act.triggered.connect(HVIEW_FUNC[i])
            tools.addAction(Act)
        tools.addSeparator()
        more_tools = PureRoundedBorderMenu('Plugins (./SV_plugins)', tools)
        more_tools.setIcon(QIcon(f'img/appIcon/{self.Puretheme}/text.svg'))
        more_tools.iconPath = 'text.svg'
        self.changeIconList.append(more_tools)
        tools.addMenu(more_tools)
        for root, dirs, files in os.walk('./SV_plugins'):
            plugins = files
        for pluginFile in plugins:
            iconpath = f'img/appIcon/{self.Puretheme}/file.svg'
            if pluginFile.split('.')[-1] == 'py':
                iconpath = f'img/appIcon/{self.Puretheme}/file_script.svg'
            plugIcon = QIcon(iconpath)
            globals()[pluginFile+'_menu'] = QAction(
                plugIcon, pluginFile, self)
            globals()[pluginFile+'_menu'].iconPath = iconpath.split('/')[-1]
            self.changeIconList.append(globals()[pluginFile+'_menu'])
            more_tools.addAction(globals()[pluginFile+'_menu'])
        self.menubar_.addMenu(tools)

        ################################
        setting = PureRoundedBorderMenu('设置(&S)', self.menubar_)
        setting.setFixedWidth(250)
        SETTING = ['偏好设置 (Preference)', None, '界面较小尺寸 (700x450)', '界面适中尺寸1 (950x600)',
                   '界面适中尺寸2 (1000x650)', '界面较大尺寸 (1100x750)', None,
                   '软件居中', '软件全屏', '退出全屏']
        SETTING_FUNC = [self.setting, None, self.resizeApp, self.resizeApp_2, self.resizeApp_2_2, self.resizeApp_3, None,
                        self.centralApp, self.fullScreenApp, self.outFullScreen]
        ICON_3 = [f'img/appIcon/{self.Puretheme}/preferences.svg',
                  None,
                  f'img/appIcon/{self.Puretheme}/window.svg',
                  f'img/appIcon/{self.Puretheme}/window.svg',
                  f'img/appIcon/{self.Puretheme}/window.svg',
                  f'img/appIcon/{self.Puretheme}/window.svg',
                  None,
                  f'img/appIcon/{self.Puretheme}/snap_face_center.svg',
                  f'img/appIcon/{self.Puretheme}/fullscreen_enter.svg',
                  f'img/appIcon/{self.Puretheme}/fullscreen_exit.svg',]
        for i in range(len(SETTING)):
            if SETTING[i] == None:
                setting.addSeparator()
            else:
                Act = QAction(SETTING[i], self)
                Act.triggered.connect(SETTING_FUNC[i])
                Act.setIcon(QIcon(ICON_3[i]))
                Act.iconPath = ICON_3[i].split('/')[-1]
                self.changeIconList.append(Act)
                setting.addAction(Act)
        self.menubar_.addMenu(setting)

        ################################
        help = PureRoundedBorderMenu('帮助(&H)', self.menubar_)
        help.setFixedWidth(250)
        HELP = ['我们的网站', '帮助文档', '关于PyQt5',  '关于我们(About us)', '版本',]
        HELP_FUNC = [self.our_website,
                     self.help_document, self.Tool_about_PyQt, self.Tool_about_APP, print]
        # self.Tool_about_APP, self.startPage
        ICON_4 = [f'img/appIcon/{self.Puretheme}/url.svg',
                  f'img/appIcon/{self.Puretheme}/url.svg',
                  f'img/appIcon/{self.Puretheme}/Qt_logo_neon_2022.svg.png',
                  f'img/appIcon/{self.Puretheme}/window.svg',
                  f'img/appIcon/{self.Puretheme}/restrict_view_off.svg',]
        for i in range(len(HELP)):
            Act = QAction(HELP[i], self)
            Act.triggered.connect(HELP_FUNC[i])
            Act.setIcon(QIcon(ICON_4[i]))
            Act.iconPath = ICON_4[i].split('/')[-1]
            self.changeIconList.append(Act)
            help.addAction(Act)
        self.menubar_.addMenu(help)

        # license
        license = PureRoundedBorderMenu('查看开源许可证 (License)', help)
        license.setIcon(
            QIcon(f'img/appIcon/{self.Puretheme}/file.svg'))
        license.iconPath = 'file.svg'
        self.changeIconList.append(license)
        help.addMenu(license)
        for root, dirs, files in os.walk('./license'):
            get_license = files
        for license_file in get_license:
            globals()[license_file+'_menu'] = QAction(
                license_file, self)
            print('[+] : license files :', license_file)
            this_open_function = f'''
def {(license_file.split('-')[0]+'_license').replace(' ','_').replace(']','_').replace('[','_')} ():
    this_str = ''
    with open('./license/{license_file}', 'r', encoding='utf-8') as license:
        this_str = license.read()
    globals()['license_WINDOW_'+str(globals()['window_count'])] = QMainWindow()
    license_WINDOW = globals()['license_WINDOW_'+ \
                             str(globals()['window_count'])]
    license_WINDOW.resize(400, 504)
    license_WINDOW.setWindowTitle('{license_file}')
    license_WINDOW.setStyleSheet('font-family: auto;')
    this_text_viewer = QTextBrowser()
    this_text_viewer.setText(this_str)
    this_text_viewer.setReadOnly(True)
    #
    screen = QDesktopWidget().screenGeometry()
    size = license_WINDOW.geometry()
    newLeft = int((screen.width() - size.width()) / 2)
    newTop = int((screen.height() - size.height()) / 2)
    license_WINDOW.move(newLeft, newTop)
    #
    license_WINDOW.setCentralWidget(this_text_viewer)
    #
    globals()['window_count'] += 1
    #
    license_WINDOW.show()
'''
            exec(this_open_function)
            globals()[(license_file.split('-')[0]+'_license').replace(' ', '_').replace(']', '_').replace('[', '_')
                      ] = locals()[(license_file.split('-')[0]+'_license').replace(' ', '_').replace(']', '_').replace('[', '_')]
            globals()[license_file +
                      '_menu'].triggered.connect(globals()[(license_file.split('-')[0]+'_license').replace(' ', '_').replace(']', '_').replace('[', '_')])
            globals()[license_file +
                      '_menu'].setIcon(QIcon(f'img/appIcon/{self.Puretheme}/file.svg'))
            globals()[license_file +
                      '_menu'].iconPath = 'file.svg'
            self.changeIconList.append(globals()[license_file +
                                                 '_menu'])
            license.addAction(globals()[license_file+'_menu'])

    def AboutPage(self):
        self.startWindowClickEvent = False  # 回复标识
        # 创建一个菜单
        self.start_w = 600
        self.start_h = 300
        self.startWindow = PAboutWidget(self, 680, 340)
        # 将对话框移动到主窗口的中央
        main_window_rect = self.geometry()
        self.startWindow.move(main_window_rect.center() -
                              self.startWindow.rect().center())
        self.startWindow.show()

    def openMineWays(self):
        os.system('start ./scripts/mineways_min/Mineways.exe')

    def openFile(self):
        try:
            fileName2, ok2 = QFileDialog.getOpenFileName(
                self, "文件另存", "C:/", "All Files (*)")
            self.AssetWidgetOpenFile(fileName2)
        except:
            pass

    def Tool_about_PyQt(self):
        QApplication.aboutQt()

    def Tool_about_APP(self):
        pass

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
        self.resize(700, 450)
        self.resize(700, 450)

    def resizeApp_2(self):
        self.resize(950, 600)
        self.resize(950, 600)

    def resizeApp_2_2(self):
        self.resize(1000, 650)
        self.resize(1000, 650)

    def resizeApp_3(self):
        self.resize(1100, 750)
        self.resize(1100, 750)

    def setting(self):
        # 导入设置
        preferences_window = NewFramelessWindow(self)
        preferences_window.setWindowTitle('偏好设置')
        preferences_window.setWindowIcon(
            QIcon('img/appIcon/dark/preferences.svg'))
        setting_widget = _Settings(self, self, self.openPath)
        setting_widget._mainwidget_.setStyleSheet(
            '#MainWidget {border-radius:0px !important;}')
        preferences_window.MainLayout.addWidget(
            setting_widget)
        preferences_window.show()

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
        theme = 'dark'
        if themeIndex == 0:
            theme = 'dark'
            self.ThemeColor = '#4772B3'
            self.BgColor = '#202020'
            self.BorderColor = '#4a4a4a'
        elif themeIndex == 1:
            theme = 'light'
            self.ThemeColor = '#5F85C1'
            self.BgColor = '#ddd'
            self.BorderColor = '#777'
        else:
            # 2
            theme = 'gray'
            self.ThemeColor = '#C85130'
            self.BgColor = '#333'
            self.BorderColor = '#4a4a4a'
        self.thisTheme = theme
        self.themeIndex = themeIndex
        print(Color.YELLOW, '[system] : Set Theme :', theme, Color.END)

        # 设置基础主题
        if theme == 'dark':
            # dark theme
            palette = QPalette()
            palette.setColor(QPalette.Window, QColor(30, 31, 33))
            palette.setColor(QPalette.WindowText, Qt.white)
            palette.setColor(QPalette.Base, QColor(45, 45, 46))
            palette.setColor(QPalette.AlternateBase, QColor(37, 37, 38))
            palette.setColor(QPalette.ToolTipBase, Qt.white)
            palette.setColor(QPalette.ToolTipText, Qt.white)
            palette.setColor(QPalette.Text, Qt.white)
            palette.setColor(QPalette.Button, QColor(37, 37, 38))
            palette.setColor(QPalette.ButtonText, Qt.white)
            palette.setColor(QPalette.BrightText, Qt.red)
            palette.setColor(QPalette.Link, QColor(71, 114, 179))
            palette.setColor(QPalette.Highlight, QColor(71, 114, 179))
            palette.setColor(QPalette.HighlightedText, Qt.black)
            self.setPalette(palette)
            # change Icon color
            # 模拟器3D视图修改背景色-dark
            for vtkViewer in self.Simulator_vtk:
                vtkViewer.selectionchange(False, 'default')
            for vtkWidget in self._mainVtk_:
                vtkWidget.selectionchange(False, 'default')
            # 默认颜色
            if self.UseDefaultBG:
                for vtkWidget in self._mainVtk_:
                    vtkWidget.renderer.SetBackground(40/255, 40/255, 40/255)
                    vtkWidget.renderer.SetBackground2(40/255, 40/255, 40/255)

        elif theme == 'light':
            # light
            palette = QPalette()
            palette.setColor(QPalette.Window, QColor(241, 243, 249))
            palette.setColor(QPalette.WindowText, Qt.black)
            palette.setColor(QPalette.Base, QColor(231, 233, 239))
            palette.setColor(QPalette.AlternateBase, QColor(237, 237, 238))
            palette.setColor(QPalette.ToolTipBase, Qt.black)
            palette.setColor(QPalette.ToolTipText, Qt.black)
            palette.setColor(QPalette.Text, Qt.black)
            palette.setColor(QPalette.Button, QColor(231, 233, 239))
            palette.setColor(QPalette.ButtonText, Qt.black)
            palette.setColor(QPalette.BrightText, Qt.red)
            palette.setColor(QPalette.Link, QColor(95, 133, 193))
            palette.setColor(QPalette.Highlight, QColor(95, 133, 193))
            palette.setColor(QPalette.HighlightedText, Qt.white)
            self.setPalette(palette)
            # 模拟器3D视图修改背景色-light
            for vtkViewer in self.Simulator_vtk:
                vtkViewer.selectionchange(False, 'light')
            for vtkWidget in self._mainVtk_:
                vtkWidget.selectionchange(False, 'light')
            # 默认颜色
            if self.UseDefaultBG:
                for vtkWidget in self._mainVtk_:
                    vtkWidget.renderer.SetBackground(153/255, 153/255, 153/255)
                    vtkWidget.renderer.SetBackground2(
                        153/255, 153/255, 153/255)

        else:
            # gray
            # 基础主题与dark类似，某些地方进行修改
            palette = QPalette()
            palette.setColor(QPalette.Window, QColor(30, 31, 33))
            palette.setColor(QPalette.WindowText, Qt.white)
            palette.setColor(QPalette.Base, QColor(45, 45, 46))
            palette.setColor(QPalette.AlternateBase, QColor(37, 37, 38))
            palette.setColor(QPalette.ToolTipBase, Qt.white)
            palette.setColor(QPalette.ToolTipText, Qt.white)
            palette.setColor(QPalette.Text, Qt.white)
            palette.setColor(QPalette.Button, QColor(37, 37, 38))
            palette.setColor(QPalette.ButtonText, Qt.white)
            palette.setColor(QPalette.BrightText, Qt.red)
            palette.setColor(QPalette.Link, QColor(200, 81, 48))
            palette.setColor(QPalette.Highlight, QColor(200, 81, 48))
            palette.setColor(QPalette.HighlightedText, Qt.black)
            self.setPalette(palette)
            # 模拟器3D视图修改背景色-gray
            for vtkViewer in self.Simulator_vtk:
                vtkViewer.selectionchange(False, 'gray')
            for vtkWidget in self._mainVtk_:
                vtkWidget.selectionchange(False, 'gray')
            # 默认颜色
            if self.UseDefaultBG:
                for vtkWidget in self._mainVtk_:
                    vtkWidget.renderer.SetBackground(64/255, 64/255, 64/255)
                    vtkWidget.renderer.SetBackground2(64/255, 64/255, 64/255)

        # 设置变色图标的样式
        for Widget in self.changeIconList:
            try:
                Widget.setIcon(
                    QIcon(f'img/appIcon/{self.thisTheme}/{Widget.iconPath}'))
            except:
                pass

        # 设置终端的样式
        for terminal_widget in self.Terminal_List:
            try:
                if theme == 'light':
                    terminal_widget[0].set_default_style('lightbg')
                else:
                    terminal_widget[0].set_default_style('linux')
            except:
                pass

        # 设置面板样式
        for widget in self.ChangePanelColor:
            try:
                widget._update_()
            except:
                pass

        # 批处理self.changeTheme_list里的控件
        for changeTheme_widget in self.changeTheme_list:
            try:
                changeTheme_widget.changeTheme(self.themeIndex)
            except:
                pass

        if self.appMode == 'Frameless':
            if themeIndex == 0:
                # dark
                self.titleBar.setStyleSheet(
                    '#CustomTitleBar{background-color: #1d1d1d;}')
                self.spaceWidget.setStyleSheet(
                    '#spaceWidget{background-color: #1d1d1d;}')
                self.tabWidget.setStyleSheet(
                    'background-color: #1d1d1d;')
                # min
                self.titleBar.minBtn.setNormalColor(Qt.white)
                self.titleBar.minBtn.setNormalBackgroundColor(
                    QColor('#1d1d1d'))
                # max
                self.titleBar.maxBtn.setNormalColor(Qt.white)
                self.titleBar.maxBtn.setNormalBackgroundColor(
                    QColor('#1d1d1d'))
                # clsoe
                self.titleBar.closeBtn.setNormalColor(Qt.white)
                self.titleBar.closeBtn.setNormalBackgroundColor(
                    QColor('#1d1d1d'))
            elif themeIndex == 1:
                # light
                self.titleBar.setStyleSheet(
                    '#CustomTitleBar{background-color: #ABABAB;}')
                self.spaceWidget.setStyleSheet(
                    '#spaceWidget{background-color: #ABABAB;}')
                self.tabWidget.setStyleSheet(
                    'background-color: #ABABAB;')
                # min
                self.titleBar.minBtn.setNormalColor(Qt.black)
                self.titleBar.minBtn.setNormalBackgroundColor(
                    QColor('#ABABAB'))
                # max
                self.titleBar.maxBtn.setNormalColor(Qt.black)
                self.titleBar.maxBtn.setNormalBackgroundColor(
                    QColor('#ABABAB'))
                # clsoe
                self.titleBar.closeBtn.setNormalColor(Qt.black)
                self.titleBar.closeBtn.setNormalBackgroundColor(
                    QColor('#ABABAB'))
            else:
                # gray
                self.titleBar.setStyleSheet(
                    '#CustomTitleBar{background-color: #4c4c4c;}')
                self.spaceWidget.setStyleSheet(
                    '#spaceWidget{background-color: #4c4c4c;}')
                self.tabWidget.setStyleSheet(
                    'background-color: #4c4c4c;')
                # min
                self.titleBar.minBtn.setNormalColor(Qt.white)
                self.titleBar.minBtn.setNormalBackgroundColor(
                    QColor('#4c4c4c'))
                # max
                self.titleBar.maxBtn.setNormalColor(Qt.white)
                self.titleBar.maxBtn.setNormalBackgroundColor(
                    QColor('#4c4c4c'))
                # clsoe
                self.titleBar.closeBtn.setNormalColor(Qt.white)
                self.titleBar.closeBtn.setNormalBackgroundColor(
                    QColor('#4c4c4c'))

        # 设置 QSS 样式
        if self.DockStyle == 'Window':
            with open(f'./theme/Window/{theme}.qss', 'r', encoding='utf-8') as Style:
                self.setStyleSheet(Style.read())
        elif self.DockStyle == 'MacOs':
            with open(f'./theme/MacOs/{theme}.qss', 'r', encoding='utf-8') as Style:
                self.setStyleSheet(Style.read())
        elif self.DockStyle == 'MacOs_2':
            with open(f'./theme/MacOs/{theme}.qss', 'r', encoding='utf-8') as Style:
                self.setStyleSheet(Style.read()+self.macOs_2_style)
        elif self.DockStyle == 'MacOs_3':
            with open(f'./theme/MacOs/{theme}.qss', 'r', encoding='utf-8') as Style:
                self.setStyleSheet(Style.read()+self.macOs_3_style)
        elif self.DockStyle == 'Graph':
            with open(f'./theme/MacOs/{theme}.qss', 'r', encoding='utf-8') as Style:
                self.setStyleSheet(Style.read()+self.graph_style)

    def resize_icon(self, icon, size):
        pixmap = icon.pixmap(size)
        scaled_pixmap = pixmap.scaled(size.width(), size.height(
        ), aspectRatioMode=Qt.KeepAspectRatio, transformMode=Qt.SmoothTransformation)
        return QIcon(scaled_pixmap)

    def makeStatus(self):
        status_bar = self.statusBar()
        status_bar.setToolTip('''<b>3D视图快捷键 :</b>
<div style="white-space: pre;">
<a style="color:gray;">按键</a>   <a style="color:orange;">W</a>\t\t网格显示模型
<a style="color:gray;">按键</a>   <a style="color:orange;">S</a>\t\t曲面显示模型
<a style="color:gray;">按键</a>   <a style="color:orange;">P</a>\t\t显示模型包围框
<a style="color:gray;">按键</a>   <a style="color:orange;">F</a>\t\t放大到选取点
<a style="color:gray;">按键</a>   <a style="color:orange;">R</a>\t\t重置相机视图
<a style="color:gray;">按键</a>   <a style="color:orange;">A</a>\t\t切换演员模式
<a style="color:gray;">按键</a>   <a style="color:orange;">C</a>\t\t切换相机模式
<a style="color:gray;">按键</a>   <a style="color:orange;">T</a>\t\t切换轨迹球模式
<a style="color:gray;">按键</a>   <a style="color:orange;">J</a>\t\t切换操纵杆模式
</div><br/>
<b >3D视图操作 :</b>
<div style="white-space: pre;">
<a style="color:gray;">鼠标</a>   <a style="color:orange;">左键</a> <img src="./img/appIcon/mouse_lmb.svg" width="18px" height="18px" align="top">\t\t选取物体
<a style="color:gray;">鼠标</a>   <a style="color:orange;">右键</a> <img src="./img/appIcon/mouse_rmb.svg" width="18px" height="18px" align="top">\t\t显示菜单
<a style="color:gray;">鼠标</a>   <a style="color:orange;">左键</a>   <a style="color:orange;">拖动</a> <img src="./img/appIcon/mouse_lmb_drag.svg" width="18px" height="18px" align="top">\t转动视角
<a style="color:gray;">鼠标</a>   <a style="color:orange;">右键</a>   <a style="color:orange;">拖动</a> <img src="./img/appIcon/mouse_rmb_drag.svg" width="18px" height="18px" align="top">\t缩放视角
<a style="color:gray;">鼠标</a>   <a style="color:orange;">中键</a>   <a style="color:orange;">滚动</a> <img src="./img/appIcon/mouse_mmb_drag.svg" width="18px" height="18px" align="top">\t缩放视角
<a style="color:gray;">鼠标</a>   <a style="color:orange;">中键</a>   <a style="color:orange;">拖动</a> <img src="./img/appIcon/mouse_mmb_drag.svg" width="18px" height="18px" align="top">\t平移视图

</div>''')
        status_bar.installEventFilter(ToolTipFilter(
            status_bar, 300, ToolTipPosition.TOP))
        layout = status_bar.layout()

        status_bar.setFixedHeight(25)  # 清除 QStatusBar 样式表
        layout.setContentsMargins(0, 0, 0, 0)
        status_bar.setContentsMargins(10, 0, 0, 0)
        #
        # status_bar.setFixedHeight(25)
        # add the widget to the layout
        self.leftClick = QPushButton()
        self.leftClick.setObjectName('statusButton')
        self.leftClick.setText('旋转视图 (Rotate)')
        self.leftClick.setIconSize(QSize(20, 20))
        self.leftClick.setIcon(
            QIcon(f'img/appIcon/{self.Puretheme}/mouse_lmb_drag.svg'))
        self.leftClick.iconPath = 'mouse_lmb_drag.svg'
        self.changeIconList.append(self.leftClick)
        status_bar.addPermanentWidget(self.leftClick, 0)
        #
        self.rightClick = QPushButton()
        self.rightClick.setText('缩放视图 (Zoom)')
        self.rightClick.setObjectName('statusButton')
        self.rightClick.setIconSize(QSize(20, 20))
        status_bar.addPermanentWidget(self.rightClick, 1)
        self.rightClick.setIcon(
            QIcon(f'img/appIcon/{self.Puretheme}/mouse_rmb_drag.svg'))
        self.rightClick.iconPath = 'mouse_rmb_drag.svg'
        self.changeIconList.append(self.rightClick)
        #
        self.wheelClick = QPushButton()
        self.wheelClick.setText('移动视图 (Move)')
        self.wheelClick.setObjectName('statusButton')
        self.wheelClick.setIconSize(QSize(20, 20))
        status_bar.addPermanentWidget(self.wheelClick, 1)
        self.wheelClick.setIcon(
            QIcon(f'img/appIcon/{self.Puretheme}/mouse_mmb_drag.svg'))
        self.wheelClick.iconPath = 'mouse_mmb_drag.svg'
        self.changeIconList.append(self.wheelClick)
        #
        self.wheelMove = QPushButton()
        self.wheelMove.setText('缩放视图 (Zoom)')
        self.wheelMove.setObjectName('statusButton')
        self.wheelMove.setIconSize(QSize(20, 20))
        status_bar.addPermanentWidget(self.wheelMove, 1)
        self.wheelMove.setIcon(
            QIcon(f'img/appIcon/{self.Puretheme}/mouse_mmb_drag.svg'))
        self.wheelMove.iconPath = 'mouse_mmb_drag.svg'
        self.changeIconList.append(self.wheelMove)
        # LABEL
        status_bar.addPermanentWidget(QWidget(), 2)
        # 创建内存获取线程并启动
        self.memory_thread = MemoryThread()
        self.memory_thread.memory_update.connect(self.update_memory)
        self.memory_thread.start()
        # label 2
        self.label_2 = QPushButton()
        self.label_2.setObjectName('statusButton')
        self.label_2.setText('内存: None MB | 0.0.2 beta')
        status_bar.addPermanentWidget(self.label_2, 0)

    def update_memory(self, memory_MB):
        self.label_2.setText(f'内存: {memory_MB:.2f} MB | 0.0.2 beta')

    def expand_tree_widget_items(self, tree_widget):
        root_item = tree_widget.invisibleRootItem()
        for i in range(root_item.childCount()):
            item = root_item.child(i)
            self.expand_tree_item(item)

    def expand_tree_item(self, item):
        item.setExpanded(True)
        for i in range(item.childCount()):
            child_item = item.child(i)
            self.expand_tree_item(child_item)

    def runObjects(self, nbtData, filePath):
        '''
        from SV 0.0.2
        '''
        for objectViewIndex in self.objectView_list:
            objectView = self.objectView_list[objectViewIndex]
            objectView.clear()
            objectView.LastPickerActor = None  # 清空状态:上一个拾取
            # set style end
            _, fileType = os.path.splitext(filePath)
            worldType = '[UnkownWorldType]'
            Size = 'size:[0,0]'
            if fileType == '.nbt':
                worldType = 'Nbt'
                Size = f'size : NBT[ x:{str(int(nbtData["size"][0]))} , y:{str(int(nbtData["size"][1]))} , z:{str(int(nbtData["size"][2]))} ]'
            elif fileType == '.mca':
                worldType = 'Region'
                Size = f'size : MCA[{str(len(nbtData))} chunks]'
            world = QTreeWidgetItem(objectView)
            world.setText(0, worldType + ' ' + Size)
            world.setIcon(
                0, QIcon('img/toolbar/d_ToolHandleLocal@2x.png'))
            # world.setCheckState(0, Qt.Checked)
            # add node
            objectView.addTopLevelItem(world)
            # if mca or nbt
            if fileType == '.mca':
                for chunkName in nbtData:
                    chunk = QTreeWidgetItem()
                    chunk.setText(0, 'chunk '+chunkName)
                    chunk.setIcon(0, QIcon('./img/3d_orange.svg'))
                    world.addChild(chunk)
            elif fileType == '.nbt':
                try:
                    for blockType in nbtData['palette']:
                        block = QTreeWidgetItem()
                        block.setText(0, blockType['Name'])
                        block.setIcon(0, QIcon('./img/3d.svg'))
                        world.addChild(block)
                except Exception:
                    print('[NBT error] : function-runObjects', nbtData,
                          traceback.format_exc())
            # 点击事件
            objectView.itemClicked.connect(self.on_item_clicked)
            self.expendFunc.expendSingal.emit(world)

    def LoadObjectInOneWindow(self, nbtData, filePath, objTree):
        '''
        在一个窗口内加载object
        '''
        objectView = objTree
        objectView.clear()
        objectView.LastPickerActor = None  # 清空状态:上一个拾取
        # set style end
        _, fileType = os.path.splitext(filePath)
        worldType = '[UnkownWorldType]'
        Size = 'size:[0,0]'
        if fileType == '.nbt':
            worldType = 'Nbt'
            Size = f'size : NBT [ x:{str(int(nbtData["size"][0]))} , y:{str(int(nbtData["size"][1]))} , z:{str(int(nbtData["size"][2]))} ]'
        elif fileType == '.mca':
            worldType = 'Region'
            Size = f'size : MCA [ {str(len(nbtData))} chunks ]'
        world = QTreeWidgetItem(objectView)
        world.setText(0, worldType + ' ' + Size)
        world.setIcon(0, QIcon('img/toolbar/d_ToolHandleLocal@2x.png'))
        print(world)
        # world.setCheckState(0, Qt.Checked)
        # add node
        objectView.addTopLevelItem(world)
        # if mca or nbt
        if fileType == '.mca':
            for chunkName in nbtData:
                chunk = QTreeWidgetItem()
                chunk.setText(0, 'chunk '+chunkName)
                chunk.setIcon(0, QIcon('./img/3d_orange.svg'))
                world.addChild(chunk)
        elif fileType == '.nbt':
            try:
                for blockType in nbtData['palette']:
                    block = QTreeWidgetItem()
                    block.setText(0, blockType['Name'])
                    block.setIcon(0, QIcon('./img/3d.svg'))
                    world.addChild(block)
            except Exception:
                print('[NBT error] : function-runObjects', nbtData,
                      traceback.format_exc())
        # 点击事件
        objectView.itemClicked.connect(self.on_item_clicked)
        self.expendFunc.expendSingal.emit(world)

    def expend_singal(self, node):
        node.setExpanded(True)

    def on_item_clicked(self, item, column):
        sender_tree_widget = self.sender()
        if isinstance(sender_tree_widget, QTreeWidget):
            text = item.text(column).replace('minecraft:', '')
            if text in self.Actor_Block_Dict:
                # 如果点击的方块类型在记录里
                if sender_tree_widget.LastPickerActor == self.Actor_Block_Dict[text]:
                    # 如果此方块等于上一个点击的方块,则什么都不做
                    pass
                else:
                    # 否则就同步状态
                    if sender_tree_widget.LastPickerActor != None:
                        sender_tree_widget.LastPickerActor.outline_actor.VisibilityOff()
                        sender_tree_widget.LastPickerActor.outline_actor.GetProperty().SetColor(1,
                                                                                                0.522, 0)  # 橙色
                    if self.Actor_Block_Dict[text] != None:
                        self.Actor_Block_Dict[text].outline_actor.GetProperty().SetColor(0,
                                                                                         0.647, 1)  # 蓝色
                        self.Actor_Block_Dict[text].outline_actor.VisibilityOn(
                        )
                    else:
                        sender_tree_widget.LastPickerActor.outline_actor.VisibilityOff()
                        sender_tree_widget.LastPickerActor.outline_actor.GetProperty().SetColor(1,
                                                                                                0.522, 0)  # 橙色
                    sender_tree_widget.LastPickerActor = self.Actor_Block_Dict[text]
            # 重新渲染一遍
            for vtkWidget in self._mainVtk_:
                vtkWidget.renderer.GetRenderWindow().Render()


'''
##############################################################################
# start Application
# 2023.11.16
##############################################################################
'''

QFontDatabase.addApplicationFont('./font/zpix.ttf')
QWebEngineSettings.globalSettings().setAttribute(
    QWebEngineSettings.PluginsEnabled, True)
QWebEngineSettings.globalSettings().setAttribute(
    QWebEngineSettings.ScreenCaptureEnabled, True)
App.setStyle("Fusion")


def OpenAPP(Mode: str = 'native') -> None:
    # Fusion dark palette from https://gist.github.com/QuantumCD/6245215.
    if Mode == 'Frameless':
        FramelessStructureViewer = type(
            'StructureViewer', (FramelessMainWindow,), dict(StructureViewer.__dict__))
        StructureViewerApp = FramelessStructureViewer(
            App, Mode, os.getcwd().replace('\\', '/'), None)
        StructureViewerApp.PostValueToTerminal()
        StructureViewerApp.showStartWindow()
    else:
        StructureViewerApp = StructureViewer(
            App, Mode, os.getcwd().replace('\\', '/'), None)
        StructureViewerApp.PostValueToTerminal()
        StructureViewerApp.showStartWindow()
    # 恢复全局参数
    # StructureStudioApp._RECOVER_GLOBALS_ENVIRONMENT_TO_CONSOLE_()


# 'Frameless'
OpenAPP('Frameless')
# 进行性能检查
sys.exit(App.exec())
