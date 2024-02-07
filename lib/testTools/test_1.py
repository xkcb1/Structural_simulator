import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QPushButton, QGraphicsDropShadowEffect
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainter, QColor, QBrush
from vtkmodules.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor
from vtkmodules.all import vtkCubeSource, vtkPolyDataMapper, vtkActor, vtkRenderer, vtkRenderWindow, vtkRenderWindowInteractor, vtkInteractorStyleTrackballCamera


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("VTK Overlay Example")
        self.setGeometry(100, 100, 800, 600)

        # 创建 VTK 渲染窗口
        self.MainWidget = QWidget()
        self.MainLayout = QVBoxLayout(self.MainWidget)
        self.vtk_widget = QVTKRenderWindowInteractor(self)
        self.setCentralWidget(self.MainWidget)
        self.MainLayout.addWidget(self.vtk_widget)

        # 创建一个按钮，点击它时打开透明的无边框圆角子窗口
        self.button = QPushButton(
            "Open Transparent Rounded Borderless Window", self)
        self.button.clicked.connect(
            self.open_transparent_rounded_borderless_window)

        # 在 VTK 控件中添加立方体和交互器
        self.add_cube_and_interactor()

    def open_transparent_rounded_borderless_window(self):
        transparent_rounded_borderless_window = TransparentRoundedBorderlessWindow(
            self.MainWidget)

        # 设置窗口为 overlay
        transparent_rounded_borderless_window.setWindowFlags(
            Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)

        # 将弹出窗口添加为 VTK 渲染窗口的子控件
        layout = QVBoxLayout(self.vtk_widget)
        layout.addWidget(transparent_rounded_borderless_window)

        transparent_rounded_borderless_window.show()

    def add_cube_and_interactor(self):
        # 创建立方体
        cube_source = vtkCubeSource()

        cube_mapper = vtkPolyDataMapper()
        cube_mapper.SetInputConnection(cube_source.GetOutputPort())

        cube_actor = vtkActor()
        cube_actor.SetMapper(cube_mapper)

        # 创建 VTK 渲染器
        renderer = vtkRenderer()

        # 将立方体添加到渲染器中
        renderer.AddActor(cube_actor)

        # 将渲染器添加到 VTK 渲染窗口中
        self.vtk_widget.GetRenderWindow().AddRenderer(renderer)

        # 创建交互器
        interactor_style = vtkInteractorStyleTrackballCamera()
        render_window_interactor = self.vtk_widget.GetRenderWindow().GetInteractor()
        render_window_interactor.SetInteractorStyle(interactor_style)

        # 渲染
        self.vtk_widget.GetRenderWindow().Render()


class TransparentRoundedBorderlessWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        # 设置无边框窗口、背景透明和圆角
        self.setAttribute(Qt.WA_TranslucentBackground)

        # 添加阴影效果

        # 创建一些内容，这里只是一个关闭按钮
        layout = QVBoxLayout(self)
        close_button = QPushButton("Close", self)
        close_button.setStyleSheet('border-radius:6px;background-color:white;')
        layout.addWidget(close_button)
        self.paintCount = 0

    def paintEvent(self, event):
        if self.paintCount >= 1:
            return

        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # 绘制透明圆角矩形
        rounded_rect = self.rect().adjusted(15, 15, -15, -15)  # 调整矩形大小以便留出阴影空间
        painter.setBrush(QBrush(QColor(0, 0, 0, 0)))
        painter.drawRoundedRect(rounded_rect, 15, 15)
        self.paintCount += 1

    def resizeEvent(self, event):
        self.paintCount = 0


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())
