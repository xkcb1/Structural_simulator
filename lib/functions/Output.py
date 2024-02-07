from lib.Widgets.comboBox import PureLabel
from lib.base import *


class OutPutWidget(QWidget):
    def __init__(self, parent=None, window=None, openPath=''):
        super(OutPutWidget, self).__init__()
        self._parent_ = parent
        self._window_ = window
        self.mainWidget = self
        self._parent_.output_class = self
        mainLayout = QVBoxLayout(self)
        mainLayout.setContentsMargins(0, 0, 0, 0)
        self._mainwidget_ = QWidget()
        mainLayout.addWidget(self._mainwidget_)
        # set main widget
        self._mainwidget_.setObjectName('MainWidget')
        self.Mainlayout = QVBoxLayout(self._mainwidget_)
        self.Mainlayout.setContentsMargins(0, 4, 0, 0)
        #

        outPutLayout = self.Mainlayout
        outPutLayout.setSpacing(0)
        outPutTopWidget = QWidget()
        outPutTopWidget.setFixedHeight(25)
        outPutLayout.addWidget(outPutTopWidget)
        outPutTopWidget.setStyleSheet(
            '#output_main{border-radius:5px !important;}')
        # set the top menu
        outPutTopWidget_layout = QHBoxLayout(outPutTopWidget)
        outPutTopWidget_layout.setContentsMargins(5, 0, 5, 0)
        outPutTopWidget_layout.setSpacing(0)
        ClearButton = QPushButton()
        ClearButton.setFixedHeight(20)
        ClearButton.setText('清除')
        ClearButton.setIcon(QIcon('img/delete-bin-2-fill.svg'))
        ClearButton.clicked.connect(self.OutPut_Clear)
        ClearButton.setStyleSheet('''*{border-top-right-radius:0px;
                           border-bottom-right-radius:0px;
                           }''')
        #
        downloadButton = QPushButton()
        downloadButton.setFixedHeight(20)
        downloadButton.setText('下载')
        downloadButton.setIcon(QIcon('img/download-2-fill.svg'))
        downloadButton.setStyleSheet('''*{border-radius:0px;
                            border-left:0px;
                           }''')
        #
        countButton = QPushButton()
        countButton.setFixedHeight(20)
        countButton.setText('消息 : 0')
        countButton.setIcon(QIcon('img/message-2-fill.svg'))
        countButton.setStyleSheet('''*{border-top-left-radius:0px;
                        border-bottom-left-radius:0px;
                        border-left:0px;
                           }''')
        #
        downloadButton.clicked.connect(print)
        outPutTopWidget_layout.addWidget(ClearButton)
        outPutTopWidget_layout.addWidget(downloadButton)
        outPutTopWidget_layout.addWidget(countButton)
        outPutTopWidget_layout.addStretch(9999)
        #
        outPut_mainWidget = QWidget()
        outPut_mainWidget.setObjectName('output_main')
        outPut_mainWidget.setStyleSheet(
            '#output_main{border-radius:5px !important;}')
        outPut_layout = QVBoxLayout(outPut_mainWidget)
        outPut_layout.setContentsMargins(5, 0, 5, 5)
        outPutLayout.addWidget(outPut_mainWidget)
        # scroll area
        layout_scroll = QVBoxLayout()
        self.OutPut_layout_scroll = layout_scroll
        self.OutPut_layout_scroll.count_ = 0
        self.OutPut_layout_scroll.countButton = countButton
        config = QScrollArea()
        config.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        config.setObjectName('OutPut')

        layout_scroll.setContentsMargins(0, 2, 0, 1)
        MainWidgetThis = QWidget()
        MainWidgetThis.setObjectName('OutPut')
        MainWidgetThis.setLayout(layout_scroll)
        MainWidgetThis.setContentsMargins(0, 0, 0, 0)
        config.setWidget(MainWidgetThis)
        config.setContentsMargins(0, 0, 0, 0)
        config.setWidgetResizable(True)
        config.widgetResizable()
        outPut_layout.addWidget(config)
        outPut_layout.setSpacing(0)
        # outPut_layout.addStretch(99999)
        self.OutPut_Send('Application is Beta Version',
                         type='warning', color='auto', widget=0)
        # self.OutPut_Send('App Start in : '+str(datetime.datetime.now()))
        self.OutPut_Send('System : '+platform.system()+' ' +
                         platform.version()+' '+platform.release(), 'info', 'auto', 0)
        self.OutPut_Send(
            'Python : '+platform.python_version(), 'info', 'auto', 0)
        # self.OutPut_Send('Structure Studio : '+self.version)

        self.outPut_layout = outPut_layout
        self.OutPut_layout_scroll.addStretch(9999)
        self.OutPut_layout_scroll.setSpacing(0)
        # 绑定信号singal
        self.OutPut_Singal = OutPut()
        self.OutPut_Singal.OutPutSingal.connect(
            self.OutPut_Send)
        self._parent_.OutPut_Singal = self.OutPut_Singal
        self._parent_.OutPut_Singal.OutPutSingal = self.OutPut_Singal.OutPutSingal

        self._parent_.OutPutList[str(self._parent_.OutPutListCount)] = self
        self._parent_.OutPutListCount += 1

    def OutPut_Send(self, text, type='info', color="auto", widget=0):
        '''
        向输出窗口发送消息
        '''
        Info = QWidget()
        Info.setObjectName('Info_widget')
        Info.setStyleSheet(
            '''#Info_widget {
                background-color:rgba(0,0,0,0);
                border:0px;
                border-radius:1px;
                border-bottom:1px solid rgba(175,175,175,0.15);
                }
            #Info_widget:hover {
                background-color:rgba(50, 150, 255,0.25);
                }''')
        if type == 'info':
            Icon = QIcon('./img/info.svg')
        elif type == 'warning':
            Icon = QIcon('./img/warning.svg')
        info_layout = QHBoxLayout(Info)
        info_layout.setContentsMargins(3, 0, 0, 0)
        Icon_Action = PureLabel()
        Icon_Action.setIcon(Icon)
        Icon_Action.setFixedWidth(16)
        info_layout.addWidget(Icon_Action)
        if widget == 0:
            Info.setFixedHeight(20)
            Text = QLineEdit()
            Text.setFixedHeight(20)
            Text.setText(str(text))
            Text.setReadOnly(1)
            Text.setCursorPosition(0)
            if color == 'auto':
                Text.setStyleSheet(
                    'background-color:rgba(0,0,0,0);border:0px !important;font-size:10px !important;font-weight:lighter;color:auto;padding:0px;')
            else:
                Text.setStyleSheet(
                    f'background-color:rgba(0,0,0,0);border:0px !important;color:{color};font-size:10px !important;font-weight:lighter;padding:0px;')
        else:
            Text = QTextBrowser()
            Text.setText(str(text))
            Text.setReadOnly(1)
            Text.setMaximumHeight(80)
            if color == 'auto':
                Text.setStyleSheet(
                    'font-size:10px !important;font-weight:lighter;color:auto;padding:0px;')
            else:
                Text.setStyleSheet(
                    f'color:{color};font-size:10px !important;font-weight:lighter;padding:0px;')
        info_layout.addWidget(Text)
        info_layout.setSpacing(0)
        self.OutPut_layout_scroll.insertWidget(
            self.OutPut_layout_scroll.count() - 1, Info)
        self.OutPut_layout_scroll.count_ += 1
        self.OutPut_layout_scroll.countButton.setText(
            '消息 : '+str(self.OutPut_layout_scroll.count_))

    def OutPut_Clear(self):
        '''
        清除输出窗口的内容
        '''
        self.OutPut_layout_scroll.count_ = 0
        self.OutPut_layout_scroll.countButton.setText('消息 : 0')
        item_list = list(
            range(self.OutPut_layout_scroll.count()))
        item_list.reverse()
        # 倒序删除,避免影响布局顺序
        for i in item_list:
            item = self.OutPut_layout_scroll.itemAt(i)
            self.OutPut_layout_scroll.removeItem(item)
            try:
                item.deleteLater()
            except:
                pass
            try:
                item.widget().deleteLater()
            except:
                pass
