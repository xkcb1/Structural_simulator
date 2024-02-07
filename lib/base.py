from lib.NbtTree import LastNBTFile
import lib.nbtToMca_nbtlib as nbtToMca_nbtlib
from lib.mca import *
import nbtlib
import platform
from vtkmodules.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor
from vtk import *
import json
import time
import psutil
import mimetypes
import numpy as np
import os
import vtk
import sys
from PyQt5 import QtCore, QtGui
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import PyQt5.QtWidgets as QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtWebEngineWidgets import *
import getpass
import traceback
import binascii
from IPython.lib.deepreload import reload
import typing
from lib.Widgets.tooltip import *
#
if platform.system() == 'Windows':
    from win32mica import ApplyMica, MicaTheme, MicaStyle
    import win32mica

# get all file types from iconLib
iconType = ['3g2', '3ga', '3gp', '7z', 'aa', 'aac', 'ac', 'accdb', 'accdt', 'ace', 'adn', 'ai', 'aif', 'aifc', 'aiff', 'ait', 'amr', 'ani', 'apk', 'app', 'applescript', 'asax', 'asc', 'ascx', 'asf', 'ash', 'ashx', 'asm', 'asmx', 'asp', 'aspx', 'asx', 'au', 'aup', 'avi', 'axd', 'aze', 'bak', 'bash', 'bat', 'bin', 'blank', 'bmp', 'bowerrc', 'bpg', 'browser', 'bz2', 'bzempty', 'c', 'cab', 'cad', 'caf', 'cal', 'cd', 'cdda', 'cer', 'cfg', 'cfm', 'cfml', 'cgi', 'chm', 'class', 'cmd', 'code-workspace', 'codekit', 'codekit3', 'coffee', 'coffeelintignore', 'com', 'compile', 'conf', 'config', 'cpp', 'cptx', 'cr2', 'crdownload', 'crt', 'crypt', 'cs', 'csh', 'cson', 'csproj', 'css', 'csv', 'cue', 'cur', 'dart', 'dat', 'data', 'db', 'dbf', 'deb', 'default', 'dgn', 'dist', 'diz', 'dll', 'dmg', 'dng', 'doc', 'docb', 'docm', 'docx', 'dot', 'dotm', 'dotx', 'download', 'dpj', 'dsn', 'dst', 'ds_store', 'dtd', 'dwg', 'dxf', 'editorconfig', 'el', 'elf', 'eml', 'enc', 'eot', 'eps', 'epub', 'eslintignore', 'exe', 'f4v', 'fax', 'fb2', 'fla', 'flac', 'flv', 'fnt', 'folder-base-open', 'folder-base', 'folder-database-open', 'folder-database', 'fon', 'gadget', 'gdp', 'gem', 'gif', 'gitattributes', 'gitignore', 'go', 'gpg', 'gpl', 'gradle', 'gz', 'h', 'handlebars', 'hbs', 'heic', 'hlp', 'hs', 'hsl', 'htm', 'html', 'ibooks', 'icma', 'icml', 'icns', 'ico', 'ics', 'idx', 'iff', 'ifo', 'image', 'img', 'iml', 'in', 'inc', 'indd', 'inf', 'info', 'ini', 'inv', 'iso', 'j2', 'jar', 'java', 'jpe', 'jpeg', 'jpg', 'js', 'json', 'jsp', 'jsx', 'key', 'kf8', 'kit', 'kmk', 'ksh', 'kt', 'kts', 'kup', 'less', 'lex', 'licx', 'lisp', 'list', 'lit', 'lnk', 'lock', 'log', 'lua',
            'm', 'm2v', 'm3u', 'm3u8', 'm4', 'm4a', 'm4r', 'm4v', 'map', 'master', 'mc', 'md', 'mdb', 'mdf', 'me', 'mi', 'mid', 'midi', 'mk', 'mkv', 'mm', 'mng', 'mo', 'mobi', 'mod', 'mov', 'mp2', 'mp3', 'mp4', 'mpa', 'mpd', 'mpe', 'mpeg', 'mpg', 'mpga', 'mpp', 'mpt', 'msg', 'msi', 'msu', 'nef', 'nes', 'nfo', 'nix', 'npmignore', 'ocx', 'odb', 'ods', 'odt', 'ogg', 'ogv', 'one', 'ost', 'otf', 'ott', 'ova', 'ovf', 'p12', 'p7b', 'pages', 'part', 'partial', 'pbix', 'pcd', 'pdb', 'pdf', 'pem', 'pfx', 'pgp', 'ph', 'phar', 'php', 'pid', 'pkg', 'pl', 'plist', 'pm', 'png', 'po', 'pom', 'pot', 'potx', 'ppk', 'pps', 'ppsx', 'ppt', 'pptm', 'pptx', 'prop', 'ps', 'ps1', 'psd', 'psp', 'pst', 'pub', 'py', 'pyc', 'pyw', 'qt', 'ra', 'ram', 'rar', 'raw', 'rb', 'rdf', 'rdl', 'reg', 'resx', 'retry', 'rm', 'rom', 'rpm', 'rpt', 'rsa', 'rss', 'rst', 'rtf', 'ru', 'rub', 'sass', 'save', 'scss', 'sdf', 'sed', 'sesx', 'sh', 'sit', 'sitemap', 'sketch', 'skin', 'sldm', 'sldx', 'sln', 'sol', 'sphinx', 'sql', 'sqlite', 'srt', 'step', 'stl', 'sub', 'svg', 'swd', 'swf', 'swift', 'swp', 'sys', 'tar', 'tax', 'tcsh', 'tex', 'tfignore', 'tga', 'tgz', 'tif', 'tiff', 'tmp', 'tmx', 'torrent', 'tpl', 'ts', 'tsv', 'tsx', 'ttf', 'twig', 'txt', 'udf', 'vb', 'vbproj', 'vbs', 'vcd', 'vcf', 'vcs', 'vdi', 'vdx', 'vmdk', 'vob', 'vox', 'vscodeignore', 'vsd', 'vss', 'vst', 'vsx', 'vtx', 'war', 'wav', 'wbk', 'webinfo', 'webm', 'webp', 'wma', 'wmf', 'wmv', 'woff', 'woff2', 'wpd', 'wps', 'wsf', 'xaml', 'xcf', 'xcodeproj', 'xfl', 'xlb', 'xlc', 'xlm', 'xls', 'xlsb', 'xlsm', 'xlsx', 'xlt', 'xltm', 'xltx', 'xml', 'xpi', 'xps', 'xrb', 'xsd', 'xsl', 'xspf', 'xz', 'yaml', 'yml', 'z', 'zip', 'zsh']

################################################################


class Slider:
    def __init__(self, a, b, step, value, function):
        self.a = a
        self.b = b
        self.value = value
        self.step = step
        self.function = function


class Button:
    def __init__(self, text, function, Icon=None):
        self.text = text
        self.function = function
        self.Icon = Icon


class Info:
    def __init__(self, text):
        self.text = text


def get_file_path(root_path, file_list, dir_list):
    # 获取该目录下所有的文件名称和目录名称
    dir_or_files = os.listdir(root_path)
    for dir_file in dir_or_files:
        # 获取目录或者文件的路径
        dir_file_path = os.path.join(root_path, dir_file)
        # 判断该路径为文件还是路径
        if os.path.isdir(dir_file_path):
            dir_list.append(dir_file_path)
            # 递归获取所有文件和目录的路径
            # get_file_path(dir_file_path,file_list,dir_list)
        else:
            file_list.append(dir_file_path)


def get_ALL_file_count(root_path, file_list_count, dir_list_count):
    # 获取该目录下所有的文件名称和目录名称
    dir_or_files = os.listdir(root_path)
    for dir_file in dir_or_files:
        # 获取目录或者文件的路径
        dir_file_path = os.path.join(root_path, dir_file)
        # 判断该路径为文件还是路径
        if os.path.isdir(dir_file_path):
            dir_list_count.append(dir_file_path)
            # 递归获取所有文件和目录的路径
            get_ALL_file_count(dir_file_path, file_list_count, dir_list_count)
        else:
            file_list_count.append(dir_file_path)
################################################################


################################################################################################
key_map = {
    "0": 0x30, "1": 0x31, "2": 0x32, "3": 0x33, "4": 0x34, "5": 0x35, "6": 0x36, "7": 0x37, "8": 0x38, "9": 0x39,
    'F1': 112, 'F2': 113, 'F3': 114, 'F4': 115, 'F5': 116, 'F6': 117, 'F7': 118, 'F8': 119,
    'F9': 120, 'F10': 121, 'F11': 122, 'F12': 123, 'F13': 124, 'F14': 125, 'F15': 126, 'F16': 127,
    "A": 65, "B": 66, "C": 67, "D": 68, "E": 69, "F": 70, "G": 71, "H": 72, "I": 73, "J": 74,
    "K": 75, "L": 76, "M": 77, "N": 78, "O": 79, "P": 80, "Q": 81, "R": 82, "S": 83, "T": 84,
    "U": 85, "V": 86, "W": 87, "X": 88, "Y": 89, "Z": 90,
    'BACKSPACE': 8, 'TAB': 9, 'TABLE': 9, 'CLEAR': 12,
    'ENTER': 13, 'SHIFT': 16, 'CTRL': 17,
    'CONTROL': 17, 'ALT': 18, 'ALTER': 18, 'PAUSE': 19, 'BREAK': 19, 'CAPSLK': 20, 'CAPSLOCK': 20, 'ESC': 27,
    ' ': 32, 'SPACEBAR': 32, 'PGUP': 33, 'PAGEUP': 33, 'PGDN': 34, 'PAGEDOWN': 34, 'END': 35, 'HOME': 36,
    'LEFT': 37, 'UP': 38, 'RIGHT': 39, 'DOWN': 40, 'SELECT': 41, 'PRTSC': 42, 'PRINTSCREEN': 42, 'SYSRQ': 42,
    'SYSTEMREQUEST': 42, 'EXECUTE': 43, 'SNAPSHOT': 44, 'INSERT': 45, 'DELETE': 46, 'HELP': 47, 'WIN': 91,
    'WINDOWS': 91, 'NMLK': 144,
    '.': 0xBE,
    'NUMLK': 144, 'NUMLOCK': 144, 'SCRLK': 145,
    '[': 219, ']': 221, '+': 107, '-': 109}

################################################################


class FileSelector(QFileDialog):
    def __init__(self, title="Select file", type="All Files (*)"):
        super().__init__()
        self.title = title
        self.type = type
        self.window().setWindowIcon(QIcon("./img/open_s.png"))
        self.selectFile()

    def selectFile(self):
        options = QFileDialog.Options()
        fileName, _ = QFileDialog.getOpenFileName(
            self, self.title, "", self.type, options=options)

        self.fileName = fileName


class StyleReader:
    @staticmethod
    def readQSS(style):
        with open(style, 'r', encoding='utf-8') as f:
            return f.read()


################################################################
'''
to Image module
'''


class PSlider(QFrame):
    def __init__(self, name: str, function, min=0, max=255, step=1, value=0):
        super().__init__()
        self.setFixedHeight(26)
        self.layout = QHBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(5)
        self.name = name
        self.min = min
        self.max = max
        self.step = step
        self.value = value
        self.function = function
        # Name
        self.NAME = QLabel(self.name)
        self.NAME.setStyleSheet('text-align:center;')
        self.NAME.setAlignment(Qt.AlignCenter)
        if self.name != '':
            self.NAME.setFixedWidth(50)
        else:
            self.NAME.setFixedWidth(0)

        self.setObjectName('PSlider')
        self.setStyleSheet(
            '''
            QFrame {
                background-color:rgba(175,175,175,0.15);
            }
            QLabel {
                background-color:rgba(0,0,0,0);
            }
            QSlider {
                background-color:rgba(0,0,0,0);
            }
            QSlider::handle:horizontal {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #c4c4c4, stop:1 #9f9f9f);
                border: 1px solid #6c6c6c;
                width: 14px;
                margin: -2px 0; /* handle is placed by default on the contents rect of the groove. Expand outside the groove */
                border-radius: 4px;
            }
        ''')
        #
        self.Slider = QSlider(Qt.Horizontal)
        self.Slider.setObjectName('Slider')

        self.Slider.setMaximum(self.max)
        self.Slider.setMinimum(self.min)
        self.Slider.setValue(self.value)
        self.Slider.setSingleStep(self.step)
        self.Slider.setTickInterval(34)
        self.Slider.setTickPosition(QSlider.TicksBelow)
        #
        self.value = QLabel(str(value))
        self.value.setFixedWidth(30)
        self.value.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.NAME)
        self.layout.addWidget(self.Slider)
        self.layout.addWidget(self.value)
        #
        self.Slider.valueChanged.connect(self.valueChange)

    def valueChange(self):
        self.value.setText(str(self.Slider.value()))
        self.function(self.name, self.Slider.value())


################################################################
'''
base settings
'''


class TabBar(QtWidgets.QTabBar):
    def tabSizeHint(self, index):
        s = QtWidgets.QTabBar.tabSizeHint(self, index)
        s.transpose()
        return s

    def paintEvent(self, event):
        painter = QtWidgets.QStylePainter(self)
        opt = QtWidgets.QStyleOptionTab()

        for i in range(self.count()):
            self.initStyleOption(opt, i)
            painter.drawControl(QtWidgets.QStyle.CE_TabBarTabShape, opt)
            painter.save()

            s = opt.rect.size()
            s.transpose()
            r = QtCore.QRect(QtCore.QPoint(), s)
            r.moveCenter(opt.rect.center())
            opt.rect = r

            c = self.tabRect(i).center()
            painter.translate(c)
            painter.rotate(90)
            painter.translate(-c)
            painter.drawControl(QtWidgets.QStyle.CE_TabBarTabLabel, opt)
            painter.restore()


class PureTabWidget(QtWidgets.QTabWidget):
    def __init__(self, *args, **kwargs):
        QtWidgets.QTabWidget.__init__(self, *args, **kwargs)
        self.setTabBar(TabBar(self))
        self.setTabPosition(QtWidgets.QTabWidget.West)


class ProxyStyle(QtWidgets.QProxyStyle):
    def drawControl(self, element, opt, painter, widget):
        if element == QtWidgets.QStyle.CE_TabBarTabLabel:
            ic = self.pixelMetric(QtWidgets.QStyle.PM_TabBarIconSize)
            r = QtCore.QRect(opt.rect)
            w = 0 if opt.icon.isNull() else opt.rect.width() + \
                self.pixelMetric(QtWidgets.QStyle.PM_TabBarIconSize)
            r.setHeight(opt.fontMetrics.width(opt.text) + w) + 16
            r.moveBottom(opt.rect.bottom())
            opt.rect = r
        QtWidgets.QProxyStyle.drawControl(self, element, opt, painter, widget)


################################################################
'''
to main application
'''


class StyleReader:
    @staticmethod
    def readQSS(style):
        with open(style, 'r', encoding='utf-8') as f:
            return f.read()


########################################################################
'''
VIEWER APP CLASS
'''


class NbtToMcaError:
    def __init__(self, errorStr):
        self.text = errorStr


def NoneFunction(*args):
    pass


'''
MORE WIDGET 2023/9/28
'''


class SpinComBox(QWidget):
    def __init__(self, value: list = []):
        super(SpinComBox, self).__init__()
        self.value = value
        # set widget properties
        self.MainWidget = QWidget()
        self.MainLayout = QHBoxLayout(self)
        self.MainLayout.setContentsMargins(0, 0, 0, 0)
        self.MainLayout.addWidget(self.MainWidget)
        self.MainWidget.setObjectName('SpinComBoxMain')
        self.MainWidget.setStyleSheet('''
#SpinComBoxMain {
    border: 1px solid red;
    border-radius:4px;
    }
                                      ''')

        self.setFixedHeight(22)
        self.Layout = QHBoxLayout(self.MainWidget)
        self.Layout.setContentsMargins(1, 1, 1, 1)
        self.Layout.setSpacing(0)
        self.setMinimumWidth(70)
        self.comboxWidget = QWidget()
        self.comboxLayout = QVBoxLayout(self.comboxWidget)
        self.comboxLayout.setContentsMargins(1, 1, 1, 1)
        self.ComBox = QComboBox()
        self.ComBox.setFixedHeight(16)
        self.comboxLayout.addWidget(self.ComBox)
        self.comboxWidget.setFixedHeight(16)
        self.ComBox.setStyleSheet(
            'border-radius:0px;border:0px;margin-bottom:1px !important;')
        self.ButtonWidget = QWidget()
        self.ButtonWidget.setFixedWidth(16)
        self.ButtonWidget.setStyleSheet('''
QPushButton {
    border-radius:0px !important;
}
''')
        self.ButtonLayout = QVBoxLayout(self.ButtonWidget)
        self.ButtonLayout.setContentsMargins(0, 0, 0, 0)
        self.ButtonLayout.setSpacing(0)
        self.Last = QPushButton()
        self.Last.setText('a')
        self.Next = QPushButton()
        # add buttons to layout
        self.ButtonLayout.addWidget(self.Last)
        self.ButtonLayout.addWidget(self.Next)
        # set layout
        self.Layout.addWidget(self.ComBox)
        self.Layout.addWidget(self.ButtonWidget)
        #
        self.ComBox.addItems(self.value)

    def setValue(self, value: list = []) -> None:
        for index in range(len(self.value)):
            self.ComBox.removeItem(index)
        self.value = value
        self.ComBox.addItems(self.value)


#####################################################################
# from Structure Studio
#####################################################################


class Vline(QFrame):
    def __init__(self, width: int = 1):
        super(Vline, self).__init__()
        self.setFixedWidth(width)
        self.setStyleSheet(
            'background-color:rgba(175,175,175,0.3); margin-bottom:2px;margin-top:2px;')


class Hline(QFrame):
    def __init__(self, height: int = 1):
        super(Hline, self).__init__()
        self.setFixedHeight(height)
        self.setFrameShape(QFrame.HLine)  # 设置框架为横线
        self.setFrameShadow(QFrame.Sunken)
        self.setObjectName('Hline')


class _Thread_(QThread):   # 创建线程类
    def __init__(self, func, argvs=None, parent: QMainWindow = None):
        super(_Thread_, self).__init__()
        self.parent = parent
        self.func = func
        self.argvs = argvs
        # self.finished.connect(self.deleteLater)

    def run(self):     # 重写run()方法
        if self.argvs == None:
            self.func()
        else:
            self.func(self.argvs)
        return
##########################################################################################################
#
#
##########################################################################################################


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
    '''Change Theme'''
    # 定义一种信号,用来传递model文件的path
    changeSingal = pyqtSignal(str)


class OutPut(QObject):
    '''OutPut'''
    # 定义一种信号,用来传递model文件的path
    OutPutSingal = pyqtSignal(str, str, str, int)


class NBT_LIST_ADD(QObject):
    '''NBT_LIST_ADD'''
    AddListSingal = pyqtSignal(dict)


class MouseFilter(QObject):
    def __init__(self, vtk_widget):
        super().__init__()
        self.vtk_widget = vtk_widget

    def eventFilter(self, obj, event):
        if event.type() == QEvent.MouseButtonPress and event.button() == Qt.RightButton:
            self.vtk_widget.onRightButtonPress()
        elif event.type() == QEvent.MouseMove:
            self.vtk_widget.onMouseMove()

        return super().eventFilter(obj, event)

        ##################################################################################
