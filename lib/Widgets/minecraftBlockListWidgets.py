# coding:utf-8
import os
from PyQt5 import QtCore, QtGui
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import PyQt5.QtWidgets as QtWidgets
from PyQt5.QtCore import *

from lib.Widgets.flowWidgets import FlowWidget
from lib.Widgets.tooltip import ToolTipFilter, ToolTipPosition
# 一个方块列表显示控件
# blocks List Widget
# 方块子项控件
# blocks Item Widget


class BlockPushButton(QPushButton):
    def __init__(self, parent=None, doubleFunc=None) -> None:
        super(BlockPushButton, self).__init__()
        self.parentSelf = parent
        self.doubleFunc = doubleFunc

    def setdoubleClick(self, doubleFunc=None):
        self.doubleFunc = doubleFunc

    def mouseDoubleClickEvent(self, a0: QMouseEvent) -> None:
        self.doubleFunc()
        return super().mouseDoubleClickEvent(a0)


class BlockItemWidget(QWidget):
    '''
    方块子项控件
    blocks Item Widget
    '''

    def __init__(self, blockName: str, blockCount) -> None:
        super(BlockItemWidget, self).__init__()
        self.blockName = blockName
        self.blockCount = blockCount
        print(self.blockName)
        self.MainWidget = QWidget()
        self.xLayout = QVBoxLayout(self)
        self.xLayout.setContentsMargins(0, 0, 0, 0)
        self.xLayout.addWidget(self.MainWidget)

        self.MainWidget.setObjectName('BlockItem')
        self.MainWidget.setStyleSheet('''#BlockItem { background-color:rgba(175,175,175,0.1);
                        border:2px solid rgba(175,175,175,0.3);
                        border-radius:0px !important;}
                                      #BlockItem:hover {
                                      background-color:rgba(175,175,175,0.2);
                                      }''')
        self.MainWidget.setToolTip(
            f'''<div style="color:gray;display:inline;">minecraft:<br/><a>{self.blockName}</a></div>''')
        self.MainWidget.installEventFilter(ToolTipFilter(
            self.MainWidget, 300, ToolTipPosition.BOTTOM))
        # layout
        self.setFixedSize(40, 40)
        self.mainLayout = QVBoxLayout(self.MainWidget)
        self.mainLayout.setContentsMargins(5, 5, 5, 5)
        # 用pushbutton来代替Label,显示图片效果更好
        self.nameLabel = BlockPushButton(self)
        icon = self.blockName+'.png'
        if os.path.exists('./img/Blocks/'+self.blockName+'.png') == False:
            if os.path.exists('./img/Blocks/'+'Block of '+self.blockName.replace(' Block', '')+'.png') == True:
                icon = 'Block of '+self.blockName.replace(' Block', '')+'.png'
                print('check one block name different',
                      self.blockName, '->', icon)
            elif os.path.exists('./img/Blocks/'+self.blockName+'.gif') == True:
                icon = self.blockName+'.gif'
            elif os.path.exists('./img/Blocks/'+self.blockName+' Block.png') == True:
                icon = self.blockName+' Block.png'
        self.icon = icon
        pixmap = QPixmap('./img/Blocks/'+icon)
        pixmap.scaled(30, 30)
        self.nameLabel.setIcon(
            QIcon(pixmap))
        self.nameLabel.setFixedSize(30, 30)
        self.nameLabel.setIconSize(QSize(30, 30))
        self.nameLabel.setStyleSheet(
            '''*{background-color:rgba(175,175,175,0.1);
            border:0px !important;
            border-radius:0px !important;}''')
        self.mainLayout.addWidget(self.nameLabel)
        #
        self.blockCountLabel = QLabel(self)
        self.blockCountLabel.setFixedWidth(35)
        self.blockCountLabel.setAlignment(Qt.AlignRight)
        self.blockCountLabel.setFixedHeight(18)
        self.blockCountLabel.setStyleSheet(
            '''background-color:rgba(0,0,0,0);
            text-align:right !important;
            border-radius:0px !important;
            font-family:zpix;''')
        self.blockCountLabel.setText(str(self.blockCount))
        self.blockCountLabel.move(0, 22)
        self.nameLabel.setdoubleClick(self.openImage)

    def openImage(self):
        Image = QMainWindow(self)
        Image.setWindowTitle(self.icon)
        Image.resize(150, 150)
        Image.setFixedSize(150, 150)
        mainWidget = QWidget()
        Image.setCentralWidget(mainWidget)
        ImageLayout = QVBoxLayout(mainWidget)
        ImageLayout.setContentsMargins(25, 5, 25, 5)
        ImageLayout.setSpacing(0)
        IconLabel = QLabel()
        IconLabel.setFixedSize(100, 100)
        IconLabel.setPixmap(QPixmap('./img/Blocks/'+self.icon))
        IconLabel.setScaledContents(True)
        ImageLayout.addWidget(IconLabel)
        ImageLayout.addStretch(999)
        ImageLayout.addWidget(QLabel(self.blockName))
        Image.show()


class BlockListWidget(QWidget):
    '''
    方块列表显示控件
    blocks List Widget
    '''

    def __init__(self, blockList: dict = {}) -> None:
        super(BlockListWidget, self).__init__()
        self.blockList = blockList
        self.setStyleSheet(
            'border-radius: 5px !important')
        # 直接复用FlowWidget
        self.mainLayout = QVBoxLayout(self)
        self.mainLayout.setContentsMargins(0, 0, 0, 0)
        self.ListWidget = FlowWidget(self, 4, 4, 4)
        self.ListWidget.setStyleSheet(
            'border-radius: 5px !important')
        self.ListWidget.ThisWidget.setStyleSheet(
            'border-radius: 5px !important')
        self.mainLayout.addWidget(self.ListWidget)
        # 初始化时就更新一次
        self.update()
        #

    def update(self, blockList: dict = {}):
        item_list = list(
            range(self.ListWidget.ThisLayout.count()))
        item_list.reverse()  # 倒序删除，避免影响布局顺序
        for i in item_list:
            item = self.ListWidget.ThisLayout.itemAt(i)
            self.ListWidget.ThisLayout.removeItem(item)
            item.widget().deleteLater()
            if item.widget():
                item.widget().deleteLater()
        # 先删除原来的
        self.blockList = blockList
        for block in self.blockList:
            blockCount = self.blockList[block]
            # add block item to layout
            self.ListWidget.ThisLayout.addWidget(
                BlockItemWidget(block, blockCount))


class Pure_BlockItemWidget(QWidget):
    '''
    方块子项控件 2
    blocks Item Widget 2
    pure[2]
    '''

    def __init__(self, iconPath, blockName) -> None:
        super(Pure_BlockItemWidget, self).__init__()
        self.iconPath = iconPath
        self.blockName = blockName

        self.MainWidget = QWidget()
        self.xLayout = QVBoxLayout(self)
        self.xLayout.setContentsMargins(0, 0, 0, 0)
        self.xLayout.addWidget(self.MainWidget)

        self.MainWidget.setObjectName('BlockItem')
        self.MainWidget.setStyleSheet('''#BlockItem { background-color:rgba(175,175,175,0.1);
                        border:2px solid rgba(175,175,175,0.3);
                        border-radius:0px !important;}
                                      #BlockItem:hover {
                                      background-color:rgba(175,175,175,0.2);
                                      }''')
        self.MainWidget.setToolTip(
            f'''<div style="color:gray;display:inline;">minecraft:<br/><a>{self.blockName}</a></div>''')
        self.MainWidget.installEventFilter(ToolTipFilter(
            self.MainWidget, 300, ToolTipPosition.BOTTOM))
        # layout
        self.setFixedSize(40, 40)
        self.mainLayout = QVBoxLayout(self.MainWidget)
        self.mainLayout.setContentsMargins(5, 5, 5, 5)
        # 用pushbutton来代替Label,显示图片效果更好
        self.nameLabel = BlockPushButton(self, print)

        self.icon = iconPath
        pixmap = QPixmap(iconPath)
        pixmap.scaled(30, 30)
        self.nameLabel.setIcon(
            QIcon(pixmap))
        self.nameLabel.setFixedSize(30, 30)
        self.nameLabel.setIconSize(QSize(30, 30))
        self.nameLabel.setStyleSheet(
            '''*{background-color:rgba(175,175,175,0.1);
            border:0px !important;
            border-radius:0px !important;}''')
        self.mainLayout.addWidget(self.nameLabel)


class PBlocksList(QWidget):

    def __init__(self) -> None:
        super(PBlocksList, self).__init__()
        self.setObjectName('blockList')
        self.setStyleSheet(
            '#blockList {background-color: gray !important;}')
        # 直接复用FlowWidget
        self.mainLayout = QVBoxLayout(self)
        self.mainLayout.setContentsMargins(0, 0, 0, 0)
        self.ListWidget = FlowWidget(self, 4, 4, 4)
        self.ListWidget.setObjectName('ListWidget')
        self.ListWidget.setStyleSheet(
            '#ListWidget {border: 0px !important;background-color:rgba(0,0,0,0) !important;}')
        self.mainLayout.addWidget(self.ListWidget)
        # 初始化时就更新一次
        self.update()
        #

    def update(self):
        for root, dirs, files in os.walk('img/Blocks'):
            allBlocks = files
        for block in allBlocks:
            blockImagePath = 'img/Blocks/'+block
            name = block.replace('.png', '')
            self.ListWidget.ThisLayout.addWidget(
                Pure_BlockItemWidget(blockImagePath, name))
