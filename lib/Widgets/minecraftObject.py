# coding:utf-8
import json
import os
import random
import typing
from PyQt5 import QtCore, QtGui
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import PyQt5.QtWidgets as QtWidgets
from PyQt5.QtCore import *
from typing import Union
import nbtlib


'''
class MinecraftWindow(QWidget):
    def __init__(self):
        minecraft_handle = win32gui.FindWindow(None, "Minecraft 1.20.1")
        if minecraft_handle:
            # 将 Minecraft 窗口嵌入到 PyQt5 窗口中
            self.minecraft_window = QWindow.fromWinId(minecraft_handle)
            self.minecraft_window.setFlags(Qt.Widget)
            self.minecraft_window.create()
            # 创建窗口容器（使用 QWidget 替代 QWindowContainer）
            container = QWidget.createWindowContainer(self.minecraft_window)
            # 设置主窗口属性
            self.setCentralWidget(container)'''


DataPackVersion = {
    '1.13 (17w43a) - 1.13 (17w47b)': 3,
    '1.13 (17w48a) - 1.14.4 (19w46b)': 4,
    '1.15 (1.15-pre1) - 1.16.1 (1.16.2-pre3)': 5,
    '1.16.2 (1.16.2-rc1) - 1.16.5 (20w45a)': 6,
    '1.17 (20w46a) - 1.17.1 (1.18-exp7)': 7,
    '1.18 (21w37a) - 1.18.1 (22w07a)': 8,
    '1.18.2 (1.18.2-pre1 - 正式版)': 9,
    '1.19 (22w11a) - 1.19.3': 10,
    '1.19.4 快照23w03a - 23w05a': 11,
    '1.19.4 (23w06a - 正式版)': 12,
    '1.20 快照23w12a - 23w14a': 13,
    '1.20 快照23w16a - 23w17a': 14,
    '1.20 (23w18a) - 1.20.1': 15,
    '1.20.2 快照23w31a': 16,
    '1.20.2 快照23w32a - 23w35a': 17,
    '1.20.2 (1.20.2-pre1 - 正式版)': 18,
    '1.20.3 快照23w40a': 19,
    '1.20.3 快照23w41a': 20,
    '1.20.3 快照23w42a': 21,
    '1.20.3 快照23w43a': 22,
    '1.20.3 (23w44a) 及以上': 23
}

VMFile = {
    '$NAME': {
        'data': {
            '$NAME': {
                'functions': {

                },
                'advanceements': {

                },
                'item_modifiers': {

                },
                'predicates': {

                },
                'loot_tables': {

                },
            },
            'minecraft': {
                'tags': {
                    'functions': {
                    }
                }
            }
        },
        'pack.mcmeta': '''''',
        'readme': '''''',
    }
}


def createProject(lastDict, path, name):
    for _dict_ in lastDict:
        if type(lastDict[_dict_]) == type({}):
            # 文件夹
            _dict_name_ = _dict_
            if _dict_ == '$NAME':
                _dict_name_ = name
            print('floder - ', path, _dict_name_)
            os.makedirs(path+'\\'+_dict_name_)
            createProject(lastDict[_dict_], path+'\\'+_dict_name_, name)

        elif type(lastDict[_dict_]) == type(""):
            print('file - ', path, _dict_)
            # 文件
            with open(path+'//'+_dict_, 'w', encoding='utf-8') as File:
                File.write(lastDict[_dict_])


'''
Structure Object
'''
