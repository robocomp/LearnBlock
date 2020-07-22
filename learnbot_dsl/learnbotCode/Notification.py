from learnbot_dsl.learnbotCode.Highlighter import *
from enum import Enum, auto
from PySide2 import QtWidgets

class Severity(Enum):
    WARNING = auto()
    ERROR = auto()

MESSAGE_STYLE = '''
font-weight: bold;
'''

POSITION_STYLE = '''
font-style: italic;
'''

SNIPPET_STYLE = '''
font-family: Courier, monospace;
color: white;
'''

class Notification(QtWidgets.QWidget):
    def __init__(self, src, start, end = None, parent = None):
        super().__init__(parent)

        self.src = src

        self.vLayout = QtWidgets.QVBoxLayout()
        self.setLayout(self.vLayout)

        self.summaryLayout = QtWidgets.QHBoxLayout()
        self.vLayout.addLayout(self.summaryLayout)

        self.icon = QtWidgets.QLabel()
        self.icon.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Ignored)
        self.summaryLayout.addWidget(self.icon)

        self.message = QtWidgets.QLabel()
        self.message.setWordWrap(True)
        self.message.setStyleSheet(MESSAGE_STYLE)
        self.summaryLayout.addWidget(self.message)

        self.position = QtWidgets.QLabel()
        self.position.setStyleSheet(POSITION_STYLE)
        self.vLayout.addWidget(self.position)

        self.snippet = QtWidgets.QTextEdit()
        self.snippet.setReadOnly(True)
        self.snippet.setStyleSheet(SNIPPET_STYLE)
        p = self.snippet.palette()
        p.setColor(self.snippet.viewport().backgroundRole(), QtGui.QColor(51, 51, 51, 255))
        self.snippet.setPalette(p)
        self.vLayout.addWidget(self.snippet)

        self.highlighter = Highlighter(self.snippet)
        self.setPosition(start, end)

    def setSeverity(self, severity):
        if severity == Severity.ERROR:
            icon = QtGui.QIcon.fromTheme('dialog-error')
        elif severity == Severity.WARNING:
            icon = QtGui.QIcon.fromTheme('dialog-warning')

        self.icon.setPixmap(icon.pixmap(QtCore.QSize(16, 16)))

    def setMessage(self, message):
        self.message.setText(message)

    def setPosition(self, start, end = None):
        self.start = start
        self.end = end

        if end:
            params = (start[0], start[1], end[0], end[1])
            lines = end[0] - start[0] + 1
            position = self.tr('at %s:%s—%s:%s') % params
            snippet = '\n'.join(self.src.split('\n')[start[0]-1:end[0]])
        else:
            params = (start[0], start[1])
            lines = 1
            position = self.tr('at %s:%s') % params
            snippet = '\n'.join(self.src.split('\n')[start[0]-1])

        self.position.setText(position)
        self.snippet.setText(snippet)

        snippetDoc = self.snippet.document()
        metrics = QtGui.QFontMetrics(snippetDoc.defaultFont())
        margins = self.snippet.contentsMargins()
        height = metrics.lineSpacing() * lines \
                + snippetDoc.documentMargin() * 2 \
                + margins.top() \
                + margins.bottom()

        self.snippet.setFixedHeight(height)

class ParseError(Notification):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setSeverity(Severity.ERROR)
        self.setMessage(self.tr('Parse error'))

class TypeMismatch(Notification):
    def __init__(self, expected, got, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setSeverity(Severity.WARNING)
        self.setMessage(self.tr('Type mismatch: expected %s, got %s') % (expected, got))