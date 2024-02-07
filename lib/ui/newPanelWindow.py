#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
from PyQt5.QtCore import Qt, QPoint, QSize
from PyQt5.QtGui import QFont, QEnterEvent, QPixmap, QColor, QIcon
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QDialog, QGraphicsDropShadowEffect
from PyQt5 import QtCore
from PyQt5.QtCore import *
from lib.ui.newPanelUI import Ui_Form


class PanelWindow(QWidget, Ui_Form):
    def __init__(self, parent=None):
        super(PanelWindow, self).__init__(parent)
        self.setupUi(self)
        self._init_main_window()  # 主窗口初始化设置
        self._initDrag()  # 设置鼠标跟踪判断扳机默认值
        self.IfCanResize = True
        self.setMouseTracking(True)  # 设置widget鼠标跟踪
        # print(self.width(),self.height())
        self.widget.installEventFilter(self)  # 初始化事件过滤器
        self.widget_2.installEventFilter(self)
        self.widget_2.setStyleSheet('''#widget_2{border-bottom-left-radius: 7px;
    border-bottom-right-radius: 7px;}''')
        # 设置阴影
        self.shadow = QGraphicsDropShadowEffect()
        self.shadow.setBlurRadius(13)
        self.shadow.setColor(QColor(0, 0, 0))
        self.shadow.setOffset(0, 0)
        self.label_2.deleteLater()
        self.setContentsMargins(0, 0, 0, 0)
        #
        self.setWindowIcon(QIcon('./img/attr/earth_30_24.png'))
        #
        self.THIS_Widget.setGraphicsEffect(self.shadow)
        self.widget.setStyleSheet(
            '''#widget__{border:0px;background-color:rgba(175,175,175,0.1);}
            *{border:0px;}''')
        self.UseQss()

    def _init_main_window(self):
        # 设置窗体无边框
        self.setWindowFlags(Qt.FramelessWindowHint)
        # 设置背景透明
        self.setAttribute(Qt.WA_TranslucentBackground)
        w = self.label.width()
        h = self.label.height()
        # 注意修改Windows路径问题
        self.pix = QPixmap(
            r'./img/attr/earth_30_24.png')
        self.label.setPixmap(self.pix)
        self.label.setScaledContents(True)

    def _initDrag(self):
        # 设置鼠标跟踪判断扳机默认值
        self._move_drag = False
        self._corner_drag = False
        self._bottom_drag = False
        self._right_drag = False

    @QtCore.pyqtSlot()
    def on_pushButton_clicked(self):
        # 最小化
        self.showMinimized()

    @QtCore.pyqtSlot()
    def on_pushButton_2_clicked(self):
        # 最大化与复原
        if self.isMaximized():  # 缩小
            self.THIS_Widget.setContentsMargins(7, 7, 7, 7)
            self.verticalLayout__.setContentsMargins(1, 1, 1, 1)
            self.showNormal()  # 切换放大按钮图标
            self.pushButton_2.setToolTip(
                "<html><head/><body><p>最大化</p></body></html>")
        else:  # 放大
            self.THIS_Widget.setContentsMargins(0, 0, 0, 0)
            self.verticalLayout__.setContentsMargins(0, 0, 0, 0)
            self.showMaximized()
            self.pushButton_2.setToolTip(
                "<html><head/><body><p>恢复</p></body></html>")

    @QtCore.pyqtSlot()
    def on_pushButton_3_clicked(self):
        # 关闭程序
        self.close()

    def eventFilter(self, obj, event):
        # 事件过滤器,用于解决鼠标进入其它控件后还原为标准鼠标样式
        if isinstance(event, QEnterEvent):
            self.setCursor(Qt.ArrowCursor)
        # 注意 ,MyWindow是所在类的名称
        return super(PanelWindow, self).eventFilter(obj, event)
        # return QWidget.eventFilter(self, obj, event)  # 用这个也行，但要注意修改窗口类型

    def resizeEvent(self, QResizeEvent):
        # 自定义窗口调整大小事件
        # 改变窗口大小的三个坐标范围
        self._right_rect = [QPoint(x, y) for x in range(self.width() - 18, self.width() - 12)
                            for y in range(self.widget.height() + 18, self.height() - 12)]
        self._bottom_rect = [QPoint(x, y) for x in range(-12, self.width() - 18)
                             for y in range(self.height() - 18, self.height() - 12)]
        self._corner_rect = [QPoint(x, y) for x in range(self.width() - 18, self.width() - 12)
                             for y in range(self.height() - 18, self.height()-12)]

    def mousePressEvent(self, event):
        # 重写鼠标点击的事件
        if (event.button() == Qt.LeftButton) and (event.pos() in self._corner_rect):
            # 鼠标左键点击右下角边界区域
            self._corner_drag = True
            event.accept()
        elif (event.button() == Qt.LeftButton) and (event.pos() in self._right_rect):
            # 鼠标左键点击右侧边界区域
            self._right_drag = True
            event.accept()
        elif (event.button() == Qt.LeftButton) and (event.pos() in self._bottom_rect):
            # 鼠标左键点击下侧边界区域
            self._bottom_drag = True
            event.accept()
        elif (event.button() == Qt.LeftButton) and (0 < event.y() < self.widget.height()+15):
            # 鼠标左键点击标题栏区域
            self._move_drag = True
            self.move_DragPosition = event.globalPos() - self.pos()
            event.accept()

    def mouseMoveEvent(self, QMouseEvent):
        # 判断鼠标位置切换鼠标手势
        # 当鼠标左键点击不放及满足点击区域的要求后，分别实现不同的窗口调整
        # 没有定义左方和上方相关的5个方向，主要是因为实现起来不难，但是效果很差，拖放的时候窗口闪烁，再研究研究是否有更好的实现
        if self.IfCanResize == True:
            if QMouseEvent.pos() in self._corner_rect:  # QMouseEvent.pos()获取相对位置
                self.setCursor(Qt.SizeFDiagCursor)
            elif QMouseEvent.pos() in self._bottom_rect:
                self.setCursor(Qt.SizeVerCursor)
            elif QMouseEvent.pos() in self._right_rect:
                self.setCursor(Qt.SizeHorCursor)
            if Qt.LeftButton and self._right_drag:
                # print(QMouseEvent.pos().x())
                # 右侧调整窗口宽度
                # self.setMaximumSize(QSize(16777215, 16777215))
                self.resize(QMouseEvent.pos().x()+20, self.height())
                QMouseEvent.accept()
            elif Qt.LeftButton and self._bottom_drag:
                # self.setMaximumSize(QSize(16777215, 16777215))
                # 下侧调整窗口高度
                self.resize(self.width(), QMouseEvent.pos().y()+20)
                QMouseEvent.accept()
            elif Qt.LeftButton and self._corner_drag:
                # self.setMaximumSize(QSize(16777215, 16777215))
                #  由于我窗口设置了圆角,这个调整大小相当于没有用了
                # 右下角同时调整高度和宽度
                self.resize(QMouseEvent.pos().x()+20, QMouseEvent.pos().y()+20)
                QMouseEvent.accept()
            elif Qt.LeftButton and self._move_drag:
                # 标题栏拖放窗口位置
                if self.isMaximized():  # 如果是放大的
                    print('small')
                    self.THIS_Widget.setContentsMargins(7, 7, 7, 7)
                    self.verticalLayout__.setContentsMargins(1, 1, 1, 1)
                    self.showNormal()  # 切换放大按钮图标
                    self.pushButton_2.setToolTip(
                        "<html><head/><body><p>最大化</p></body></html>")
                    QMouseEvent.accept()
                self.move(QMouseEvent.globalPos() - self.move_DragPosition)
                QMouseEvent.accept()
        else:
            if Qt.LeftButton and self._move_drag:
                # 标题栏拖放窗口位置
                if self.isMaximized():  # 如果是放大的
                    print('small')
                    self.THIS_Widget.setContentsMargins(7, 7, 7, 7)
                    self.verticalLayout__.setContentsMargins(1, 1, 1, 1)
                    self.showNormal()  # 切换放大按钮图标
                    self.pushButton_2.setToolTip(
                        "<html><head/><body><p>最大化</p></body></html>")
                    QMouseEvent.accept()
                self.move(QMouseEvent.globalPos() - self.move_DragPosition)
                QMouseEvent.accept()

    def mouseReleaseEvent(self, QMouseEvent):
        # 鼠标释放后，各扳机复位
        self._move_drag = False
        self._corner_drag = False
        self._bottom_drag = False
        self._right_drag = False

    def UseQss(self):
        self.setStyleSheet('''
#pushButton {
    /*small*/
    border: 0px;
    background: url('./img/small_black.png');
    background-repeat: no-repeat;
    background-position: center center !important;
}
#pushButton_2 {
    /*full*/
    border: 0px;
    background: url('./img/full_black.png');
    background-repeat: no-repeat;
    background-position: center center !important;
}   
#pushButton_3 {
    /*close*/
    border: 0px;
    background: url('./img/close_black_2.png');
    background-repeat: no-repeat;
    background-position: center center !important;
}
#pushButton_3:hover {
    background-color:red;
    background-image: url('./img/close.png');
    background-position: center center !important;
}
#pushButton_3:checked {
}
#pushButton_2:hover,#pushButton:hover {
    background-color:rgba(150,150,150,0.1);
}
* {
    font-family: system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, 'Open Sans', 'Helvetica Neue', sans-serif;
}
QWidget {background-color:gray !important;}
''')
