# coding:utf-8
import os
from PyQt5 import QtCore, QtGui
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import PyQt5.QtWidgets as QtWidgets
from PyQt5.QtCore import *
from lib.NbtTree import AddItemThread, NbtTreeThread, NBTLastFileThread, LastNBTFile


def CreateFileTree():
    # filetreeview
    fileTreeView = QTreeView()
    fileTreeView.model_ = QDirModel()
    # self.fileTreeView.model_.index

    fileTreeView.setModel(fileTreeView.model_)

    fileTreeView.setAnimated(True)
    fileTreeView.setIndentation(20)
    fileTreeView.setRootIndex(fileTreeView.model_.index('./'))
    fileTreeView.setSortingEnabled(True)
    fileTreeView.setEditTriggers(
        QAbstractItemView.DoubleClicked | QAbstractItemView.EditKeyPressed)
    fileTreeView.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
    # 置水平滚动条为按需显示
    fileTreeView.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
    # 置双击或者按下Enter键时，树节点可编辑
    fileTreeView.setEditTriggers(
        QAbstractItemView.DoubleClicked | QAbstractItemView.EditKeyPressed)
    # 设置树节点为单选
    fileTreeView.setSelectionMode(QAbstractItemView.SingleSelection)
    # 置选中节点时为整行选中
    fileTreeView.setSelectionBehavior(QAbstractItemView.SelectRows)
    fileTreeView.setAutoExpandDelay(-1)
    # 置自动展开延时为-1，表示自动展开不可用
    fileTreeView.setItemsExpandable(True)
    # 置是否可以展开项
    fileTreeView.setSortingEnabled(True)
    # 置单击头部可排序
    fileTreeView.setWordWrap(True)
    # 置自动换行
    fileTreeView.setHeaderHidden(False)
    # 置不隐藏头部
    fileTreeView.setExpandsOnDoubleClick(True)
    # 置双击可以展开节点
    fileTreeView.header().setVisible(True)
    # 设置显示头部
    # 为树控件设置数据模型
    return fileTreeView


class PTreeWidget(QTreeWidget):
    def __init__(self, window):
        super().__init__()
        self.selectionModel().currentChanged.connect(self.onTreeClicked)
        self.window = window

    def onTreeClicked(self, index):
        # 如果点击到了节点，则尝试产生下一个节点
        try:
            item = self.currentItem()
            if item.childCount() == 0:
                name = 'newAddItemThread_'+str(self.window.thread_count)
                globals()[name
                          ] = AddItemThread(self, item, self.window)
                exec(name +
                     '.finished.connect('+name+'.deleteLater)')
                exec(name + '.start()')
                self.window.thread_count += 1
        except:
            pass
