from __future__ import print_function, absolute_import
from PySide6 import QtGui, QtCore
reserved_words = ['def', '=', 'function', '>=', '<=',
    '<', '>', 'deactivate', 'activate', 'not', 'True',
    'False', 'or', 'and', 'main', 'if', 'else',
    'elif', 'when', 'while', 'end']

# darkOrange = ["\\bdef\\b",
#               "\\bmain\\b",
#
#               "\\bactivate\\b",
#               "\\bdeactivate\\b",
#               "\\bnot\\b",
#               "\\bTrue\\b",
#               "\\bFalse\\b",
#               "\\bor\\b",
#               "\\band\\b",
#               "\\bif\\b",
#               "\\belif\\b",
#               "\\belse\\b",
#               "\\bwhen\\b",
#               "\\bwhile\\b"
#               ]
class Highlighter(QtGui.QSyntaxHighlighter):
    def __init__(self, parent=None, errors=[]):
        super(Highlighter, self).__init__(parent)

        self.errors = errors

        keywordFormat = QtGui.QTextCharFormat()
        keywordFormat.setForeground(QtGui.QBrush(QtGui.QColor(220, 140, 0, 255)))
        keywordsOrange = ["\\bdef\\b",
                      "\\bmain\\b",
                      "\\btry\\b",
                      "\\bexcept\\b",
                      "\\bas\\b",
                      "\\bfrom\\b",
                      "\\bimport\\b",
                      "\\bglobal\\b",
                      "\\bactivate\\b",
                      "\\bdeactivate\\b",
                      "\\bif\\b",
                      "\\belif\\b",
                      "\\belse\\b",
                      "\\bwhen\\b",
                      "\\bwhile\\b",
                      "\\bend\\b",
                      "\\b,\\b",
                      ]
        self.highlightingRules = [(QtCore.QRegularExpression(pattern), keywordFormat) for pattern in keywordsOrange]

        keywordFormatMagenta = QtGui.QTextCharFormat()
        keywordFormatMagenta.setForeground(QtGui.QBrush(QtGui.QColor(230, 0, 162, 255)))
        keywordsMagenta = [
                      "\\bnot\\b",
                      "\\bTrue\\b",
                      "\\bFalse\\b",
                      "\\bor\\b",
                      "\\band\\b"
                      ]
        self.highlightingRules += [(QtCore.QRegularExpression(pattern), keywordFormatMagenta) for pattern in keywordsMagenta]

        numberFormat = QtGui.QTextCharFormat()
        numberFormat.setForeground(QtGui.QBrush(QtGui.QColor(31, 166, 255, 255)))
        self.highlightingRules.append((QtCore.QRegularExpression("\\b[0-9]+.[0-9]+\\b"), numberFormat))
        self.highlightingRules.append((QtCore.QRegularExpression("\\b[0-9]+\\b"), numberFormat))


        singleLineCommentFormat = QtGui.QTextCharFormat()
        singleLineCommentFormat.setForeground(QtCore.Qt.lightGray)
        self.highlightingRules.append((QtCore.QRegularExpression("#[^\n]*"),
                singleLineCommentFormat))

        self.multiLineCommentFormat = QtGui.QTextCharFormat()
        self.multiLineCommentFormat.setForeground(QtCore.Qt.green)

        quotationFormat = QtGui.QTextCharFormat()
        quotationFormat.setForeground(QtCore.Qt.green)
        self.highlightingRules.append((QtCore.QRegularExpression("\".*\""),
                quotationFormat))

        functionFormat = QtGui.QTextCharFormat()
        functionFormat.setFontItalic(False)
        # functionFormat.setForeground(QtGui.QBrush(QtGui.QColor(242, 185, 0, 255)))
        functionFormat.setForeground(QtGui.QBrush(QtGui.QColor(230, 190, 71, 255)))
        self.highlightingRules.append((QtCore.QRegularExpression("\\b[A-Za-z0-9_]+(?=\\()"),
                functionFormat))

        self.commentStartExpression = QtCore.QRegularExpression("'''")
        self.commentEndExpression = QtCore.QRegularExpression("'''")

    def highlightBlock(self, text):
        # Inicializar todo el bloque con el color blanco
        self.setFormat(0, len(text), QtCore.Qt.white)

        # Aplicar las reglas de resaltado
        for pattern, format in self.highlightingRules:
            # Cambiar QRegExp por QRegularExpression
            expression = QtCore.QRegularExpression(pattern)
            match = expression.match(text)
            index = match.capturedStart()
            
            while index >= 0:
                length = match.capturedLength()
                self.setFormat(index, length, format)
                # Buscar la siguiente coincidencia
                match = expression.match(text, index + length)
                index = match.capturedStart()

        self.setCurrentBlockState(0)

        # Manejo de comentarios multilínea
        startIndex = 0
        if self.previousBlockState() != 1:
            startIndex = self.commentStartExpression.match(text).capturedStart()

        while startIndex >= 0:
            endMatch = self.commentEndExpression.match(text, startIndex + 3)
            endIndex = endMatch.capturedStart()

            if endIndex == -1:
                self.setCurrentBlockState(1)
                commentLength = len(text) - startIndex
            else:
                commentLength = endIndex - startIndex + endMatch.capturedLength()

            self.setFormat(startIndex, commentLength, self.multiLineCommentFormat)
            startIndex = self.commentStartExpression.match(text, startIndex + commentLength + 3).capturedStart()