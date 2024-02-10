from PyQt5.QtWidgets import QApplication, QMainWindow, QComboBox

app = QApplication([])

# 创建一个主窗口
main_window = QMainWindow()

# 创建一个 QComboBox 作为菜单栏的小部件
combo_box = QComboBox()
combo_box.addItem("Option 1")
combo_box.addItem("Option 2")
combo_box.addItem("Option 3")

# 将 QComboBox 设置为主窗口的菜单栏
main_window.setMenuWidget(combo_box)

main_window.show()
app.exec_()
