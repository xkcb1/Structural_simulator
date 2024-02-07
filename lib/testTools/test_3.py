import keyword
from pygments.lexers import PythonLexer
from PyQt5.Qsci import QsciScintilla, QsciLexerPython, QsciAPIs
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QVBoxLayout, QWidget, QAction, QSplitter
import sys
import inspect
from PyQt5.QtGui import QColor  # 导入 QColor


class CodeEditor(QMainWindow):
    def __init__(self):
        super(CodeEditor, self).__init__()
        self._build_in_ = ['ArithmeticError', 'AssertionError', 'AttributeError', 'BaseException', 'BaseExceptionGroup', 'BlockingIOError', 'BrokenPipeError', 'BufferError', 'BytesWarning', 'ChildProcessError', 'ConnectionAbortedError', 'ConnectionError', 'ConnectionRefusedError', 'ConnectionResetError', 'DeprecationWarning', 'EOFError', 'Ellipsis', 'EncodingWarning', 'EnvironmentError', 'Exception', 'ExceptionGroup', 'False', 'FileExistsError', 'FileNotFoundError', 'FloatingPointError', 'FutureWarning', 'GeneratorExit', 'IOError', 'ImportError', 'ImportWarning', 'IndentationError', 'IndexError', 'InterruptedError', 'IsADirectoryError', 'KeyError', 'KeyboardInterrupt', 'LookupError', 'MemoryError', 'ModuleNotFoundError', 'NameError', 'None', 'NotADirectoryError', 'NotImplemented', 'NotImplementedError', 'OSError', 'OverflowError', 'PendingDeprecationWarning', 'PermissionError', 'ProcessLookupError', 'RecursionError', 'ReferenceError', 'ResourceWarning', 'RuntimeError', 'RuntimeWarning', 'StopAsyncIteration', 'StopIteration', 'SyntaxError', 'SyntaxWarning', 'SystemError',
                           'SystemExit', 'TabError', 'TimeoutError', 'True', 'TypeError', 'UnboundLocalError', 'UnicodeDecodeError', 'UnicodeEncodeError', 'UnicodeError', 'UnicodeTranslateError', 'UnicodeWarning', 'UserWarning', 'ValueError', 'Warning', 'WindowsError', 'ZeroDivisionError', '__build_class__', '__debug__', '__doc__', '__import__', '__loader__', '__name__', '__package__', '__spec__', 'abs', 'aiter', 'all', 'anext', 'any', 'ascii', 'bin', 'bool', 'breakpoint', 'bytearray', 'bytes', 'callable', 'chr', 'classmethod', 'compile', 'complex', 'copyright', 'credits', 'delattr', 'dict', 'dir', 'divmod', 'enumerate', 'eval', 'exec', 'exit', 'filter', 'float', 'format', 'frozenset', 'getattr', 'globals', 'hasattr', 'hash', 'help', 'hex', 'id', 'input', 'int', 'isinstance', 'issubclass', 'iter', 'len', 'license', 'list', 'locals', 'map', 'max', 'memoryview', 'min', 'next', 'object', 'oct', 'open', 'ord', 'pow', 'print', 'property', 'quit', 'range', 'repr', 'reversed', 'round', 'set', 'setattr', 'slice', 'sorted', 'staticmethod', 'str', 'sum', 'super', 'tuple', 'type', 'vars', 'zip']
        # 创建编辑器
        self.editor = QsciScintilla(self)
        self.editor.setUtf8(True)

        # 设置语法高亮
        lexer = QsciLexerPython(self.editor)
        self.editor.setLexer(lexer)

        # 启用折叠
        self.editor.setFolding(True)
        # self.editor.setMarginWidth(2, 12)

        # 启用自动补全
        self.api = QsciAPIs(lexer)
        self.prepare_auto_completion()
        self.api.prepare()
        self.editor.setCallTipsVisible(-1)

        self.editor.setAutoCompletionSource(
            QsciScintilla.AcsAll)  # 设置为 AcsAll
        self.editor.setAutoCompletionThreshold(2)

        # 设置背景色
        # 设置编辑器底纹颜色
        lexer.setDefaultPaper(QColor("#222"))
        lexer.setDefaultColor(QColor("#222"))
        lexer.setPaper(QColor('#222'), QsciLexerPython.Number)
        lexer.setColor(QColor("#eee"), -1)
        '''self.editor.SendScintilla(
            QsciScintilla.SCI_STYLESETFONT, 1, 'Helvetica')'''

        # 设置编辑器边缘背景色
        self.editor.setMarginsBackgroundColor(QColor("#333"))
        self.editor.setMarginsForegroundColor(QColor("#aaa"))
        #

        # 启用缩进
        self.editor.setIndentationWidth(4)
        self.editor.setIndentationsUseTabs(True)
        self.editor.setTabWidth(4)
        self.editor.setIndentationGuides(True)
        self.editor.setAutoIndent(True)
        self.editor.setMarginWidth(0, "00000")
        self.editor.setMarginType(0, QsciScintilla.NumberMargin)
        self.editor.setMargins(1)
        #
        self.editor.setAutoCompletionCaseSensitivity(1)

        # 创建预览编辑器
        self.preview_editor = QsciScintilla(self)
        self.preview_editor.setReadOnly(True)
        self.preview_editor.setUtf8(True)
        self.preview_editor.setMarginWidth(1, 0)

        # 设置预览编辑器的语法高亮
        preview_lexer = QsciLexerPython(self.preview_editor)
        self.preview_editor.setLexer(preview_lexer)

        # 设置字体大小为4
        font = QFont()
        font.setPointSize(2)
        preview_lexer.setFont(font)

        # 创建布局
        layout = QVBoxLayout()
        splitter = QSplitter()

        splitter.addWidget(self.editor)
        splitter.addWidget(self.preview_editor)

        layout.addWidget(splitter)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        # 创建菜单栏
        menubar = self.menuBar()
        file_menu = menubar.addMenu('File')

        # 添加打开动作
        open_action = QAction('Open', self)
        open_action.triggered.connect(self.open_file)
        file_menu.addAction(open_action)

        # 监听编辑器内容变化，更新预览
        self.editor.textChanged.connect(self.update_preview)

        # 同步滚动条
        self.editor.verticalScrollBar().valueChanged.connect(self.sync_scrollbar)
        self.preview_editor.verticalScrollBar().valueChanged.connect(self.sync_scrollbar)

    def open_file(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        file_path, _ = QFileDialog.getOpenFileName(
            self, 'Open File', '', 'Python Files (*.py);;All Files (*)', options=options)

        if file_path:
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
                self.editor.setText(content)
                self.update_preview()

    def update_preview(self):
        # 更新预览编辑器的内容
        preview_content = self.editor.text()
        self.preview_editor.setText(preview_content)

    def sync_scrollbar(self, value):
        # 同步滚动条位置
        self.editor.verticalScrollBar().setValue(value)
        self.preview_editor.verticalScrollBar().setValue(value)

    def prepare_auto_completion(self):
        # 获取 Python 的关键字和内建函数
        for kw in keyword.kwlist:
            self.api.add(kw)

        for name in self._build_in_:
            if inspect.isroutine(eval(name)):
                # 如果是函数
                try:
                    sig = inspect.signature(eval(name))
                    OutName = name + str(sig)
                except:
                    OutName = name
            elif inspect.isclass(eval(name)):
                # 如果是函数
                try:
                    init_func = getattr(eval(name), "__init__")
                    sig = inspect.signature(init_func)
                    OutName = name + str(sig)
                except:
                    OutName = name
            else:
                OutName = name
            self.api.add(OutName)

    def keyPressEvent(self, event):
        # 处理按键事件
        if event.key() == 32 and event.modifiers() == 16777249:  # Check for Ctrl+Space
            self.editor.autoComplete()


int()
app = QApplication(sys.argv)
editor = CodeEditor()
editor.show()
sys.exit(app.exec_())
