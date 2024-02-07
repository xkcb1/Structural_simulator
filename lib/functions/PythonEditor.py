from lib.Widgets.Editor import CodeEditor
from lib.base import *
import keyword
from pygments.lexers import PythonLexer
from PyQt5.Qsci import QsciScintilla, QsciLexerPython, QsciAPIs
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QVBoxLayout, QWidget, QAction, QSplitter
import sys
import inspect
from PyQt5.QtGui import QColor  # 导入 QColor


class PythonEditor(QWidget):
    def __init__(self, parent=None, window=None, openPath=''):
        super(PythonEditor, self).__init__()
        self._parent_ = parent
        self._window_ = window
        self.openPath = openPath
        self.untitledCount = 0
        self.page = self._window_.page
        self.editor = []
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
        self.EditorTabWidget = QTabWidget()
        self.EditorTabWidget.setMovable(1)
        self.EditorTabWidget.setObjectName('EditorTabWidget')
        self.EditorTabWidget.setTabsClosable(1)
        self.Mainlayout.addWidget(self.EditorTabWidget)
        self.EditorTabWidget.setContentsMargins(0, 0, 0, 0)
        self._parent_.changeTheme_list.append(self)
        # 向自定义控件注入组件
        self.addDefineWidget()
        #
        self.AddPythonFile()

    def addDefineWidget(self):
        # 打开按钮
        MyPageLayout = QHBoxLayout()
        MyPageLayout.setContentsMargins(0, 0, 0, 0)
        MyPageLayout.setSpacing(0)
        self.OpenButton = QPushButton()
        self.OpenButton.setStyleSheet('''*{border-top-right-radius:0px;
                           border-bottom-right-radius:0px;
                           padding-left:4px;
                           padding-right:4px;
                           }''')
        self.OpenButton.setFixedHeight(21)
        self.OpenButton.clicked.connect(print)
        self.OpenButton.setText('打开')
        self.OpenButton.setIcon(
            QIcon(f'img/appIcon/{self._parent_.Puretheme}/FolderEmpty Icon.png'))
        self.OpenButton.iconPath = 'FolderEmpty Icon.png'
        self._parent_.changeIconList.append(self.OpenButton)
        self.OpenButton.setToolTip(
            '打开文件 (选择一个文件)\nOpen File (Choose a file in your computer)')
        self.OpenButton.installEventFilter(ToolTipFilter(
            self.OpenButton, 300, ToolTipPosition.BOTTOM))
        self.OpenButton.setIconSize(QSize(18, 18))
        MyPageLayout.addWidget(self.OpenButton)

        # 新建按钮
        self.NewButton = QPushButton()
        self.NewButton.setStyleSheet('''*{border-radius:0px;
                            border-left:0px;
                            padding-left:4px;
                           padding-right:4px;
                           }''')
        self.NewButton.setFixedHeight(21)
        self.NewButton.clicked.connect(self.AddPythonFile)
        self.NewButton.setText('新建')
        self.NewButton.setIcon(
            QIcon(f'img/appIcon/{self._parent_.Puretheme}/plus.svg'))
        self.NewButton.iconPath = 'plus.svg'
        self._parent_.changeIconList.append(self.NewButton)
        self.NewButton.setToolTip(
            '新建文件 (新建一个文件)\nNew File (add a file to your computer)')
        self.NewButton.installEventFilter(ToolTipFilter(
            self.NewButton, 300, ToolTipPosition.BOTTOM))
        self.NewButton.setIconSize(QSize(18, 18))
        MyPageLayout.addWidget(self.NewButton)

        # 另存为按钮
        self.SaveAsButton = QPushButton()
        self.SaveAsButton.setStyleSheet('''*{border-radius:0px;
                            border-left:0px;
                            padding-left:4px;
                           padding-right:4px;
                           }''')
        self.SaveAsButton.setFixedHeight(21)
        self.SaveAsButton.clicked.connect(print)
        self.SaveAsButton.setText('另存为')
        self.SaveAsButton.setIcon(
            QIcon(f'img/appIcon/{self._parent_.Puretheme}/FolderOpened Icon.png'))
        self.SaveAsButton.iconPath = 'FolderOpened Icon.png'
        self._parent_.changeIconList.append(self.SaveAsButton)
        self.SaveAsButton.setToolTip(
            '文件另存为 (选择一个目录另存)\nFile Save As')
        self.SaveAsButton.installEventFilter(ToolTipFilter(
            self.SaveAsButton, 300, ToolTipPosition.BOTTOM))
        self.SaveAsButton.setIconSize(QSize(18, 18))
        MyPageLayout.addWidget(self.SaveAsButton)

        # 语言选择下拉框
        self.languageChoose = QToolButton()
        self.languageChoose.setStyleSheet('''*{border-top-left-radius:0px;
                           border-bottom-left-radius:0px;
                            border-left:0px;
                            padding-left:4px;
                           padding-right:4px;
                           }''')
        self.languageChoose.setToolTip(
            '选择语言高亮模式\nChoose language highlight mode')
        self.languageChoose.installEventFilter(ToolTipFilter(
            self.languageChoose, 300, ToolTipPosition.BOTTOM))
        self.languageChoose.setText('Python')
        self.languageChooseInit()
        self.languageChoose.clicked.connect(print)
        # 添加进自定义布局
        self.languageChoose.setFixedHeight(21)
        MyPageLayout.addWidget(self.languageChoose)

        # 运行按钮
        self.runButton = QPushButton()
        self.runButton.setFixedHeight(21)
        self.runButton.setFixedWidth(21)
        self.runButton.clicked.connect(self.runCode)
        self.runButton.setIcon(
            QIcon(f'img/appIcon/{self._parent_.Puretheme}/play-fill.svg'))
        self.runButton.iconPath = 'play-fill.svg'
        self._parent_.changeIconList.append(self.runButton)
        self.runButton.setToolTip(
            '运行脚本文件 (使用python解释器)\nRun script file (Use Python to run)')
        self.runButton.installEventFilter(ToolTipFilter(
            self.runButton, 300, ToolTipPosition.BOTTOM))
        self.runButton.setIconSize(QSize(18, 18))
        MyPageLayout.addWidget(self.runButton)

        self._window_.PageLayout.addLayout(MyPageLayout)
        self._window_.PageLayout.addWidget(self.runButton)
        self._window_.TopMenu_2.setMinimumWidth(250)

    def showDefineWidget(self):
        # 重新显示此窗口时自动调用
        pass

    def languageChooseInit(self):
        pass

    def runCode(self):
        runCode_Text = self.EditorTabWidget.currentWidget().editor.text()
        for terminal in self._parent_.Terminal_List:
            if terminal[1] == self.page:
                # 在本页面找到了终端，就直接用
                terminal[0].execute(runCode_Text)
                # 运行一个就停止for
                return
            else:
                # 要不然就不管
                pass
        # 如果本页面找不到，就随便找一个好了,self._parent_.Terminal_List里至少会有一个终端的,所以直接拿第一个好了
        self._parent_.Terminal_List[0][0].execute(runCode_Text)

    def AddPythonFile(self, name=None):
        if type(name) != str:
            name = 'untitled '+str(self.untitledCount)
            self.untitledCount += 1
        print('new file: %s' % name)
        Editor = CodeEditor(self._parent_, self._parent_.themeIndex)
        self.editor.append(Editor)
        self.EditorTabWidget.addTab(Editor, QIcon(
            'img/file_script.svg'), name)

    def changeTheme(self, themeIndex):
        for Editor in self.editor:
            try:
                Editor.setTheme(themeIndex)
            except:
                pass
