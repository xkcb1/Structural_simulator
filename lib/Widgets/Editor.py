import keyword
from PyQt5.Qsci import QsciScintilla, QsciLexerPython, QsciAPIs
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtWidgets import QFileDialog, QVBoxLayout, QWidget, QPushButton, QLabel, QHBoxLayout
from PyQt5.QtCore import QSize
import sys
import inspect
from PyQt5.QtGui import QColor

from lib.Widgets.tooltip import ToolTipFilter, ToolTipPosition  # 导入 QColor

'''
Default = ... # type: int
Comment = ... # type: int
Number = ... # type: int
DoubleQuotedString = ... # type: int
SingleQuotedString = ... # type: int
Keyword = ... # type: int
TripleSingleQuotedString = ... # type: int
TripleDoubleQuotedString = ... # type: int
ClassName = ... # type: int
FunctionMethodName = ... # type: int
Operator = ... # type: int
Identifier = ... # type: int
CommentBlock = ... # type: int
UnclosedString = ... # type: int
HighlightedIdentifier = ... # type: int
Decorator = ... # type: int
DoubleQuotedFString = ... # type: int
SingleQuotedFString = ... # type: int
TripleSingleQuotedFString = ... # type: int
TripleDoubleQuotedFString = ... # type: int
'''


class CodeEditor(QWidget):
    def __init__(self, parent, theme):
        super(CodeEditor, self).__init__()
        self._parent_ = parent
        self._build_in_ = ['ArithmeticError', 'AssertionError', 'AttributeError', 'BaseException', 'BaseExceptionGroup', 'BlockingIOError', 'BrokenPipeError', 'BufferError', 'BytesWarning', 'ChildProcessError', 'ConnectionAbortedError', 'ConnectionError', 'ConnectionRefusedError', 'ConnectionResetError', 'DeprecationWarning', 'EOFError', 'Ellipsis', 'EncodingWarning', 'EnvironmentError', 'Exception', 'ExceptionGroup', 'False', 'FileExistsError', 'FileNotFoundError', 'FloatingPointError', 'FutureWarning', 'GeneratorExit', 'IOError', 'ImportError', 'ImportWarning', 'IndentationError', 'IndexError', 'InterruptedError', 'IsADirectoryError', 'KeyError', 'KeyboardInterrupt', 'LookupError', 'MemoryError', 'ModuleNotFoundError', 'NameError', 'None', 'NotADirectoryError', 'NotImplemented', 'NotImplementedError', 'OSError', 'OverflowError', 'PendingDeprecationWarning', 'PermissionError', 'ProcessLookupError', 'RecursionError', 'ReferenceError', 'ResourceWarning', 'RuntimeError', 'RuntimeWarning', 'StopAsyncIteration', 'StopIteration', 'SyntaxError', 'SyntaxWarning', 'SystemError',
                           'SystemExit', 'TabError', 'TimeoutError', 'True', 'TypeError', 'UnboundLocalError', 'UnicodeDecodeError', 'UnicodeEncodeError', 'UnicodeError', 'UnicodeTranslateError', 'UnicodeWarning', 'UserWarning', 'ValueError', 'Warning', 'WindowsError', 'ZeroDivisionError', '__build_class__', '__debug__', '__doc__', '__import__', '__loader__', '__name__', '__package__', '__spec__', 'abs', 'aiter', 'all', 'anext', 'any', 'ascii', 'bin', 'bool', 'breakpoint', 'bytearray', 'bytes', 'callable', 'chr', 'classmethod', 'compile', 'complex', 'copyright', 'credits', 'delattr', 'dict', 'dir', 'divmod', 'enumerate', 'eval', 'exec', 'exit', 'filter', 'float', 'format', 'frozenset', 'getattr', 'globals', 'hasattr', 'hash', 'help', 'hex', 'id', 'input', 'int', 'isinstance', 'issubclass', 'iter', 'len', 'license', 'list', 'locals', 'map', 'max', 'memoryview', 'min', 'next', 'object', 'oct', 'open', 'ord', 'pow', 'print', 'property', 'quit', 'range', 'repr', 'reversed', 'round', 'set', 'setattr', 'slice', 'sorted', 'staticmethod', 'str', 'sum', 'super', 'tuple', 'type', 'vars', 'zip']
        self.theme_color_dict = {
            0: {
                'Default': '#abb2bf',
                'Comment': '#5c6370',
                'Number': '#d19a66',
                'DoubleQuotedString': '#98c379',
                'SingleQuotedString': '#98c379',
                'Keyword': '#c678dd',
                'TripleSingleQuotedString': '#98c379',
                'TripleDoubleQuotedString': '#98c379',
                'ClassName': '#e5c07b',
                'FunctionMethodName': '#61afef',
                'Operator': '#e06c75',
                'Identifier': '#abb2bf',
                'CommentBlock': '#5c6370',
                'UnclosedString': '#e06c75',
                'HighlightedIdentifier': '#56b6c2',
                'Decorator': '#61afef',
                'DoubleQuotedFString': '#98c379',
                'SingleQuotedFString': '#98c379',
                'TripleSingleQuotedFString': '#98c379',
                'TripleDoubleQuotedFString': '#98c379',
            },
            1: {
                'Default': '#abb2bf',
                'Comment': '#5c6370',
                'Number': '#d19a66',
                'DoubleQuotedString': '#98c379',
                'SingleQuotedString': '#98c379',
                'Keyword': '#c678dd',
                'TripleSingleQuotedString': '#98c379',
                'TripleDoubleQuotedString': '#98c379',
                'ClassName': '#e5c07b',
                'FunctionMethodName': '#61afef',
                'Operator': '#e06c75',
                'Identifier': '#abb2bf',
                'CommentBlock': '#5c6370',
                'UnclosedString': '#e06c75',
                'HighlightedIdentifier': '#56b6c2',
                'Decorator': '#61afef',
                'DoubleQuotedFString': '#98c379',
                'SingleQuotedFString': '#98c379',
                'TripleSingleQuotedFString': '#98c379',
                'TripleDoubleQuotedFString': '#98c379',
            },
            2: {
                'Default': '#abb2bf',
                'Comment': '#5c6370',
                'Number': '#d19a66',
                'DoubleQuotedString': '#98c379',
                'SingleQuotedString': '#98c379',
                'Keyword': '#c678dd',
                'TripleSingleQuotedString': '#98c379',
                'TripleDoubleQuotedString': '#98c379',
                'ClassName': '#e5c07b',
                'FunctionMethodName': '#61afef',
                'Operator': '#e06c75',
                'Identifier': '#abb2bf',
                'CommentBlock': '#5c6370',
                'UnclosedString': '#e06c75',
                'HighlightedIdentifier': '#56b6c2',
                'Decorator': '#61afef',
                'DoubleQuotedFString': '#98c379',
                'SingleQuotedFString': '#98c379',
                'TripleSingleQuotedFString': '#98c379',
                'TripleDoubleQuotedFString': '#98c379',
            }
        }
        # 创建编辑器
        self.theme = theme
        self.editor = QsciScintilla(self)
        self.editor.setUtf8(True)

        # 设置语法高亮
        self.lexer = QsciLexerPython(self.editor)
        self.editor.setLexer(self.lexer)

        # 启用折叠
        self.editor.setFolding(True)
        # self.editor.setMarginWidth(2, 12)
        # 启用自动补全
        self.api = QsciAPIs(self.lexer)
        self.prepare_auto_completion()
        self.api.prepare()
        self.editor.setCallTipsVisible(-1)
        self.editor.setAutoCompletionSource(
            QsciScintilla.AcsAll)  # 设置为 AcsAll
        self.editor.setAutoCompletionThreshold(2)

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
        self.editor.setStyleSheet('padding:0px;border:0px;margin:0px;')
        #
        self.editor.setAutoCompletionCaseSensitivity(1)
        # 创建布局
        layout = QVBoxLayout(self)
        layout.addWidget(self.editor)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        # bottom widget
        self.BottomWidget = QWidget()
        self.BottomWidget.setFixedHeight(20)
        self.BottomWidget.setStyleSheet(
            'border-bottom-left-radius:5px !important;border-bottom-right-radius:5px !important;')
        self.BottomLayout = QHBoxLayout(self.BottomWidget)
        self.BottomLayout.setContentsMargins(5, 0, 5, 2)
        self.BottomLayout.setSpacing(20)
        # 设置是否显示侧边栏
        self.button_1 = QPushButton()
        self.button_1.setStyleSheet(
            '''*{background-color:rgba(0,0,0,0);border:0px;}
            *:hover {background-color:rgba(125,125,125,0.3);}''')
        self.button_1.setIcon(
            QIcon(f'img/appIcon/{self._parent_.Puretheme}/linenumbers_on.svg'))
        self.button_1.iconPath = 'linenumbers_on.svg'
        self.button_1.setFixedSize(18, 18)
        self.button_1.setIconSize(QSize(20, 20))
        self.button_1.lineNumber = 1
        self._parent_.changeIconList.append(self.button_1)
        self.BottomLayout.addWidget(self.button_1)
        self.button_1.clicked.connect(self.changeLineNumber)
        self.button_1.setToolTip(
            '行号 (是否显示行号)\nDisplay line number')
        self.button_1.installEventFilter(ToolTipFilter(
            self.button_1, 300, ToolTipPosition.TOP_LEFT))
        # 行列
        self.label_1 = QLabel()
        self.label_1.setText('Line 1 , Column 1')
        # language
        self.label_3 = QLabel()
        self.label_3.setText('language : python')
        #
        self.label_2 = QLabel()
        self.label_2.setText('Tab : 4')
        self.BottomLayout.addWidget(self.label_1)
        self.BottomLayout.addStretch(9999)
        self.BottomLayout.addWidget(self.label_2)
        self.BottomLayout.addWidget(self.label_3)

        layout.addWidget(self.BottomWidget)
        self.editor.cursorPositionChanged.connect(self.updateBottomWidget)
        # 设置主题色
        self.setTheme(self.theme)

    def changeLineNumber(self):
        if self.button_1.lineNumber == 1:
            self.button_1.lineNumber = 0
            self.button_1.setIcon(
                QIcon(f'img/appIcon/{self._parent_.thisTheme}/linenumbers_off.svg'))
            self.button_1.iconPath = 'linenumbers_off.svg'
            self.editor.setMarginWidth(0, 0)
        else:
            self.button_1.lineNumber = 1
            self.button_1.setIcon(
                QIcon(f'img/appIcon/{self._parent_.thisTheme}/linenumbers_on.svg'))
            self.button_1.iconPath = 'linenumbers_on.svg'
            self.editor.setMarginWidth(0, '00000')

    def updateBottomWidget(self, a, b):
        # a行号，b列号
        self.label_1.setText(f'Line {a+1} , Column {b+1}')

    def setTheme(self, theme):
        if theme == 0:
            # dark
            # 设置编辑器底纹颜色
            self.lexer.setDefaultPaper(QColor("#232323"))
            self.lexer.setDefaultColor(QColor("#232323"))
            self.lexer.setPaper(QColor('#232323'), -1)
            self.lexer.setFont(QFont("Consolas", 13, QFont.Normal), -1)
            # 开始改变前景色
            for color in self.theme_color_dict[theme]:
                self.lexer.setColor(
                    QColor(self.theme_color_dict[theme][color]), eval('QsciLexerPython.'+color))
            self.editor.setMarginsBackgroundColor(QColor("#1d1d1d"))
            self.editor.setMarginsForegroundColor(QColor("#aaa"))
            # 设置编辑器边缘背景色
            self.editor.setCaretLineVisible(1)
            self.editor.setCaretLineBackgroundColor(QColor('#2c2d2f'))
            self.editor.setCaretForegroundColor(QColor('#61afef'))
            self.editor.setCaretWidth(2)
        elif theme == 1:
            # light
            # dark
            # 设置编辑器底纹颜色
            self.lexer.setDefaultPaper(QColor("#313133"))
            self.lexer.setDefaultColor(QColor("#313133"))
            self.lexer.setPaper(QColor('#313133'), -1)
            self.lexer.setColor(QColor("#eee"), -1)
            # 开始改变前景色
            for color in self.theme_color_dict[theme]:
                self.lexer.setColor(
                    QColor(self.theme_color_dict[theme][color]), eval('QsciLexerPython.'+color))
            self.editor.setMarginsBackgroundColor(QColor("#414143"))
            self.editor.setMarginsForegroundColor(QColor("#aaa"))
            self.editor.setCaretWidth(2)
            # 设置编辑器边缘背景色
            self.editor.setCaretLineVisible(1)
            self.editor.setCaretLineBackgroundColor(QColor('#555'))
            self.editor.setCaretForegroundColor(QColor('#aaa'))
        elif theme == 2:
            # gray
            # dark
            # 设置编辑器底纹颜色
            self.lexer.setDefaultPaper(QColor("#303031"))
            self.lexer.setDefaultColor(QColor("#303031"))
            self.lexer.setPaper(QColor('#303031'), -1)
            self.lexer.setColor(QColor("#eee"), -1)
            # 开始改变前景色
            for color in self.theme_color_dict[theme]:
                self.lexer.setColor(
                    QColor(self.theme_color_dict[theme][color]), eval('QsciLexerPython.'+color))
            self.editor.setMarginsBackgroundColor(QColor("#3a3b3c"))
            self.editor.setMarginsForegroundColor(QColor("#bbb"))
            self.editor.setCaretWidth(2)
            # 设置编辑器边缘背景色
            self.editor.setCaretLineVisible(1)
            self.editor.setCaretLineBackgroundColor(QColor('#373839'))
            self.editor.setCaretForegroundColor(QColor('#61afef'))

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
