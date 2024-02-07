import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QFrame
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QWindow
import win32gui


class MinecraftWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # 获取 Minecraft 窗口句柄
        minecraft_handle = win32gui.FindWindow(None, "Minecraft 1.20.1")

        if minecraft_handle:
            # 将 Minecraft 窗口嵌入到 PyQt5 窗口中
            self.minecraft_window = QWindow.fromWinId(minecraft_handle)
            self.minecraft_window.setFlags(Qt.Widget)
            self.minecraft_window.create()

            # 创建窗口容器（使用 QWidget 替代 QWindowContainer）
            container = QWidget.createWindowContainer(self.minecraft_window)

            # 设置主窗口属性
            self.setCentralWidget(container)
            self.setGeometry(100, 100, 800, 600)
            self.show()
        else:
            print("Minecraft窗口未找到")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    minecraft_app = MinecraftWindow()
    sys.exit(app.exec_())
