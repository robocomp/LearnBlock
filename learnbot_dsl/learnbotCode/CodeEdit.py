from PySide2 import QtWidgets, QtGui, QtCore
from math import log10, ceil

class CodeEdit(QtWidgets.QPlainTextEdit):
    class LineNumberArea(QtWidgets.QWidget):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self._offset = 1
            self._count = 0
            self._fontScale = 0.8

        def sizeHint(self):
            lastLine = self._offset + self._count
            digits = ceil(log10(lastLine))
            metrics = QtGui.QFontMetrics(self.font())
            margins = self.contentsMargins()
            width = margins.left() + margins.right() + metrics.horizontalAdvance('9' * digits)

            return QtCore.QSize(width, -1)

        def paintEvent(self, event):
            parent = self.parentWidget()
            painter = QtGui.QPainter(self)
            background = self.palette().color(QtGui.QPalette.Background)
            foreground = self.palette().color(QtGui.QPalette.Foreground)
            painter.fillRect(event.rect(), background)

            block = parent.firstVisibleBlock()
            number = block.blockNumber() + self.offset()
            top = parent.blockBoundingGeometry(block).translated(parent.contentOffset()).top()
            bottom = top + parent.blockBoundingRect(block).height()

            font = parent.font()
            font.setPointSizeF(font.pointSizeF() * self._fontScale)
            painter.setFont(font)

            while block.isValid() and top <= event.rect().bottom():
                if block.isVisible() and bottom >= event.rect().top():
                    width = self.sizeHint().width()
                    height = parent.fontMetrics().height()

                    painter.setPen(foreground)
                    painter.drawText(0, top + height * ((1 - self._fontScale) / 2),
                            width - self.contentsMargins().right(), height,
                            QtGui.Qt.AlignRight, str(number))

                block = block.next()
                top = bottom
                bottom = top + parent.blockBoundingRect(block).height()
                number += 1

            painter.end()

        def count(self):
            return self._count

        def setCount(self, count):
            self._count = count

        def offset(self):
            return self._offset

        def setOffset(self, offset):
            self._offset = offset

        def fontScale(self):
            return self._fontScale

        def setFontScale(self, fontScale):
            self._fontScale = fontScale

    def __init__(self, *args, **kwargs):
        super().__init__(*args, *kwargs)

        self.lineNumbers = CodeEdit.LineNumberArea(self)
        self.lineNumbers.setContentsMargins(QtCore.QMargins(4, 0, 4, 0))
        p = self.palette()
        self.lineNumbers.setPalette(p)
        self.textChanged.connect(self.updateLineCount)

        self.blockCountChanged.connect(self.updateLineCount)
        self.updateRequest.connect(self.updateLineNumbers)
        self.cursorPositionChanged.connect(self.highlightCurrentLine)

        self.errorSels = []

        self.lineSel = QtWidgets.QTextEdit.ExtraSelection()
        self.lineSel.format.setBackground(QtGui.QColor(255, 255, 0, 16))
        self.lineSel.format.setProperty(QtGui.QTextFormat.FullWidthSelection, True)
        self.lineSel.cursor = self.textCursor()
        self.lineSel.cursor.clearSelection()
        self.updateSelections()

    def offset(self):
        return self.lineNumbers.offset()

    def setOffset(self, offset):
        self.lineNumbers.setOffset(offset)

    def updateLineCount(self):
        self.lineNumbers.setCount(self.document().blockCount())
        self.setViewportMargins(self.lineNumbers.sizeHint().width(), 0, 0, 0)

    def updateLineNumbers(self, rect, dy):
        if dy:
            self.lineNumbers.scroll(0, dy)
        else:
            size = self.lineNumbers.sizeHint()
            self.lineNumbers.update(0, rect.y(), size.width(), rect.height())

        if rect.contains(self.viewport().rect()):
            self.updateLineCount()

    def highlightCurrentLine(self):
        if not self.isReadOnly():
            self.lineSel.cursor = self.textCursor()
            self.lineSel.cursor.clearSelection()

            self.updateSelections()

    def clearErrorHighlight(self):
        self.errorSels = []
        self.updateSelections()

    def addErrorHighlight(self, start, end):
        errorSel = QtWidgets.QTextEdit.ExtraSelection()
        errorSel.format.setBackground(QtGui.QColor(255, 0, 0, 16))
        errorSel.format.setProperty(QtGui.QTextFormat.TextUnderlineColor, QtGui.QColor(255, 0, 0))
        errorSel.format.setProperty(QtGui.QTextFormat.TextUnderlineStyle, QtGui.QTextCharFormat.UnderlineStyle.SpellCheckUnderline)
        errorSel.cursor = QtGui.QTextCursor(self.document())
        errorSel.cursor.setPosition(start)
        errorSel.cursor.setPosition(end, QtGui.QTextCursor.KeepAnchor)
        self.errorSels.append(errorSel)

        self.updateSelections()

    def updateSelections(self):
        selections = self.errorSels.copy()

        if not self.isReadOnly():
            selections.append(self.lineSel)

        self.setExtraSelections(selections)

    def setFont(self, font):
        super().setFont(font)
        self.lineNumbers.setFont(font)

    def setReadOnly(self, ro):
        super().setReadOnly(ro)
        self.updateSelections()

    def resizeEvent(self, event):
        super().resizeEvent(event)

        cr = self.contentsRect()
        width = self.lineNumbers.sizeHint().width()
        self.lineNumbers.setGeometry(QtCore.QRect(cr.left(), cr.top(), width, cr.height()))