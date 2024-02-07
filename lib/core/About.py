from lib.base import *
from qframelesswindow import FramelessWindow, StandardTitleBar
from qframelesswindow import AcrylicWindow


class AboutWidget(QWidget):
    def __init__(self, window):
        super(AboutWidget, self).__init__()
        thisLayout = QHBoxLayout(self)
        thisLayout.setContentsMargins(0, 20, 0, 30)
        thisLayout.setSpacing(10)
        self.url = 'www.McEearth.com'
        #
        icon = QPushButton()
        icon.resize(200, 200)
        icon.setFixedSize(200, 200)
        icon.setIcon(QIcon('./img/mcEarth_2.png'))
        icon.setIconSize(QSize(200, 200))
        icon.setStyleSheet(
            'background-color: rgba(0,0,0,0);border:0px !important;')
        #
        thisLayout.addWidget(icon)
        #
        rightDiv = QTextBrowser()
        rightDiv.setText(f'''
        <h1 style='font-weight:bold'>Structure Viewer 0.0.4 beta</h1>
        <p><a>It is a software used to Edit the .Nbt file. It free for every one to use ,</a><a>This software has nothing to do with Mojang Studios and MoJang AB. This software is an independent Minecraft gameplay extension and production tool. 
</a></p><p><a>our website <a href="{self.url}">  {self.url}</a></p>
<a style="color:gray;text-align: center;">©Copyright 2023 XK(Xinkong) | LY(Lingyuan)</a>
        ''')
        rightDiv.setStyleSheet(
            'border: 0px;background-color: rgba(0,0,0,0);margin-top:30px;font-family:微软雅黑;')
        thisLayout.addWidget(rightDiv)


class CustomTitleBar(StandardTitleBar):
    """ Custom title bar """

    def __init__(self, parent):
        super().__init__(parent)

        # customize the style of title bar button
        self.minBtn.setHoverColor(Qt.white)
        self.minBtn.setHoverBackgroundColor(QColor(0, 100, 182))
        self.minBtn.setPressedColor(Qt.white)
        self.minBtn.setPressedBackgroundColor(QColor(54, 57, 65))

        # use qss to customize title bar button
        self.maxBtn.setStyleSheet("""
            TitleBarButton {
                qproperty-hoverColor: white;
                qproperty-hoverBackgroundColor: rgb(0, 100, 182);
                qproperty-pressedColor: white;
                qproperty-pressedBackgroundColor: rgb(54, 57, 65);
            }
        """)


class AboutWindow(AcrylicWindow):

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setWindowTitle("Acrylic Window")
        self.setTitleBar(CustomTitleBar(self))
        self.windowEffect.setAcrylicEffect(self.winId(), "96979910")
        self.titleBar.setTitle('About Structure Viewer')
        xlayout = QVBoxLayout()
        xlayout.setContentsMargins(0, 30, 0, 0)
        self.mainwidget = QWidget()
        self.setLayout(xlayout)
        xlayout.addWidget(self.mainwidget)
