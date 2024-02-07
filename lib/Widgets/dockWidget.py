# coding:utf-8
import os
import platform
from PyQt5 import QtCore, QtGui
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import PyQt5.QtWidgets as QtWidgets
from PyQt5.QtCore import *
from lib.Widgets.menu import PureRoundedBorderMenu
from lib.Widgets.tooltip import ToolTipFilter, ToolTipPosition
if platform.system() == 'Windows':
    from win32mica import ApplyMica, MicaTheme, MicaStyle
    import win32mica

# 浮动窗口


class Vline(QFrame):
    def __init__(self, width: int = 1):
        super(Vline, self).__init__()
        self.setFixedWidth(width)
        self.setStyleSheet(
            'background-color:rgba(175,175,175,0.3); margin-bottom:5px;margin-top:2px;')


class Hline(QFrame):
    def __init__(self, height: int = 1):
        super(Hline, self).__init__()
        self.setFixedHeight(height)
        self.setFrameShape(QFrame.HLine)  # 设置框架为横线
        self.setFrameShadow(QFrame.Sunken)
        self.setObjectName('Hline')


class Pure_QDockWidget(QDockWidget):
    def __init__(self, _parent_, Wtype: str, page):
        super().__init__(_parent_)
        self.setMinimumWidth(200)
        self.setMinimumHeight(40)
        self.mica = False
        self._parent_ = _parent_
        self.Wtype = Wtype
        self.CanClose = False
        self.LastFloating = False
        self.page = page
        # widget
        self.MainWidget = QWidget()
        self.MainWidget.setObjectName("MainWidget")
        self.WindowLayout = QVBoxLayout(self.MainWidget)
        self.WindowLayout.setContentsMargins(0, 0, 0, 0)
        self.WindowLayout.setSpacing(0)
        self.setWidget(self.MainWidget)
        self.topLevelChanged.connect(self.IF_MICA)
        self.setWindowTitle('')
        # set window choose button
        self.TopMenu = QWidget(self)
        self.TopMenu.setObjectName('Window_TopMenu')
        self.TopMenu.setStyleSheet(
            '#Window_TopMenu{background-color:rgba(0,0,0,0) !important;}')
        self.TopMenu.setFixedHeight(24)
        self.TopMenu.setFixedWidth(130)
        # 第二个
        self.TopMenu_2 = QWidget(self)
        self.TopMenu_2.setMinimumWidth(0)
        self.TopMenu_2.setObjectName('Window_TopMenu')
        self.TopMenu_2.setStyleSheet(
            '#Window_TopMenu{background-color:rgba(0,0,0,0) !important;}')
        self.TopMenu_2.setFixedHeight(24)
        self.TopMenu_2.move(135, 0)
        # 按钮部分
        self.TopMenu_layout = QHBoxLayout(self.TopMenu)
        self.TopMenu_layout.setContentsMargins(0, 2, 0, 0)
        self.TopMenu.move(5, 0)
        self.TopMenu_layout.setSpacing(5)
        #
        self.ViewButton = QPushButton("视图")  # 视图按钮
        self.MakeViewFunction()
        self.ViewButton.setFixedSize(40, 21)
        self.ViewButton.setObjectName('ButtonMenuBar')
        self.ViewButton.clicked.connect(self.viewClicked)
        #
        self.SettingButton = QPushButton("设置")  # 视图按钮
        self.MakeSettingFunction()
        self.SettingButton.setFixedSize(40, 21)
        self.SettingButton.setObjectName('ButtonMenuBar')
        self.SettingButton.clicked.connect(self.settingClicked)
        #
        self.Choose_WindowType = QToolButton()
        self.Choose_WindowType.setObjectName('Choose_Window')
        self.Choose_WindowType.setToolTip(
            f'<div><b>编辑器类型</b><br/>此区域当前的编辑器类型 : <a style="color:orange;">{self.Wtype}</a></div>')
        self.Choose_WindowType.installEventFilter(ToolTipFilter(
            self.Choose_WindowType, 300, ToolTipPosition.BOTTOM_LEFT))
        self.Choose_WindowType.setPopupMode(QToolButton.InstantPopup)
        self.Choose_WindowType.setIcon(
            QIcon(self._parent_.windowType[self.Wtype][0]))
        self.Choose_WindowType.clicked.connect(self.changeWindow)
        self.TopMenu_layout.addWidget(self.Choose_WindowType)
        self.Choose_WindowType.setFixedSize(35, 21)
        self.MakeChooseButton()
        #
        self.PageLayout = QHBoxLayout(self.TopMenu_2)  # 每个页面自定义的布局部分
        self.PageLayout.setContentsMargins(0, 2, 0, 0)
        self.TopMenu_layout.addWidget(self.ViewButton)
        self.TopMenu_layout.addWidget(self.SettingButton)
        self.TopMenu_layout.addStretch(9999)
        self.newWindowInit(self.Wtype)

    def MakeSettingFunction(self):
        self.SettingMenu = PureRoundedBorderMenu(self)
        action1 = QAction('设置窗口样式 (setting window)', self)
        self.SettingMenu.addAction(action1)

    def settingClicked(self):
        self.SettingMenu.exec_(self.SettingButton.mapToGlobal(
            self.SettingButton.rect().bottomLeft()))

    def MakeViewFunction(self):
        self.ViewMenu = PureRoundedBorderMenu(self)
        action1 = QAction('水平分割 (split horizontal)', self)
        action1.setIcon(QIcon('img/main/split_R.png'))
        action1.triggered.connect(self.split_H)
        action2 = QAction('垂直分割 (split vertical)', self)
        action2.setIcon(QIcon('img/main/split_v.png'))
        action2.triggered.connect(self.split_V)
        action3 = QAction('浮动窗口 (float window)', self)
        action3.setIcon(QIcon('img/main/out3_2.png'))
        action3.triggered.connect(lambda: self.setFloating(1))
        self.ViewMenu.addAction(action1)
        self.ViewMenu.addAction(action2)
        self.ViewMenu.addAction(action3)
        self.ViewMenu.addSeparator()
        action5 = QAction('关闭窗口 (close window)', self)
        action5.setIcon(QIcon('img/main/close_this.png'))
        action5.triggered.connect(self.close)
        self.ViewMenu.addAction(action5)

    def split_H(self):
        new_window = Pure_QDockWidget(
            self._parent_, Wtype='空白页面', page=self.page)
        self._parent_.Page_Index[str(self.page)].append(new_window)
        new_window.page = self.page
        #
        self._parent_.splitDockWidget(self,
                                      new_window, Qt.Horizontal)

    def split_V(self):
        new_window = Pure_QDockWidget(
            self._parent_, Wtype='空白页面', page=self.page)
        self._parent_.Page_Index[str(self.page)].append(new_window)
        new_window.page = self.page
        #
        self._parent_.splitDockWidget(self,
                                      new_window, Qt.Vertical)

    def viewClicked(self):
        self.ViewMenu.exec_(self.ViewButton.mapToGlobal(
            self.ViewButton.rect().bottomLeft()))

    def MakeChooseButton(self):
        # 创建一个下拉菜单
        self.menu = PureRoundedBorderMenu(self)
        self.menu.setStyleSheet('''
                            QMenu{padding:0px !important;border-top-left-radius:0px !important;}''')
        Panel = QWidget()
        Panel.setStyleSheet('''
                            #ButtonMenu {text-align:left;}
                            QLabel {
                                padding-left:5px;
                                margin-bottom:10px;
                                margin-top:5px;
                            }''')
        Panel.setFixedSize(600, 220)
        ChoosePanel_Action = QWidgetAction(self.menu)
        ChoosePanel_Action.setDefaultWidget(Panel)
        self.menu.addAction(ChoosePanel_Action)
        PanelLayout = QHBoxLayout(Panel)
        PanelLayout.setContentsMargins(0, 0, 0, 0)
        PanelLayout.setSpacing(0)
        # 将下拉菜单关联到工具按钮
        self.Choose_WindowType.setMenu(self.menu)
        # 选择面板主要部分
        BaseLabel = QLabel('基础')
        BaseLabel.setStyleSheet('margin-left:2px;')
        simulatorLabel = QLabel('模拟')
        simulatorLabel.setStyleSheet('margin-left:2px;')
        ToolLabel = QLabel('工具')
        ToolLabel.setStyleSheet('margin-left:2px;')
        DebugLabel = QLabel('调试')
        DebugLabel.setStyleSheet('margin-left:2px;')
        #
        BaseLayout = QVBoxLayout()
        BaseLayout.setContentsMargins(0, 0, 0, 0)
        BaseLayout.setSpacing(0)
        ToolLayout = QVBoxLayout()
        ToolLayout.setContentsMargins(0, 0, 0, 0)
        ToolLayout.setSpacing(0)
        simulatorLayout = QVBoxLayout()
        simulatorLayout.setContentsMargins(0, 0, 0, 0)
        simulatorLayout.setSpacing(0)
        DebugLayout = QVBoxLayout()
        DebugLayout.setContentsMargins(0, 0, 0, 0)
        DebugLayout.setSpacing(0)
        PanelLayout.addLayout(BaseLayout)
        PanelLayout.addLayout(simulatorLayout)
        PanelLayout.addLayout(ToolLayout)
        PanelLayout.addLayout(DebugLayout)
        #
        BaseLayout.addWidget(BaseLabel)
        BaseLayout.addWidget(Hline())
        simulatorLayout.addWidget(simulatorLabel)
        simulatorLayout.addWidget(Hline())
        ToolLayout.addWidget(ToolLabel)
        ToolLayout.addWidget(Hline())
        DebugLayout.addWidget(DebugLabel)
        DebugLayout.addWidget(Hline())
        # add button -> base
        for base_window in self._parent_.base_Windows:
            newButton = QPushButton()
            newButton.setFixedHeight(24)
            newButton.setObjectName('ButtonMenu')
            newButton.WindowName = base_window
            newButton.setText(base_window)
            newButton.clicked.connect(self.changeWindow)
            newButton.setStyleSheet(f'''#ButtonMenu {{
                background-image: url({self._parent_.base_Windows[base_window][0]});
                background-repeat: no-repeat;
                background-position: left center;
                padding-left:20px;
                margin-left:5px;
            }}
                                    ''')
            BaseLayout.addWidget(newButton)
        BaseLayout.addStretch(9999)
        # add button -> simulator
        for simulator_window in self._parent_.simulator_Windows:
            newButton = QPushButton()
            newButton.setFixedHeight(24)
            newButton.setObjectName('ButtonMenu')
            newButton.WindowName = simulator_window
            newButton.setText(simulator_window)
            newButton.clicked.connect(self.changeWindow)
            newButton.setStyleSheet(f'''#ButtonMenu {{
                background-image: url({self._parent_.simulator_Windows[simulator_window][0]});
                background-repeat: no-repeat;
                background-position: left center;
                padding-left:20px;
                margin-left:5px;
            }}
                                    ''')
            simulatorLayout.addWidget(newButton)
        simulatorLayout.addStretch(9999)
        # add button -> tool
        for tool_window in self._parent_.tool_Windows:
            newButton = QPushButton()
            newButton.setFixedHeight(24)
            newButton.setObjectName('ButtonMenu')
            newButton.WindowName = tool_window
            newButton.setText(tool_window)
            newButton.clicked.connect(self.changeWindow)
            newButton.setStyleSheet(f'''#ButtonMenu {{
                background-image: url({self._parent_.tool_Windows[tool_window][0]});
                background-repeat: no-repeat;
                background-position: left center;
                padding-left:20px;
                margin-left:5px;
            }}
                                    ''')
            ToolLayout.addWidget(newButton)
        ToolLayout.addStretch(9999)
        # add button -> debug
        for debug_window in self._parent_.debug_Windows:
            newButton = QPushButton()
            newButton.setFixedHeight(24)
            newButton.setObjectName('ButtonMenu')
            newButton.WindowName = debug_window
            newButton.setText(debug_window)
            newButton.clicked.connect(self.changeWindow)
            newButton.setStyleSheet(f'''#ButtonMenu {{
                background-image: url({self._parent_.debug_Windows[debug_window][0]});
                background-repeat: no-repeat;
                background-position: left center;
                padding-left:20px;
                margin-left:5px;
            }}
                                    ''')
            DebugLayout.addWidget(newButton)
        DebugLayout.addStretch(9999)

    def changeWindow(self):
        self.menu.hide()
        windowName = self.sender().WindowName
        # 如果不是原来的那个窗口
        if windowName != self.Wtype:
            print('changeWindow to %s' % windowName)
            self.setObjectName(windowName)
            self.TopMenu_2.setMinimumWidth(0)
            # 先删除原来的
            self.deleteWindow()
            # 改变button的图标
            self.Choose_WindowType.setIcon(
                QIcon(self._parent_.windowType[windowName][0]))
            # 再重新加载一下新的
            self.newWindowInit(windowName)
            self.Choose_WindowType.setToolTip(
                f'<br>编辑器类型</br>\n此区域当前的编辑器类型 : {windowName}')

    def newWindowInit(self, windowName: str):
        '''
        Resource(
            self, self.Resource_window, openPath=self.openPath)
        '''
        print('[!] : 初始化 窗口:', windowName)
        GetWindow = False
        for _new_dockWidget_ in self._parent_.Window_Save_Widget[windowName]:
            if _new_dockWidget_.isHidden():
                print('[#] : find already dock widget')
                # 如果他的父类是None，说明他没有被占用
                # 如果要新建的窗口在储存里已经有了，就直接拿来用
                self.ThisWindowWidget = _new_dockWidget_
                self.ThisWindowWidget.show()
                self.ThisWindowWidget.page = self.page  # 更新page检索
                self.WindowLayout.addWidget(self.ThisWindowWidget)
                self.Wtype = windowName
                self.setObjectName(windowName)
                GetWindow = True
                # 直接返回退出函数
                try:
                    # 调用自定义的显示函数
                    # 假定每个PureWidget的自定义控件都实现了showDefineWidget方法
                    self.ThisWindowWidget.showDefineWidget()
                except:
                    pass
        if GetWindow == False:
            print('[+] : new dock widget')
            # 如果没有return，说明没有空闲的此类dockwidget
            self.ThisWindowWidget = self._parent_.windowType[windowName][1](
                self._parent_, self, openPath=self._parent_.openPath)
            self.WindowLayout.addWidget(self.ThisWindowWidget)
            self._parent_.Window_Save_Widget[windowName].append(
                self.ThisWindowWidget)
            self.Wtype = windowName
            self.setObjectName(windowName)

    def deleteWindow(self):
        if self.Wtype == '3D视图' or self.Wtype == '模拟视图':
            # 尝试关闭vtkwidget
            self.ThisWindowWidget.vtkWidget.Finalize()
        # 尝试删除一下自定义布局里的东西
        try:
            item_list = list(
                range(self.PageLayout.count()))
            item_list.reverse()  # 倒序删除，避免影响布局顺序
            for i in item_list:
                item = self.PageLayout.itemAt(i)
                self.PageLayout.removeItem(item)
                item.widget().deleteLater()
                if item.widget():
                    item.widget().deleteLater()
        except:
            print(self.Wtype, ':没有自定义布局可删除')
        self.WindowLayout.removeWidget(self.ThisWindowWidget)
        self.ThisWindowWidget.hide()
        '''self._parent_.Window_Save_Widget[self.Wtype].append(
            self.ThisWindowWidget)  # 放进储存字典里'''

    def IF_MICA(self):
        if self.isFloating() == True:
            self.TopMenu.hide()
            self.TopMenu_2.hide()
            self.setWindowTitle(self.Wtype)

            # self.ThisWindowWidget.Mainlayout.setContentsMargins(0, 0,0,0)
        else:
            self.TopMenu.show()
            self.TopMenu_2.show()
            self.setWindowTitle('')

            # self.ThisWindowWidget.Mainlayout.setContentsMargins(0, 4, 0, 3)
        if self.mica == False:
            if platform.system() == 'Windows':
                def callbackFunction(NewTheme):
                    pass
                #
                hwnd = self.winId().__int__()
                mode = MicaTheme.AUTO

                style = MicaStyle.DEFAULT
                win32mica.ApplyMica(HWND=hwnd, Theme=mode, Style=style,
                                    OnThemeChange=callbackFunction)
            else:
                print(
                    f'System : {platform.system()} cannot use Mica Style in {self.winId()}')
        self.mica = True
