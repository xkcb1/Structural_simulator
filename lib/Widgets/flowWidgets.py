# coding:utf-8
import mimetypes
import os
from PyQt5 import QtCore, QtGui
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import PyQt5.QtWidgets as QtWidgets
from PyQt5.QtCore import *
from lib.Widgets.tooltip import *
from lib.Widgets.menu import PureRoundedBorderMenu

# 流动控件和布局
iconType = ['3g2', '3ga', '3gp', '7z', 'aa', 'aac', 'ac', 'accdb', 'accdt', 'ace', 'adn', 'ai', 'aif', 'aifc', 'aiff', 'ait', 'amr', 'ani', 'apk', 'app', 'applescript', 'asax', 'asc', 'ascx', 'asf', 'ash', 'ashx', 'asm', 'asmx', 'asp', 'aspx', 'asx', 'au', 'aup', 'avi', 'axd', 'aze', 'bak', 'bash', 'bat', 'bin', 'blank', 'bmp', 'bowerrc', 'bpg', 'browser', 'bz2', 'bzempty', 'c', 'cab', 'cad', 'caf', 'cal', 'cd', 'cdda', 'cer', 'cfg', 'cfm', 'cfml', 'cgi', 'chm', 'class', 'cmd', 'code-workspace', 'codekit', 'codekit3', 'coffee', 'coffeelintignore', 'com', 'compile', 'conf', 'config', 'cpp', 'cptx', 'cr2', 'crdownload', 'crt', 'crypt', 'cs', 'csh', 'cson', 'csproj', 'css', 'csv', 'cue', 'cur', 'dart', 'dat', 'data', 'db', 'dbf', 'deb', 'default', 'dgn', 'dist', 'diz', 'dll', 'dmg', 'dng', 'doc', 'docb', 'docm', 'docx', 'dot', 'dotm', 'dotx', 'download', 'dpj', 'dsn', 'dst', 'ds_store', 'dtd', 'dwg', 'dxf', 'editorconfig', 'el', 'elf', 'eml', 'enc', 'eot', 'eps', 'epub', 'eslintignore', 'exe', 'f4v', 'fax', 'fb2', 'fla', 'flac', 'flv', 'fnt', 'folder-base-open', 'folder-base', 'folder-database-open', 'folder-database', 'fon', 'gadget', 'gdp', 'gem', 'gif', 'gitattributes', 'gitignore', 'go', 'gpg', 'gpl', 'gradle', 'gz', 'h', 'handlebars', 'hbs', 'heic', 'hlp', 'hs', 'hsl', 'htm', 'html', 'ibooks', 'icma', 'icml', 'icns', 'ico', 'ics', 'idx', 'iff', 'ifo', 'image', 'img', 'iml', 'in', 'inc', 'indd', 'inf', 'info', 'ini', 'inv', 'iso', 'j2', 'jar', 'java', 'jpe', 'jpeg', 'jpg', 'js', 'json', 'jsp', 'jsx', 'key', 'kf8', 'kit', 'kmk', 'ksh', 'kt', 'kts', 'kup', 'less', 'lex', 'licx', 'lisp', 'list', 'lit', 'lnk', 'lock', 'log', 'lua',
            'm', 'm2v', 'm3u', 'm3u8', 'm4', 'm4a', 'm4r', 'm4v', 'map', 'master', 'mc', 'md', 'mdb', 'mdf', 'me', 'mi', 'mid', 'midi', 'mk', 'mkv', 'mm', 'mng', 'mo', 'mobi', 'mod', 'mov', 'mp2', 'mp3', 'mp4', 'mpa', 'mpd', 'mpe', 'mpeg', 'mpg', 'mpga', 'mpp', 'mpt', 'msg', 'msi', 'msu', 'nef', 'nes', 'nfo', 'nix', 'npmignore', 'ocx', 'odb', 'ods', 'odt', 'ogg', 'ogv', 'one', 'ost', 'otf', 'ott', 'ova', 'ovf', 'p12', 'p7b', 'pages', 'part', 'partial', 'pbix', 'pcd', 'pdb', 'pdf', 'pem', 'pfx', 'pgp', 'ph', 'phar', 'php', 'pid', 'pkg', 'pl', 'plist', 'pm', 'png', 'po', 'pom', 'pot', 'potx', 'ppk', 'pps', 'ppsx', 'ppt', 'pptm', 'pptx', 'prop', 'ps', 'ps1', 'psd', 'psp', 'pst', 'pub', 'py', 'pyc', 'pyw', 'qt', 'ra', 'ram', 'rar', 'raw', 'rb', 'rdf', 'rdl', 'reg', 'resx', 'retry', 'rm', 'rom', 'rpm', 'rpt', 'rsa', 'rss', 'rst', 'rtf', 'ru', 'rub', 'sass', 'save', 'scss', 'sdf', 'sed', 'sesx', 'sh', 'sit', 'sitemap', 'sketch', 'skin', 'sldm', 'sldx', 'sln', 'sol', 'sphinx', 'sql', 'sqlite', 'srt', 'step', 'stl', 'sub', 'svg', 'swd', 'swf', 'swift', 'swp', 'sys', 'tar', 'tax', 'tcsh', 'tex', 'tfignore', 'tga', 'tgz', 'tif', 'tiff', 'tmp', 'tmx', 'torrent', 'tpl', 'ts', 'tsv', 'tsx', 'ttf', 'twig', 'txt', 'udf', 'vb', 'vbproj', 'vbs', 'vcd', 'vcf', 'vcs', 'vdi', 'vdx', 'vmdk', 'vob', 'vox', 'vscodeignore', 'vsd', 'vss', 'vst', 'vsx', 'vtx', 'war', 'wav', 'wbk', 'webinfo', 'webm', 'webp', 'wma', 'wmf', 'wmv', 'woff', 'woff2', 'wpd', 'wps', 'wsf', 'xaml', 'xcf', 'xcodeproj', 'xfl', 'xlb', 'xlc', 'xlm', 'xls', 'xlsb', 'xlsm', 'xlsx', 'xlt', 'xltm', 'xltx', 'xml', 'xpi', 'xps', 'xrb', 'xsd', 'xsl', 'xspf', 'xz', 'yaml', 'yml', 'z', 'zip', 'zsh']


def get_file_type(file_path):
    mime, _ = mimetypes.guess_type(file_path)
    return mime


class FlowLayout(QLayout):
    def __init__(self, parent=None, margin=-1, hspacing=-1, vspacing=-1):
        super(FlowLayout, self).__init__(parent)
        self._hspacing = hspacing
        self._vspacing = vspacing
        self._items = []
        self.setContentsMargins(margin, margin, margin, margin)

    def __del__(self):
        del self._items[:]

    def addItem(self, item):
        self._items.append(item)

    def horizontalSpacing(self):
        if self._hspacing >= 0:
            return self._hspacing
        else:
            return self.smartSpacing(
                QStyle.PM_LayoutHorizontalSpacing)

    def verticalSpacing(self):
        if self._vspacing >= 0:
            return self._vspacing
        else:
            return self.smartSpacing(
                QStyle.PM_LayoutVerticalSpacing)

    def count(self):
        return len(self._items)

    def itemAt(self, index):
        if 0 <= index < len(self._items):
            return self._items[index]

    def takeAt(self, index):
        if 0 <= index < len(self._items):
            return self._items.pop(index)

    def expandingDirections(self):
        return QtCore.Qt.Orientations(0)

    def hasHeightForWidth(self):
        return True

    def heightForWidth(self, width):
        return self.doLayout(QtCore.QRect(0, 0, width, 0), True)

    def setGeometry(self, rect):
        super(FlowLayout, self).setGeometry(rect)
        self.doLayout(rect, False)

    def sizeHint(self):
        return self.minimumSize()

    def minimumSize(self):
        size = QtCore.QSize()
        for item in self._items:
            size = size.expandedTo(item.minimumSize())
        left, top, right, bottom = self.getContentsMargins()
        size += QtCore.QSize(left + right, top + bottom)
        return size

    def doLayout(self, rect, testonly):
        left, top, right, bottom = self.getContentsMargins()
        effective = rect.adjusted(+left, +top, -right, -bottom)
        x = effective.x()
        y = effective.y()
        lineheight = 0
        for item in self._items:
            widget = item.widget()
            hspace = self.horizontalSpacing()
            if hspace == -1:
                hspace = widget.style().layoutSpacing(
                    QSizePolicy.PushButton,
                    QSizePolicy.PushButton, QtCore.Qt.Horizontal)
            vspace = self.verticalSpacing()
            if vspace == -1:
                vspace = widget.style().layoutSpacing(
                    QSizePolicy.PushButton,
                    QSizePolicy.PushButton, QtCore.Qt.Vertical)
            nextX = x + item.sizeHint().width() + hspace
            if nextX - hspace > effective.right() and lineheight > 0:
                x = effective.x()
                y = y + lineheight + vspace
                nextX = x + item.sizeHint().width() + hspace
                lineheight = 0
            if not testonly:
                item.setGeometry(
                    QtCore.QRect(QtCore.QPoint(x, y), item.sizeHint()))
            x = nextX
            lineheight = max(lineheight, item.sizeHint().height())
        return y + lineheight - rect.y() + bottom

    def smartSpacing(self, pm):
        parent = self.parent()
        if parent is None:
            return -1
        elif parent.isWidgetType():
            return parent.style().pixelMetric(pm, None, parent)
        else:
            return parent.spacing()


class FlowBox(QFrame):
    def __init__(self, name: str, type, clickButton, fileSize: str, path: str, parent, size_=[70, 90]):
        super(FlowBox, self).__init__()
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.rightMenuShow)  # 开放右键策略
        self.setContentsMargins(1, 1, 1, 1)
        self.type = type
        self.name = name
        self.parent = parent
        self.clickButton = clickButton
        self.path = path.replace('\\', '/')
        self.size_ = size_
        self.fileSize = fileSize
        self.mainLayout = QVBoxLayout(self)
        self.mainLayout.setContentsMargins(0, 0, 0, 0)
        self.mainLayout.setSpacing(0)

        self.MainWidget = QWidget()
        self.MainWidget.setObjectName('flowMainWidget')
        self.MainWidget.setStyleSheet('''
#flowMainWidget 
{
    border : 0px !important;
    background-color : rgba(0,0,0,0);
    border-radius :5px;
}
#flowMainWidget:hover {
    background-color : rgba(175,175,175,0.2);
    border-radius :5px;
}
''')
        self.mainLayout.addWidget(self.MainWidget)

        self.ThisLayout = QVBoxLayout(self.MainWidget)
        self.setMaximumSize(size_[0], size_[1])
        self.setMinimumSize(size_[0], size_[1])
        self.ThisLayout.setContentsMargins(0, 4, 0, 4)
        self.ThisLayout.setSpacing(0)
        #
        self.setObjectName('baseFlowBox')

        #
        self.IconLabel = QLabel()  # 图标
        Hlayout = QHBoxLayout()
        self.IconLabel.setFixedSize(size_[0] - 28, size_[0] - 28)
        #
        self.NameLabel = QTextBrowser()  # 名字
        self.NameLabel.setHorizontalScrollBarPolicy(1)
        self.NameLabel.setVerticalScrollBarPolicy(1)
        # self.NameLabel.setAlignment(Qt.AlignCenter)
        # self.NameLabel.setWordWrap(True)
        #
        self.NameLabel.setAlignment(Qt.AlignTop)
        #
        type_ = self.type+'.svg'
        if self.type == 'mcfunction':
            type_ = self.type+'.png'
        if self.name == 'readme':
            type_ = 'readme.svg'
        self.IconLabel.setStyleSheet(f'''
background-repeat: no-repeat;
background-position: center center;
background-color:rgba(0,0,0,0);''')

        # check the icon existence
        if self.type in iconType:
            icon = QPixmap(f'./img/fileTypeIcon/high-contrast/{type_}')
        else:
            icon = QPixmap(f'./img/fileTypeIcon/high-contrast/blank.svg')
        # 一些特殊的文件类型的图标
        if self.type == 'mcfunction':
            # mcfunction文件图标
            icon = QPixmap('img/pureIcon/icon2x512.png')
        elif self.type == 'nbt':
            # nbt文件图标
            icon = QPixmap('img/fileTypeIcon/high-contrast/inv.svg')
        elif self.type == 'mca':
            # mca文件图标
            icon = QPixmap('img/fileTypeIcon/high-contrast/inv.svg')
        elif self.type == 'obj':
            # obj文件图标
            icon = QPixmap('img/fileTypeIcon/high-contrast/ps1.svg')
        elif self.type == 'mtl':
            # obj文件图标
            icon = QPixmap('img/fileTypeIcon/high-contrast/ps1.svg')
        elif self.name == '__NBTFileChangedTime__':
            # __NBTFileChangedTime__文件图标
            icon = QPixmap('img/fileTypeIcon/high-contrast/app.svg')
        elif self.type == 'mcmeta':
            # mcmeta文件图标
            icon = QPixmap('img/fileTypeIcon/high-contrast/app.svg')

        self.IconLabel.setPixmap(icon)
        self.icon = icon

        # self.IconLabel.setScaledContents(True)
        self.IconLabel.setScaledContents(True)
        ##
        self.NameLabel.setText(self.name)
        self.NameLabel.setFixedHeight(44)
        self.NameLabel.setFixedWidth(size_[0])
        self.NameLabel.setStyleSheet('''
font-size:10px;
border:0px;
background-color:rgba(0,0,0,0);
text-align:center;''')

        Type = get_file_type(self.name)
        if Type == None:
            Type = self.name.split('.')[-1]
        #
        Type += ' File Type'
        self.Filetype = 'file'
        if self.fileSize == 'folder':
            Type = 'Folder'
            self.Filetype = 'folder'
            # 统计此文件夹下的项目
            folderCount = 0
            fileCount = 0
            dir_or_files = os.listdir(self.path)
            for dir_file in dir_or_files:
                dir_file_path = os.path.join(self.path, dir_file)
                if os.path.isdir(dir_file_path):
                    folderCount += 1
                else:
                    fileCount += 1
            self.fileSize = f'Folder : {folderCount}  | File : {fileCount}'
        else:
            self.Filetype = 'file'

        self.TYPE = Type
        self.setToolTip(
            f'<div><b >{self.name}</b><br/>Type : {Type}<br/>Path : {self.path}<br/>Size : {self.fileSize}</div>')
        self.installEventFilter(ToolTipFilter(
            self, 300, ToolTipPosition.RIGHT))
        # add
        Hlayout.addWidget(self.IconLabel)
        self.ThisLayout.addLayout(Hlayout)
        self.ThisLayout.addWidget(self.NameLabel)

    def mouseDoubleClickEvent(self, a0: QMouseEvent) -> None:
        self.clickButton([self.name, self.Filetype])
        return super().mouseDoubleClickEvent(a0)

    def mousePressEvent(self, a0: QMouseEvent) -> None:
        if self.parent.lastClick != None:
            # set last click
            try:
                self.parent.lastClick.MainWidget.setObjectName(
                    'flowMainWidget')
                self.parent.lastClick.MainWidget.setStyleSheet('''
    #flowMainWidget 
    {
        border : 0px !important;
        background-color : rgba(0,0,0,0);
        border-radius 5px;
    }
    #flowMainWidget:hover {
        background-color : rgba(175,175,175,0.2);
        border-radius :5px;
    }
                ''')
                # set this click
                self.MainWidget.setStyleSheet('''
    #flowMainWidget 
    {
        border : 0px !important;
        background-color : rgba(105, 151, 219,0.4);
        border-radius :5px;
    }
    #flowMainWidget:hover {
        background-color : rgba(71, 114, 179,0.4);
        border-radius :5px;
    }
                ''')
                self.parent.lastClick = self
            except:
                self.MainWidget.setStyleSheet('''
#flowMainWidget 
{
    border : 0px !important;
    background-color : rgba(105, 151, 219,0.4);
    border-radius :5px;
}
#flowMainWidget:hover {
    background-color : rgba(71, 114, 179,0.4);
    border-radius :5px;
}
            ''')
            self.parent.lastClick = self
        else:
            self.MainWidget.setStyleSheet('''
#flowMainWidget 
{
    border : 0px !important;
    background-color : rgba(105, 151, 219,0.4);
    border-radius :5px;
}
#flowMainWidget:hover {
    background-color : rgba(71, 114, 179,0.4);
    border-radius :5px;
}
            ''')
            self.parent.lastClick = self

    def rightMenuShow(self, pos):  # 添加右键菜单
        # print('rightMenuShow')
        menu = PureRoundedBorderMenu(self)
        menu.setFixedWidth(250)
        # info widget
        self.info_action = QWidgetAction(menu)
        self.info_widget = QWidget()
        self.info_widget.setObjectName('info_widget')
        self.info_widget.setStyleSheet(
            '#info_widget {background-color:rgba(0,0,0,0);}')
        # set icon
        BigIcon = QLabel()
        BigIcon.setScaledContents(1)
        new_icon = QPixmap(self.icon)
        new_icon.scaled(60, 60)
        BigIcon.setPixmap(new_icon)
        BigIcon.setFixedSize(60, 60)
        #
        rightLayout = QVBoxLayout()
        Name = QLabel(self.name)
        Name.setStyleSheet(
            'font-size:14px;font-weight:bold;background-color:rgba(0,0,0,0);')
        Type = QLabel(self.TYPE)
        Type.setStyleSheet(
            'font-size:10px;color:gray;background-color:rgba(0,0,0,0);')
        Size = QLabel(self.fileSize)
        Size.setStyleSheet(
            'font-size:10px;color:gray;background-color:rgba(0,0,0,0);')
        rightLayout.addWidget(Name)
        rightLayout.addWidget(Type)
        rightLayout.addWidget(Size)
        rightLayout.setContentsMargins(0, 0, 0, 0)
        #

        infoLayout = QHBoxLayout(self.info_widget)
        infoLayout.addWidget(BigIcon)
        infoLayout.addLayout(rightLayout)
        self.info_widget.setFixedWidth(200)
        self.info_widget.setFixedHeight(80)
        self.info_action.setDefaultWidget(self.info_widget)

        menu.addAction(self.info_action)
        menu.addSeparator()

        open = QAction('打开', menu)
        open.setIcon(QIcon('./img/toolbar/d_AreaEffector2D Icon.png'))
        open.setShortcut('Shift+O')
        menu.addAction(open)

        copy = QAction('复制', menu)
        copy.setIcon(QIcon('./img/toolbar/d_Profiler.UIDetails@2x.png'))
        copy.setShortcut('Shift+C')
        menu.addAction(copy)

        paste = QAction('粘贴', menu)
        paste.setIcon(QIcon('./img/toolbar/d_winbtn_win_restore_h@2x.png'))
        paste.setShortcut('Shift+V')
        menu.addAction(paste)

        saveAs = QAction('另存为', menu)
        saveAs.setIcon(QIcon('./img/toolbar/saveAs.png'))
        saveAs.setShortcut('Shift+S')
        menu.addAction(saveAs)

        rename = QAction('重命名', menu)
        rename.setIcon(QIcon('./img/toolbar/d_SceneViewTools@2x.png'))
        rename.setShortcut('Shift+R')
        menu.addAction(rename)

        menu.addSeparator()
        delete = QAction('删除', menu)
        delete.setIcon(QIcon('./img/toolbar/d_winbtn_mac_close_h@2x.png'))
        delete.setShortcut('Shift+D')
        menu.addAction(delete)
        #
        menu.triggered.connect(self.menuSlot)
        menu.exec_(QCursor.pos())

    def menuSlot(self, act):
        select = act.text()
        if select == '删除':
            if self.fileSize == 'folder':
                warningTitle = f'Delete Folder'
                warningMessage = f'If you want to delete all files in the : "{self.path}" ?'
            else:
                warningTitle = f'Delete File'
                warningMessage = f'If you want to delete the file : "{self.path}" ?'
            # 先询问一下是否删除
            dialog = QMessageBox.warning(
                self.parent.parent, warningTitle, warningMessage, QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

            if dialog == QMessageBox.Yes:
                # 如果同意，就删除
                if self.fileSize == 'folder':
                    os.removedirs(self.path)
                else:
                    os.remove(self.path)
                self.hide()
            else:
                # 如果不同意
                pass
        elif select == '重命名':
            pass
        elif select == '复制':
            pass
        elif select == '粘贴':
            pass
        elif select == '另存为':
            pass
        elif select == '打开':
            # print('open file', self.name)
            self.clickButton([self.name, self.Filetype])

################################################################


class FlowWidget(QScrollArea):
    def __init__(self, parent, margin=2, hs=0, vs=0) -> None:
        super().__init__()
        self.setWidgetResizable(True)
        self.margin = margin
        self.hs = hs
        self.vs = vs
        self.ThisWidget = QFrame(self)
        self.ThisLayout = FlowLayout(
            self.ThisWidget, margin=self.margin, hspacing=self.hs, vspacing=self.vs)
        self.setWidget(self.ThisWidget)
        self.setObjectName('AssetWidget')
        # 完成初始化控件部分
        self.ThisWidget.setObjectName('AssetWidget')

    def addWidget(self, widget):
        self.ThisLayout.addWidget(widget)

################################################################


class AssetWidget(FlowWidget):
    def __init__(self, parent, path, bottom, openFile, pathWidget, changeFunction, filetype='*') -> None:
        super().__init__(parent)
        self.path = path
        self.parent = parent  # self:QMainWindow
        self.pathWidget = pathWidget
        self.filetype = filetype
        self.bottom = bottom
        self.lastClick = None
        self.changeFunction = changeFunction
        self.setRootPath(self.path)
        self.openFile = openFile

    def deleteLayout(self, layout):
        if layout is not None:
            while layout.count():
                item = layout.takeAt(0)
                widget = item.widget()
                if widget is not None:
                    widget.deleteLater()
                else:
                    self.parent.deleteLayout(item.layout())

    def setRootPath(self, path):
        # 更换目录用的
        self.path = path
        print('AssetWidget.Path ->', path)
        #
        item_list = list(
            range(self.ThisLayout.count()))
        item_list.reverse()  # 倒序删除，避免影响布局顺序
        for i in item_list:
            item = self.ThisLayout.itemAt(i)
            self.ThisLayout.removeItem(item)
            item.widget().deleteLater()
            if item.widget():
                item.widget().deleteLater()

        self.fileCount = 0
        self.DirCount = 0

        dir_or_files = os.listdir(self.path)
        for dir_file in dir_or_files:
            dir_file_path = os.path.join(self.path, dir_file)
            state = os.stat(dir_file_path)
            fileSize = state.st_size
            size = str(round(float(fileSize/1024), 2)) + ' kb'
            name = dir_file_path.split('\\')[-1]

            if os.path.isdir(dir_file_path):
                self.DirCount += 1
                self.ThisLayout.addWidget(
                    FlowBox(name, 'folder-base', self.click, 'folder', dir_file_path, self))
            else:
                self.fileCount += 1
                self.ThisLayout.addWidget(
                    FlowBox(name, name.split('.')[-1], self.click, size, dir_file_path, self))

        self.bottom.setText(
            f'目录 : {self.path.split("/")[-1]}  |  文件 : {str(self.fileCount)}  |  文件夹 : {str(self.DirCount)}')

        # 每次换目录都会重置一次thisclick
        self.lastClick = None
        self.changeFunction(self.path)
        self.pathWidget.setRootPath(self.path)

    # click 是传给flowbox的，flowbox被点击时会调用这个

    def click(self, name):
        pathName = name[0]
        pathType = name[1]
        Path = self.path+'/'+pathName
        if pathType == 'folder':
            self.path = Path
            self.setRootPath(self.path)
            self.pathWidget.setRootPath(self.path)

        elif pathType == 'file':
            # 从这里链接到main里的方法
            self.openFile(Path)


class PpathWidget(QScrollArea):
    def __init__(self, path, change_function):
        super().__init__()
        self.initUI()
        self.PathList = []
        self.path = path
        self.setRootPath(path)
        self.change_function = change_function

    def initUI(self):
        self.ThisWidget = QWidget(self)
        self.setWidgetResizable(True)
        self.setContentsMargins(0, 0, 0, 0)
        self.ThisLayout = QHBoxLayout(self.ThisWidget)
        self.setWidget(self.ThisWidget)

        self.ThisLayout.setContentsMargins(2, 1, 2, 1)
        self.setFixedHeight(40)
        self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.setObjectName('pathWidget')
        self.ThisWidget.setObjectName('ThisWidget_pathWidget')
        self.ThisWidget.setStyleSheet('''
#ThisWidget_pathWidget{
    border-radius:4px !important;
}
QPushButton {
    background-color:rgba(150,150,150,0.0);
    border-radius:3px;
    border:0px !important;
}
                                      ''')

    def setRootPath(self, path):
        self.PathList = []
        self.RootPath = path
        self.path = path
        item_list = list(
            range(self.ThisLayout.count()))
        item_list.reverse()  # 倒序删除，避免影响布局顺序
        for i in item_list:
            item = self.ThisLayout.itemAt(i)
            self.ThisLayout.removeItem(item)
            if item.widget():
                item.widget().deleteLater()
        # rewrite_print(path)
        PathCount = 0
        for Item in self.path.split('/'):
            ThisButton = QPushButton()
            ThisButton.setContentsMargins(0, 0, 0, 0)
            ThisButton.setFixedHeight(20)
            ThisButton.setIcon(QIcon('./img/open_s_a7.png'))
            ThisButton.setText(Item)
            ThisButton.setToolTip('floder : '+Item)
            ThisButton.installEventFilter(ToolTipFilter(
                ThisButton, 300, ToolTipPosition.BOTTOM))
            ThisButton.setObjectName("ThisButton")
            ThisButton.className = str(PathCount)
            ThisButton.setStyleSheet(
                '''
#ThisButton {color:rgba(97,158,239,0.9);}
#ThisButton:hover {color:#aaa;}''')
            ThisButton.clicked.connect(self.change)
            RIGHT_label = QLabel()
            RIGHT_label.setText('>')
            RIGHT_label.setStyleSheet(
                'font-weight:bold ;font-family:Consolas;')
            self.ThisLayout.addWidget(ThisButton)
            self.ThisLayout.addWidget(RIGHT_label)
            self.PathList.append(Item)
            PathCount += 1
        # 最后一个目录，特殊显示
        ThisButton.setStyleSheet(
            '''
#ThisButton {color:white;
background-color:#4772B3;
}''')
        RIGHT_label.hide()
        self.ThisLayout.addStretch(99999)

    def getPath(self):
        return self.RootPath

    def change(self):
        thisSender = self.sender().text()
        index = int(self.sender().className)
        print(index)
        newList = self.PathList[0:index]+[thisSender]
        self.PathList = newList
        # del
        self.path = '/'.join(newList)
        self.setRootPath(self.path)
        self.change_function(self.path)
