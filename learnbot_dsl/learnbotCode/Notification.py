from learnbot_dsl.learnbotCode.CodeEdit import *
from learnbot_dsl.learnbotCode.Highlighter import *
from enum import Enum, auto
from PySide2 import QtWidgets

class Severity(Enum):
    WARNING = auto()
    ERROR = auto()

class Notification(QtWidgets.QWidget):
    resized = QtCore.Signal()

    def __init__(self, src, start, end = None, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.HINT = self.tr('Hint')
        self.src = src

        self.vLayout = QtWidgets.QVBoxLayout()
        self.setLayout(self.vLayout)

        self.summaryLayout = QtWidgets.QHBoxLayout()
        self.vLayout.addLayout(self.summaryLayout)

        self.icon = QtWidgets.QLabel()
        self.icon.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Ignored)
        self.summaryLayout.addWidget(self.icon)

        self._message = ''
        self.messageWidget = QtWidgets.QLabel()
        self.messageWidget.setWordWrap(True)
        font = self.messageWidget.font()
        font.setBold(True)
        self.messageWidget.setFont(font)
        self.summaryLayout.addWidget(self.messageWidget)

        self.position = QtWidgets.QLabel()
        font = self.position.font()
        font.setItalic(True)
        self.position.setFont(font)
        self.vLayout.addWidget(self.position)

        self.snippet = CodeEdit()
        self.snippet.setReadOnly(True)
        font = QtGui.QFont()
        font.setFamily('Courier')
        font.setFixedPitch(True)

        self.snippet.setFont(font)
        self.snippet.setReadOnly(True)
        self.snippet.setOffset(start[1]-1)
        self.vLayout.addWidget(self.snippet)

        self._hints = []
        self.hintsWidget = QtWidgets.QVBoxLayout()
        self.vLayout.addLayout(self.hintsWidget)

        self.highlighter = Highlighter(self.snippet.document())
        self.setPosition(start, end)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.fitSnippetToContent()

    def fitSnippetToContent(self):
        margins = self.snippet.contentsMargins()
        height = self.snippet.document().documentMargin() * 2 \
                + margins.top() \
                + margins.bottom()

        for line in range(self.snippet.blockCount()):
            block = self.snippet.document().findBlock(line)
            height += self.snippet.blockBoundingRect(block).height()

        if self.snippet.horizontalScrollBar().isVisible():
            height += self.snippet.horizontalScrollBar().height()

        self.snippet.setFixedHeight(height)
        self.resized.emit()

    def setSeverity(self, severity):
        if severity == Severity.ERROR:
            icon = QtGui.QIcon.fromTheme('dialog-error')
        elif severity == Severity.WARNING:
            icon = QtGui.QIcon.fromTheme('dialog-warning')

        self.icon.setPixmap(icon.pixmap(QtCore.QSize(16, 16)))

    def message(self):
        return self._message

    def setMessage(self, message):
        self._message = message
        self.messageWidget.setText(message)

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
            snippet = self.src.split('\n')[start[0]-1]

        self.position.setText(position)
        self.snippet.setPlainText(snippet)

    def hints(self):
        return self._hints

    def setHints(self, hints):
        self._hints = hints

        for _ in range(self.hintsWidget.count()):
            self.vLayout.itemAt().widget().setParent(None)

        for hint in hints:
               item = QtWidgets.QLabel(self)
               item.setText('<b>' + self.HINT + '</b>: ' + hint)
               self.hintsWidget.addWidget(item)

    def simpleHtml(self):
        tooltip = '<h2>' + self._message + '</h2>'
        tooltip += '<ul>'

        for hint in self._hints:
            tooltip += self.tr('<li><b>Hint:</b> ') + hint + '</li>'

        tooltip += '</ul>'
        return tooltip

class InvalidSyntax(Notification):
    def __init__(self, rule, *args, **kwargs):
        super().__init__(*args, **kwargs)

        hints = [
            self.tr('did you forget something while making the <code>%s</code>?') % rule.__name__,
        ]

        self.setSeverity(Severity.ERROR)
        self.setMessage(self.tr('Invalid syntax'))
        self.setHints(hints)

class TypeMismatch(Notification):
    def __init__(self, expected, got, *args, **kwargs):
        super().__init__(*args, **kwargs)

        hints = [
            self.tr('check the marked expression: does it really return a value of type <code>%s</code>?') % expected,
            self.tr('did you make a typo while making the expression? Check the operators!'),
            self.tr('be careful with operator precedence!'),
        ]

        self.setSeverity(Severity.WARNING)
        self.setMessage(self.tr('Type mismatch: expected %s, got %s') % (expected, got))
        self.setHints(hints)