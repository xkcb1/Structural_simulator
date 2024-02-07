from lib.Widgets.console import JupyterConsoleWidget
from lib.Widgets.terminal import Pureterminal
from lib.base import *


class Console(QWidget):
    def __init__(self, parent=None, window=None, openPath=''):
        super(Console, self).__init__()
        self._parent_ = parent
        self._window_ = window
        # start
        mainLayout = QVBoxLayout(self)
        mainLayout.setContentsMargins(0, 0, 0, 0)
        self._mainwidget_ = QWidget()
        mainLayout.addWidget(self._mainwidget_)
        # set main widget
        self._mainwidget_.setObjectName('MainWidget')
        #
        self.Mainlayout = QVBoxLayout(self._mainwidget_)
        self.Mainlayout.setContentsMargins(0, 0, 0, 5)
        self.Mainlayout.setSpacing(0)
        #
        self.console = Pureterminal()
        self.console.console_text.setStyleSheet(
            'border:0px !important;')
        #
        self.bottomWidget = QWidget()
        self.bottomWidget.setFixedHeight(15)
        self.bottomWidgetLayout = QHBoxLayout(self.bottomWidget)
        self.bottomWidgetLayout.setContentsMargins(5, 0, 5, 0)
        self.bottomWidgetLayout.setSpacing(15)
        #
        self.Mainlayout.addWidget(self.console)
        self.Mainlayout.addWidget(self.bottomWidget)
        #
        if sys.platform.startswith('win'):
            self.TerminalCommand = 'cmd'
        elif sys.platform.startswith('darwin'):
            self.TerminalCommand = 'open -a Terminal'
        elif sys.platform.startswith('linux'):
            self.TerminalCommand = "gnome-termina"
        _platform_ = QLabel()
        _platform_Version_ = QLabel()
        UseTerminal = QLabel()
        #
        python_version_info = sys.version_info
        _platform_.setText(
            platform.system() + ' ' + platform.version())
        _platform_Version_.setText('python '+str(python_version_info.major) +
                                   "."+str(python_version_info.minor) +
                                   "." + str(python_version_info.micro))
        UseTerminal.setText("Terminal : "+self.TerminalCommand)
        self.bottomWidgetLayout.addWidget(_platform_)
        self.bottomWidgetLayout.addWidget(_platform_Version_)
        self.bottomWidgetLayout.addStretch(9999)
        self.bottomWidgetLayout.addWidget(UseTerminal)
