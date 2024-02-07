import sys
from PyQt5.QtCore import QTextCodec, QEvent, Qt, QProcess
from PyQt5.QtGui import QTextCursor
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QTextEdit, QWidget, QPushButton


class MainWindow(QWidget):
    def __init__(self):
        super(MainWindow, self).__init__()
        if sys.platform.startswith('win'):
            self.TerminalCommand = 'cmd'
        elif sys.platform.startswith('darwin'):
            self.TerminalCommand = 'open -a Terminal'
        elif sys.platform.startswith('linux'):
            print("gnome-termina")
        # 创建控件
        self.console_text = QTextEdit(self)
        self.cmd_process = QProcess(self)

        # 设置文本框可编辑
        self.console_text.setReadOnly(False)

        # 安装事件过滤器
        self.console_text.installEventFilter(self)

        # 创建布局
        layout = QVBoxLayout()
        layout.addWidget(self.console_text)

        self.start_cmd()

        # 创建主窗口部件
        central_widget = QWidget(self)
        central_widget.setLayout(layout)
        self.LastOutPut = 0

        # 设置主窗口
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.console_text)

    def start_cmd(self):
        # 启动 cmd 进程
        self.cmd_process.start(self.TerminalCommand, mode=QProcess.ReadWrite)
        # 连接 cmd 输出到文本框
        self.cmd_process.readyReadStandardOutput.connect(self.read_cmd_output)
        self.cmd_process.readyReadStandardError.connect(self.read_cmd_output)

    def read_cmd_output(self):
        # 读取 cmd 输出并显示在文本框中
        output = QTextCodec.codecForLocale().toUnicode(
            self.cmd_process.readAllStandardOutput())
        error_output = QTextCodec.codecForLocale().toUnicode(
            self.cmd_process.readAllStandardError())
        print(output)
        self.append_text_to_console(error_output)
        self.append_text_to_console(output)

    def append_text_to_console(self, text):
        try:
            if text == '':
                return
            elif text[-1] == '\n':
                text = text[:-1]
        except:
            pass
        # 将文本追加到文本框中
        self.console_text.append(text)
        cursor = self.console_text.textCursor()
        cursor.movePosition(QTextCursor.End)
        self.console_text.setTextCursor(cursor)
        self.LastOutPut = len(self.console_text.toPlainText())

    def eventFilter(self, source, event):
        if source is self.console_text and event.type() == QEvent.KeyPress:
            key = event.key()
            modifiers = event.modifiers()
            cursor = self.console_text.textCursor()
            # 检测回车键
            if key == Qt.Key_Return and not modifiers:

                # 获取当前光标之前的文本
                cursor.select(QTextCursor.BlockUnderCursor)
                selected_text = cursor.selectedText()
                selected_text = ''.join(selected_text.split('>')[1:])
                # print(f"{selected_text}\n".encode('utf-8'))
                # 发送用户输入给 cmd 进程
                self.cmd_process.write(f"{selected_text}\n".encode('utf-8'))

                # 阻止回车键的默认行为
                return True
            # 检查光标是否在文本末尾

            elif cursor.position() != cursor.document().characterCount() - 1:
                return True
            # 检测删除键
            elif key == Qt.Key_Backspace and not modifiers:
                cursor = self.console_text.textCursor()
                # print(f'this: {cursor.position()}', f'last: {self.LastOutPut}')
                # 检查删除动作的起始位置是否在之前的输出部分
                if cursor.position() <= self.LastOutPut:
                    return True

        return super().eventFilter(source, event)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
