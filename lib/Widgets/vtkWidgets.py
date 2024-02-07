# coding:utf-8
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import PyQt5.QtWidgets as QtWidgets
from PyQt5.QtCore import *
import vtk
from vtkmodules.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor
from lib.Widgets.menu import PureRoundedBorderMenu

colors = vtk.vtkNamedColors()


class MouseInteractorHighLightActor(vtk.vtkInteractorStyleTrackballCamera):

    def __init__(self, renderer, parent=None):
        self.AddObserver(
            "LeftButtonPressEvent", self.on_left_button_down)
        self.AddObserver("MouseMoveEvent", self.on_mouse_move)
        self.AddObserver(
            "LeftButtonReleaseEvent", self.on_left_button_up)

        self._renderer_ = renderer
        self.LastPickedActor = None  # 上一个被选中的Actor
        self.LastPickedProperty = vtk.vtkProperty()  # 空属性(属性保存器)
        self.CanHightLightActor = False  # 标志是否可以高亮Actor

    def on_mouse_move(self, obj, event):
        # 调用父类的方法以确保其他交互行为得以继续
        self.CanHightLightActor = False
        obj.OnMouseMove()

    def on_left_button_up(self, obj, event):
        # 调用父类的方法以确保其他交互行为得以继续
        if self.CanHightLightActor:
            clickPos = self.GetInteractor().GetEventPosition()
            picker = vtk.vtkPropPicker()
            picker.Pick(clickPos[0], clickPos[1], 0, self.GetDefaultRenderer())
            # 创建一个新的actor
            self.NewPickedActor = picker.GetActor()
            # If something was selected
            if self.NewPickedActor:
                # If we picked something before, reset its property
                try:
                    # 尝试让上一个选中Actor的编译高亮不显示
                    self.LastPickedActor.outline_actor.VisibilityOff()
                    self.LastPickedActor.outline_actor.GetProperty().SetColor(1, 0.522, 0)  # 橙色
                except:
                    pass
                # 使用外轮廓的办法来高亮
                try:
                    self.NewPickedActor.outline_actor.GetProperty().SetColor(1, 0.522, 0)  # 橙色
                    self.NewPickedActor.outline_actor.VisibilityOn()
                    # 保存最后一个选中的actor
                    self.LastPickedActor = self.NewPickedActor  # 更新现在的选中Actor
                except:
                    pass
            else:
                try:
                    self.LastPickedActor.outline_actor.VisibilityOff()
                    self.LastPickedActor.outline_actor.GetProperty().SetColor(1, 0.522, 0)  # 橙色
                except:
                    pass
            self.CanHightLightActor = False
        obj.OnLeftButtonUp()

    def on_left_button_down(self, obj, event):
        self.CanHightLightActor = True
        obj.OnLeftButtonDown()


class TransparentRoundedBorderlessWindow(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # 设置无边框窗口、背景透明和圆角
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowFlags(self.windowFlags(
        ) | Qt.FramelessWindowHint | Qt.NoDropShadowWindowHint)
        # 添加阴影效果

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        opacity = 0.5
        painter.setOpacity(opacity)
        # 绘制透明圆角矩形
        rounded_rect = self.rect().adjusted(15, 15, -15, -15)  # 调整矩形大小以便留出阴影空间
        painter.setBrush(QBrush(QColor(0, 0, 0, 0)))
        painter.drawRoundedRect(rounded_rect, 15, 15)


class CustomVTKWidget(QVTKRenderWindowInteractor):
    def __init__(self, parent=None):
        super().__init__(parent)

        # 创建右键菜单
        self.context_menu = PureRoundedBorderMenu(self)
        #
        self.CommandInputer = QLineEdit()
        self.CommandInputer.setFixedHeight(25)
        self.CommandInputer.setPlaceholderText('input Command')
        self.CommandInputer.setObjectName('SearchPathWidget')
        self.CommandInputer.setClearButtonEnabled(1)
        self.CommandInputer.setStyleSheet(
            '''* {
                padding-left: 12px;
                background-image: url(./img/toolbar/d_PlayButton.png);
                background-repeat: no-repeat;
                background-position: left center;
                }''')
        actionWidget = QWidgetAction(self.context_menu)
        inputer_Widget = QWidget()
        inputer_Widget.setFixedWidth(200)
        inputer_Widget.setFixedHeight(30)
        actionWidget.setDefaultWidget(inputer_Widget)
        inputer_Layout = QVBoxLayout(inputer_Widget)
        inputer_Layout.setContentsMargins(5, 5, 5, 0)
        inputer_Layout.addWidget(self.CommandInputer)
        #
        action_reset = QAction("重置相机 (Reset Camera)", self)
        action_reset.triggered.connect(self.resetCamera)
        self.context_menu.addAction(actionWidget)
        self.context_menu.addAction(action_reset)
        # 监听事件状态，标识是否可以弹出右键菜单
        self.canPopMenu = False
        # 设置右键菜单策略
        self.setContextMenuPolicy(Qt.CustomContextMenu)

    def resetCamera(self):
        self.context_menu.hide()  # 隐藏右键菜单
        # 在这里添加代码以重置 VTK 渲染器的相机视图

    def mouseMoveEvent(self, ev):
        self.canPopMenu = False
        return super().mouseMoveEvent(ev)

    def mousePressEvent(self, ev):
        if ev.button() == Qt.RightButton:
            # 右键按下
            self.canPopMenu = True
        return super().mousePressEvent(ev)

    def mouseReleaseEvent(self, ev):
        if ev.button() == Qt.RightButton:
            # 右键释放
            if self.canPopMenu:
                self.context_menu.exec_(self.mapToGlobal(ev.pos()))
            self.canPopMenu = False
        return super().mouseReleaseEvent(ev)
