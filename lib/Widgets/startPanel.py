# coding:utf-8
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

from lib.Widgets.tooltip import ToolTipFilter, ToolTipPosition
# 启动页面


class PStartWidget(QDialog):
    def __init__(self, parent=None, w=520, h=500):
        super().__init__(parent)
        self.window = parent
        self._parent_ = parent
        self.w = w
        self.h = h
        self.setFixedSize(w, h)
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setWindowFlag(Qt.Dialog)
        # 设置圆角
        # 启用窗口透明背景
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.MainWidget = QWidget()
        self.MainLayout = QVBoxLayout(self)
        self.MainLayout.setContentsMargins(9, 9, 9, 9)
        self.MainLayout.addWidget(self.MainWidget)
        self.MainWidget.setObjectName('startPanel')

        # 使用QGraphicsDropShadowEffect添加阴影
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setColor(QColor(0, 0, 0, 100))
        shadow.setBlurRadius(11)
        shadow.setOffset(0, 0)
        self.setGraphicsEffect(shadow)
        #
        self.uiInit()

    def uiInit(self):
        self.starterLayout = QVBoxLayout(self.MainWidget)
        self.starterLayout.setContentsMargins(1, 1, 1, 1)
        self.starterLayout.setSpacing(0)
        self.startImage = QLabel()
        self.startImage.setScaledContents(1)
        self.startImage.setFixedHeight(int(800/3)-25)
        #
        self.starterLayout.addWidget(self.startImage)
        self.startImage.setStyleSheet(
            '''border-top-left-radius:5px !important;
            border-top-right-radius:5px !important;
            background-image: url(img/start/version_2.png);
            background-repeat: no-repeat;
            ''')
        self.OptionsWidget = QWidget()
        self.starterLayout.addWidget(self.OptionsWidget)
        self.optLayout = QVBoxLayout(self.OptionsWidget)
        self.optLayout.setContentsMargins(20, 20, 20, 10)
        self.optLayout.setSpacing(0)
        # 网址Label
        self.weblabel = QLabel(self.MainWidget)
        self.weblabel.setText(self._parent_.url)
        self.weblabel.setFixedSize(250, 20)
        self.weblabel.move(10, 220)
        self.weblabel.setStyleSheet(
            '''background-color:rgba(0,0,0,0) !important;color:rgba(125,125,125,0.7);font-size:10px;''')
        # 版本号
        self.versionLabel = QLabel(self.MainWidget)
        self.versionLabel.setText(self._parent_.version)
        self.versionLabel.setFixedSize(50, 20)
        self.versionLabel.move(440, 5)
        self.versionLabel.setStyleSheet(
            '''background-color:rgba(0,0,0,0) !important;color:rgba(125,125,125,0.7);font-size:10px;
            font-weight:bold;''')
        # 操作面板
        self.topOption = QWidget()
        self.bottomOption = QWidget()
        self.bottomOption.setFixedHeight(70)
        self.optLayout.addWidget(self.topOption)
        self.optLayout.addWidget(self.bottomOption)
        # bottom option
        self.openbutton = QPushButton()
        self.openbutton.setObjectName('ButtonMenuBar')
        self.openbutton.setText('打开文件')
        self.openbutton.setToolTip(
            '打开一个nbt, mca, json类型文件\nOpen a file of type NBT, MCA and JSON.')
        self.openbutton.installEventFilter(ToolTipFilter(
            self.openbutton, 300, ToolTipPosition.BOTTOM))
        self.openbutton.setStyleSheet(
            'QPushButton {text-align:left;}')
        self.openbutton.setIcon(
            QIcon(f'img/appIcon/{self._parent_.Puretheme}/folder-open-fill.svg'))
        self.openbutton.iconPath = 'folder-open-fill.svg'
        # https://xkcb1.github.io/StructureViewerWebSite/
        self._parent_.changeIconList.append(self.openbutton)
        #
        self.aboutbutton = QPushButton()
        self.aboutbutton.setObjectName('ButtonMenuBar')
        self.aboutbutton.setText('发布说明')
        self.aboutbutton.setToolTip('发布说明(网页)\nRelease Notes(Web page)')
        self.aboutbutton.installEventFilter(ToolTipFilter(
            self.aboutbutton, 300, ToolTipPosition.BOTTOM))
        self.aboutbutton.clicked.connect(
            self.openWebSite)
        self.aboutbutton.setStyleSheet(
            'QPushButton {text-align:left;}')
        self.aboutbutton.setIcon(
            QIcon(f'img/appIcon/{self._parent_.Puretheme}/global-line.svg'))
        self.aboutbutton.iconPath = 'global-line.svg'
        self._parent_.changeIconList.append(self.aboutbutton)
        #
        self.doc = QPushButton()
        self.doc.setObjectName('ButtonMenuBar')
        self.doc.setText('文档')
        self.doc.setToolTip('文档 (网页)\nDocuments (Web pages)')
        self.doc.installEventFilter(ToolTipFilter(
            self.doc, 300, ToolTipPosition.BOTTOM))
        self.doc.setStyleSheet('QPushButton {text-align:left;}')
        self.doc.setIcon(
            QIcon(f'img/appIcon/{self._parent_.Puretheme}/question-fill.svg'))
        self.doc.iconPath = 'question-fill.svg'
        self._parent_.changeIconList.append(self.doc)
        #
        self.heart = QPushButton()
        self.heart.setObjectName('ButtonMenuBar')
        self.heart.setText('支持我们')
        self.heart.setToolTip('支持我们的项目 (网页)\nSupport our project (webpage)')
        self.heart.installEventFilter(ToolTipFilter(
            self.heart, 300, ToolTipPosition.BOTTOM))
        self.heart.setStyleSheet(
            'QPushButton {text-align:left;}')
        self.heart.setIcon(
            QIcon(f'img/appIcon/{self._parent_.Puretheme}/heart-3-fill.svg'))
        self.heart.iconPath = 'heart-3-fill.svg'
        self._parent_.changeIconList.append(self.heart)
        #
        self.bottomOption_layout = QGridLayout(self.bottomOption)
        self.bottomOption_layout.setSpacing(0)
        self.bottomOption_layout.addWidget(self.openbutton, 0, 0)
        self.bottomOption_layout.addWidget(self.aboutbutton, 0, 1)
        self.bottomOption_layout.addWidget(self.heart, 1, 1)
        self.bottomOption_layout.addWidget(self.doc, 1, 0)
        self.bottomOption_layout.setHorizontalSpacing(40)
        #
        self.initTopWidget()

    def openWebSite(self):
        QDesktopServices.openUrl(QUrl(self._parent_.url))

    def initTopWidget(self):
        self.toplayout = QGridLayout(self.topOption)
        self.topOption.setFixedHeight(130)
        self.toplayout.setHorizontalSpacing(40)
        self.toplayout.setVerticalSpacing(2)
        Label_1 = QLabel()
        Label_1.setText('打开文件')
        Label_1.setStyleSheet('color:gray;margin-left:3px;')
        #
        Label_2 = QLabel()
        Label_2.setText('最近打开的文件')
        Label_2.setStyleSheet('color:gray;margin-left:3px;')
        #
        self.toplayout.addWidget(Label_1, 0, 0)
        self.toplayout.addWidget(Label_2, 0, 1)
        #
        self.open_none = QPushButton()
        self.open_none.setText('空白 项目')
        self.open_none.setObjectName('ButtonMenuBar')
        self.open_none.setIcon(QIcon('img/main_3/White.png'))
        self.open_none.setStyleSheet('QPushButton {text-align:left;}')
        #
        self.open_nbt = QPushButton()
        self.open_nbt.setText('Nbt 文件')
        self.open_nbt.setObjectName('ButtonMenuBar')
        self.open_nbt.setIcon(QIcon('img/main_3/Nbt.png'))
        self.open_nbt.setStyleSheet('QPushButton {text-align:left;}')
        #
        self.open_mca = QPushButton()
        self.open_mca.setObjectName('ButtonMenuBar')
        self.open_mca.setText('Mca 文件')
        self.open_mca.setIcon(QIcon('img/main_3/TerrainMaker.png'))
        self.open_mca.setStyleSheet('QPushButton {text-align:left;}')
        #
        self.open_json = QPushButton()
        self.open_json.setText('Json 文件')
        self.open_json.setObjectName('ButtonMenuBar')
        self.open_json.setIcon(QIcon('img/main_3/javaCommand.png'))
        self.open_json.setStyleSheet('QPushButton {text-align:left;}')
        #
        self.open_mcfunction = QPushButton()
        self.open_mcfunction.setText('Mcfunction 文件')
        self.open_mcfunction.setObjectName('ButtonMenuBar')
        self.open_mcfunction.setIcon(QIcon('img/main_3/pakage.png'))
        self.open_mcfunction.setStyleSheet('QPushButton {text-align:left;}')
        #
        self.toplayout.addWidget(self.open_none, 1, 0)
        self.toplayout.addWidget(self.open_nbt, 2, 0)
        self.toplayout.addWidget(self.open_mca, 3, 0)
        self.toplayout.addWidget(self.open_json, 4, 0)
        #
        if self._parent_.recent == []:
            nofile = QLabel()
            nofile.setText('没有文件记录')
            nofile.setStyleSheet('color:gray;margin-left:3px;')
            self.toplayout.addWidget(nofile, 1, 1)
        else:
            for file in self._parent_.recent:
                pass


class PAboutWidget(QDialog):
    def __init__(self, parent=None, w=504, h=490):
        super().__init__(parent)
        self.window = parent
        self.w = w
        self.h = h
        self.setFixedSize(w, h)
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setWindowFlag(Qt.Dialog)
        # 设置圆角
        # 启用窗口透明背景
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.MainWidget = QWidget()
        self.MainLayout = QVBoxLayout(self)
        self.MainLayout.setContentsMargins(9, 9, 9, 9)
        self.MainLayout.addWidget(self.MainWidget)
        self.MainWidget.setObjectName('startPanel')
        #
        self.ThisLayout = QHBoxLayout(self.MainWidget)
        # 使用QGraphicsDropShadowEffect添加阴影
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setColor(QColor(0, 0, 0, 100))
        shadow.setBlurRadius(9)
        shadow.setOffset(0, 0)
        self.setGraphicsEffect(shadow)
        # uiInit
        self.uiInit()

    def uiInit(self):
        self.url = self.window.url
        self.license = 'GNU GPL-3.0'
        #
        icon = QPushButton()
        icon.resize(200, 200)
        icon.setFixedSize(200, 200)
        icon.setIcon(QIcon('./img/mcEarth_black_40.png'))
        icon.setIconSize(QSize(200, 200))
        icon.setStyleSheet(
            'background-color: rgba(0,0,0,0);border:0px !important;')
        #
        self.ThisLayout.addWidget(icon)
        TopLayout = QHBoxLayout()
        Title = QLabel('Structure studio 0.0.1')
        Title.setStyleSheet(
            'border: 0px;background-color: rgba(0,0,0,0);font-family:微软雅黑;font-size:30px;font-weight:bold;')
        TopLayout.addWidget(Title)
        # project面板
        project = QWidget()
        self.makeProject(project)
        #
        rightLayout = QVBoxLayout()
        rightLayout.setContentsMargins(5, 20, 5, 5)
        rightDiv = QTextBrowser()
        rightDiv.setText(f'''
<p><a>Website <a href="{self.url}">  {self.url}</a></p>
</a></p><p><a>License <a href="./license/EULA">  {self.license}</a></p>
<a style="color:gray;text-align: center;">©Copyright 2023-2024 XK(Xinkong) and LY(Lingyuan)</a>
        ''')
        rightDiv.setStyleSheet(
            'border: 0px;background-color: rgba(0,0,0,0);font-family:微软雅黑;')
        rightLayout.addLayout(TopLayout)
        rightLayout.addWidget(project)
        rightLayout.addWidget(rightDiv)
        self.ThisLayout.addLayout(rightLayout)

    def makeProject(self, projectWidget):
        projectLayout = QGridLayout(projectWidget)
        info = QLabel('FrameWorks , Libraries , Icons')
        projectLayout.setContentsMargins(10, 0, 10, 0)
        projectLayout.addWidget(info, 0, 0)
        # 1
        _project_pyqt5_ = QPushButton()
        _project_pyqt5_.setObjectName('ButtonMenuBar')
        _project_pyqt5_.setText('Qt (PyQt5)')
        _project_pyqt5_.setIcon(QIcon('img/Qt_logo_neon_2022.svg.png'))
        _project_pyqt5_.setStyleSheet('QPushButton {text-align:left;}')
        projectLayout.addWidget(_project_pyqt5_, 1, 0)

        # 2
        _project_Blender_ = QPushButton()
        _project_Blender_.setObjectName('ButtonMenuBar')
        _project_Blender_.setText('Blender UI (icon set)')
        _project_Blender_.setIcon(QIcon('img/blendericon27.png'))
        _project_Blender_.setStyleSheet('QPushButton {text-align:left;}')
        projectLayout.addWidget(_project_Blender_, 1, 1)

        # 3
        _project_VTK_ = QPushButton()
        _project_VTK_.setObjectName('ButtonMenuBar')
        _project_VTK_.setText('VTK (3D view)')
        _project_VTK_.setIcon(QIcon('img/vtk_logo-main1.png'))
        _project_VTK_.setStyleSheet('QPushButton {text-align:left;}')
        projectLayout.addWidget(_project_VTK_, 2, 0)

        # 4
        _project_Python_ = QPushButton()
        _project_Python_.setObjectName('ButtonMenuBar')
        _project_Python_.setText('Python 3.11')
        _project_Python_.setIcon(
            QIcon('img/fileTypeIcon/high-contrast/py.svg'))
        _project_Python_.setStyleSheet('QPushButton {text-align:left;}')
        projectLayout.addWidget(_project_Python_, 2, 1)

        # 5
        _project_Minecraft_ = QPushButton()
        _project_Minecraft_.setObjectName('ButtonMenuBar')
        _project_Minecraft_.setText('Minecraft Asset')
        _project_Minecraft_.setIcon(
            QIcon('img/Minecraft.png'))
        _project_Minecraft_.setStyleSheet('QPushButton {text-align:left;}')
        projectLayout.addWidget(_project_Minecraft_, 3, 0)

        # 6
        _project_PureSV_ = QPushButton()
        _project_PureSV_.setObjectName('ButtonMenuBar')
        _project_PureSV_.setText('Structure Tools')
        _project_PureSV_.setIcon(
            QIcon('img/appIcon_2.png'))
        _project_PureSV_.setStyleSheet('QPushButton {text-align:left;}')
        projectLayout.addWidget(_project_PureSV_, 3, 1)
