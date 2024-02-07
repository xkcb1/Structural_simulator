# coding:utf-8
import os
from PyQt5 import QtCore, QtGui
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import PyQt5.QtWidgets as QtWidgets
from PyQt5.QtCore import *


class ImageBox(QWidget):
    def __init__(self):
        super(ImageBox, self).__init__()
        self.img = None
        self.scaled_img = None
        self.start_pos = None
        self.end_pos = None
        self.left_click = False
        self.wheel_flag = False

        self.scale = 1
        self.old_scale = 1
        self.point = QPoint(0, 0)
        self.x = -1
        self.y = -1
        self.new_height = -1
        self.new_width = -1

    def set_image(self, img_path):
        self.img = QPixmap(img_path)
        width, height = self.img.width(), self.img.height()

        self.scaled_img = self.img

        self.new_height = height
        self.new_width = width
        self.scale = 1

    def paintEvent(self, e):
        if self.scaled_img:
            painter = QPainter()
            painter.begin(self)
            painter.scale(self.scale, self.scale)
            if self.wheel_flag:        # 定点缩放
                self.wheel_flag = False
                # 判断当前鼠标pos在不在图上
                this_left_x = self.point.x() * self.old_scale
                this_left_y = self.point.y() * self.old_scale
                this_scale_width = self.new_width * self.old_scale
                this_scale_height = self.new_height * self.old_scale

                # 鼠标点在图上，以鼠标点为中心动作
                gap_x = self.x - this_left_x
                gap_y = self.y - this_left_y
                if 0 < gap_x < this_scale_width and 0 < gap_y < this_scale_height:
                    new_left_x = int(self.x / self.scale -
                                     gap_x / self.old_scale)
                    new_left_y = int(self.y / self.scale -
                                     gap_y / self.old_scale)
                    self.point = QPoint(new_left_x, new_left_y)
                # 鼠标点不在图上，固定左上角进行缩放
                else:
                    true_left_x = int(
                        self.point.x() * self.old_scale / self.scale)
                    true_left_y = int(
                        self.point.y() * self.old_scale / self.scale)
                    self.point = QPoint(true_left_x, true_left_y)
            # 此函数中还会用scale对point进行处理
            painter.drawPixmap(self.point, self.scaled_img)
            painter.end()

    def wheelEvent(self, event):
        angle = event.angleDelta() / 8  # 返回QPoint对象，为滚轮转过的数值，单位为1/8度
        angleY = angle.y()
        self.old_scale = self.scale
        self.x, self.y = event.x(), event.y()
        self.wheel_flag = True
        # 获取当前鼠标相对于view的位置
        if angleY > 0:
            self.scale *= 1.08
        else:  # 滚轮下滚
            self.scale *= 0.92
        if self.scale < 0.3:
            self.scale = 0.3
        self.adjustSize()
        self.update()

    def mouseMoveEvent(self, e):
        if self.left_click:
            self.end_pos = e.pos() - self.start_pos                    # 当前位置-起始位置=差值
            self.point = self.point + self.end_pos / self.scale        # 左上角的距离变化
            self.start_pos = e.pos()
            self.repaint()

    def mousePressEvent(self, e):
        if e.button() == Qt.LeftButton:
            self.left_click = True
            self.start_pos = e.pos()

    def mouseReleaseEvent(self, e):
        if e.button() == Qt.LeftButton:
            self.left_click = False


class TransparentWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._parent_ = parent
        # 设置无边框窗口、背景透明和圆角
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowFlags(
            Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setBrush(QBrush(QColor(0, 0, 0, 0)))
