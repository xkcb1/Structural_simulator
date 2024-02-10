import nbtlib
import sys
import os
import PyQt5.QtGui as QtGui
from PyQt5 import QtCore
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import PyQt5.QtWidgets as QtWidgets
from PyQt5.QtCore import *
from lib.mca import *
# import end


class LastNBTFile:
    def __init__(self, objpath, nbt_data) -> None:
        self.objpath = objpath
        self.nbt_data = nbt_data


class NbtTreeThread(QThread):   # 创建线程类
    def __init__(self, File, TreeWidget, parent=None, have_viewer=False):
        super(NbtTreeThread, self).__init__()
        self.parent = parent
        self.File = File
        self.TreeWidget = TreeWidget
        self.have_viewer = have_viewer

    def run(self):     # 重写run()方法
        if self.parent == None:
            nbt_file = TreePureNbtToObj(
                self.File, self.TreeWidget, self)
        else:
            nbt_file = TreePureNbtToObj(
                self.File, self.TreeWidget, self)
        # run objects functions
        # 更新 Objects 对象列表
        if self.have_viewer == True:
            self.parent.runObjects(nbt_file, self.File)
            # 更新 3D viewer 视图
            for vtkwidget in self.parent._mainVtk_:
                print('load model in ', vtkwidget, self.File)
                try:
                    vtkwidget._3D_viewer_(nbt_file, self.File)
                except:
                    # formatted_lines = traceback.format_exc()
                    # print(formatted_lines)
                    pass
        print('[!] : finished Thread -> NbtTreeThread')
        return


class NBTLastFileThread(QThread):   # 创建线程类
    def __init__(self, File, Objpath, TreeWidget, parent: QMainWindow = None):
        super(NBTLastFileThread, self).__init__()
        self.parent = parent
        self.File = File
        self.TreeWidget = TreeWidget
        self.Objpath = Objpath

    def run(self):     # 重写run()方法
        if self.parent == None:
            nbt_file = TreePureNbtToObj(
                self.File, self.TreeWidget, self)
        else:
            nbt_file = TreePureNbtToObj(
                self.File, self.TreeWidget, self)
        # run objects functions
        # 更新 Objects 对象列表
        if nbt_file != None:
            self.parent.runObjects(nbt_file, self.File)
            # 更新 3D viewer 视图
            LastNBT = LastNBTFile(self.Objpath, nbt_file)
            self.parent.lastNBT.LastNbtSignal.emit(LastNBT)
            # self.parent.loadNbtModelFunction(LastNBT)
        print('[!] : finished Thread -> NBTLastFile')
        return


#######################################################################


def deleteItem(TreeWidget):
    try:
        # 尝试删除子节点（通过其父节点，调用removeChild函数进行删除）
        currNode = TreeWidget.currentItem()
        parent1 = currNode.parent()
        parent1.removeChild(currNode)
    except Exception:
        # 遇到异常时删除根节点
        try:
            rootIndex = TreeWidget.indexOfTopLevelItem(currNode)
            TreeWidget.takeTopLevelItem(rootIndex)
        except Exception:
            print(Exception)
########################################################################


def TreePureNbtToObj(File, TreeWidget_list: QTreeWidget, self):
    for TreeWidget_index in TreeWidget_list:
        TreeWidget = TreeWidget_list[TreeWidget_index]
        TreeWidget.clear()
        fileType = File.split('/')[-1].split('.')[-1]
        if fileType == 'nbt':
            nbt_file = nbtlib.load(File)
            nbt_file = nbtlib.Compound(nbt_file)
        elif fileType == 'mca':
            nbt_file = makeMcaToNbt(File, outPut=False)
        else:
            # 退出表示弹出框标题，"你确定退出吗？"表示弹出框的内容
            msg_box = QMessageBox(QMessageBox.Critical,
                                  'Error - Unkown filetype', f'<p style="color:red;">未知的文件类型 : {fileType}</p><p style="color:red;">允许的文件类型 : .nbt , .mca</p>')
            msg_box.setWindowIcon(QIcon('./img/main_3/Nbt.png'))
            msg_box.exec_()
            nbt_file = None
        if nbt_file != None:
            tagParent = QTreeWidgetItem(TreeWidget)
            tagParent.setText(0, File.split('/')[-1])
            tagParent.setIcon(0, QIcon('img/toolbar/CGProgram_Icon.png'))
            tagParent.NBT = None
            # tagParent.setExpanded(True)
            for item in nbt_file:
                if str(type(nbt_file[item])) == "<class 'nbtlib.tag.ByteArray'>":
                    MakeTree(nbtlib.ByteArray(
                        nbt_file[item]), tagParent, item, 0)
                else:
                    MakeTree(nbt_file[item], tagParent, item, 0)

            # if parent != None then run Objects functions
            # 展开
            self.parent.expendFunc.expendSingal.emit(tagParent)
        return nbt_file


def MakeTree(parent, parentWidget, name='', count=1):
    tag = QTreeWidgetItem(parentWidget)
    tag.NBT = parent
    # print('makeTree [1] :',tag,tag.NBT)
    if str(type(parent)) == "<class 'nbtlib.tag.String'>":
        tag.setIcon(0, QIcon('./img/fileicon/str_1.png'))
        tag.setText(0, name)
        tag.setText(1, str(parent))
    elif str(type(parent)) == "<class 'nbtlib.tag.ByteArray'>":
        tag.setIcon(0, QIcon('./img/fileicon/B_LIST_1.png'))
        tag.setText(0, name+' ['+str(len(parent))+']')
        for item in parent:
            if count != 0:
                MakeTree(item, tag, count=0)
        if len(parent) == 0:
            tag.setText(1, '[ ]')
    elif str(parent)[:4] == 'List':
        tag.setIcon(0, QIcon('./img/fileicon/LIST_1.png'))
        tag.setText(0, name+' ['+str(len(parent))+']')
        for item in parent:
            if count != 0:
                MakeTree(item, tag, count=0)
        if len(parent) == 0:
            tag.setText(1, '[ ]')
    elif str(parent)[:8] == 'Compound':
        tag.setIcon(0, QIcon('./img/fileicon/COM_1.png'))
        tag.setText(0, name+' ['+str(len(parent))+']')
        for item in parent:
            if count != 0:
                MakeTree(parent[item], tag, item, count=0)
        if len(parent) == 0:
            tag.setText(1, '{ }')
    elif str(parent)[:4] == 'Byte':
        tag.setIcon(0, QIcon('./img/fileicon/B_1.png'))
        tag.setText(0, name)
        tag.setText(1, str(parent))
    elif str(parent)[:4] == 'Long':
        tag.setIcon(0, QIcon('./img/fileicon/L_1.png'))
        tag.setText(0, name)
        tag.setText(1, str(parent))
    elif str(parent)[:5] == 'Short':
        tag.setIcon(0, QIcon('./img/fileicon/S_1.png'))
        tag.setText(0, name)
        tag.setText(1, str(parent))
    elif str(parent)[:5] == 'Float':
        tag.setIcon(0, QIcon('./img/fileicon/F_1.png'))
        tag.setText(0, name)
        tag.setText(1, str(parent))
    elif str(parent)[:6] == 'Double':
        tag.setIcon(0, QIcon('./img/fileicon/D_1.png'))
        tag.setText(0, name)
        tag.setText(1, str(parent))
    elif str(parent)[:3] == 'End':
        tag.setIcon(0, QIcon('./img/fileicon/NONE_1.png'))
        tag.setText(0, name)
        tag.setText(1, str(parent))
    elif str(parent)[:3] == 'Int':
        tag.setIcon(0, QIcon('./img/fileicon/I_1.png'))
        tag.setText(0, name)
        tag.setText(1, str(parent))


class AddItemThread(QThread):   # 创建线程类
    '''
    用来异步创建子项
    '''

    def __init__(self, TreeWidget, parentWidget, parent=None):
        super(AddItemThread, self).__init__()
        '''
        parent是QMainWindow
        parentWidget是父项，或者父控件
        TreeWidget是树控件，也就是根父控件
        '''
        self.parent = parent
        self.parentWidget = parentWidget
        self.TreeWidget = TreeWidget

    def run(self):     # 重写run()方法
        # print(self.parentWidget)
        try:
            parent = self.parentWidget.NBT
            if str(type(parent)) == "<class 'nbtlib.tag.ByteArray'>":
                for item in parent:
                    self.MakeTree(item, self.parentWidget, count=0)
                if len(parent) == 0:
                    self.parentWidget.setText(1, '[ ]')
            elif str(parent)[:4] == 'List':
                for item in parent:
                    self.MakeTree(item, self.parentWidget, count=0)
                if len(parent) == 0:
                    self.parentWidget.setText(1, '[ ]')
            elif str(parent)[:8] == 'Compound':
                for item in parent:
                    newCompound = nbtlib.Compound()
                    # print('\nin compound ->',item,parent[item],type(parent[item]))
                    self.MakeTree(parent[item],
                                  self.parentWidget, item, count=0)
                if len(parent) == 0:
                    self.parentWidget.setText(1, '{ }')
            # 然后准备销毁tag.NBT属性
            del self.parentWidget.NBT
        except:
            pass

    def MakeTree(self, parent, parentWidget, name='', count=1):
        '''
        parent是NBT数据
        parentWidget是父控件，或者父项
        name是项名字
        count是迭代次数
        '''
        tag = QTreeWidgetItem(parentWidget)
        tag.NBT = parent
        # print('makeTree [2] :',tag.NBT,type(tag.NBT))
        if str(type(tag.NBT)) == "<class 'nbtlib.tag.String'>":
            # print('!->>')
            tag.setIcon(0, QIcon('./img/fileicon/str_1.png'))
            tag.setText(0, name)
            tag.setText(1, str(tag.NBT))
        elif str(type(tag.NBT)) == "<class 'nbtlib.tag.ByteArray'>":
            tag.setIcon(0, QIcon('./img/fileicon/B_LIST_1.png'))
            tag.setText(0, name+' ['+str(len(tag.NBT))+']')
            for item in tag.NBT:
                if count != 0:
                    self.MakeTree(item, tag, count=0)
            if len(tag.NBT) == 0:
                tag.setText(1, '[ ]')
        elif str(tag.NBT)[:4] == 'List':
            tag.setIcon(0, QIcon('./img/fileicon/LIST_1.png'))
            tag.setText(0, name+' ['+str(len(tag.NBT))+']')
            for item in tag.NBT:
                if count != 0:
                    self.MakeTree(item, tag, count=0)
            if len(tag.NBT) == 0:
                tag.setText(1, '[ ]')
        elif str(tag.NBT)[:8] == 'Compound':
            tag.setIcon(0, QIcon('./img/fileicon/COM_1.png'))
            tag.setText(0, name+' ['+str(len(tag.NBT))+']')
            for item in tag.NBT:
                if count != 0:
                    self.MakeTree(tag.NBT[item], tag, item, count=0)
            if len(tag.NBT) == 0:
                tag.setText(1, '{ }')
        elif str(tag.NBT)[:4] == 'Byte':
            tag.setIcon(0, QIcon('./img/fileicon/B_1.png'))
            tag.setText(0, name)
            tag.setText(1, str(tag.NBT))
        elif str(tag.NBT)[:4] == 'Long':
            tag.setIcon(0, QIcon('./img/fileicon/L_1.png'))
            tag.setText(0, name)
            tag.setText(1, str(tag.NBT))
        elif str(tag.NBT)[:5] == 'Short':
            tag.setIcon(0, QIcon('./img/fileicon/S_1.png'))
            tag.setText(0, name)
            tag.setText(1, str(tag.NBT))
        elif str(tag.NBT)[:5] == 'Float':
            tag.setIcon(0, QIcon('./img/fileicon/F_1.png'))
            tag.setText(0, name)
            tag.setText(1, str(tag.NBT))
        elif str(tag.NBT)[:6] == 'Double':
            tag.setIcon(0, QIcon('./img/fileicon/D_1.png'))
            tag.setText(0, name)
            tag.setText(1, str(tag.NBT))
        elif str(tag.NBT)[:3] == 'End':
            tag.setIcon(0, QIcon('./img/fileicon/NONE_1.png'))
            tag.setText(0, name)
            tag.setText(1, str(tag.NBT))
        elif str(tag.NBT)[:3] == 'Int':
            tag.setIcon(0, QIcon('./img/fileicon/I_1.png'))
            tag.setText(0, name)
            tag.setText(1, str(tag.NBT))
