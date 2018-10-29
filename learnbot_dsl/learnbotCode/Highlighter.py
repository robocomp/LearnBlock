from __future__ import print_function, absolute_import
from PySide import QtGui, QtCore
reserved_words = ['def', '=', 'function', '>=', '<=',
    '<', '>', 'deactivate', 'activate', 'not', 'True',
    'False', 'or', 'and', 'main', 'if', 'else',
    'elif', 'when', 'while', 'end']

darkOrange = ["\\bdef\\b",
              "\\bmain\\b",
              "\\bactivate\\b",
              "\\bdeactivate\\b",
              "\\bnot\\b",
              "\\bTrue\\b",
              "\\bFalse\\b",
              "\\bor\\b",
              "\\band\\b",
              "\\bif\\b",
              "\\belif\\b",
              "\\belse\\b",
              "\\bwhen\\b",
              "\\bwhile\\b"
              # "\\b\\b",
              # "\\b\\b",
              # "\\b\\b",
              ]
class Highlighter(QtGui.QSyntaxHighlighter):
    def __init__(self, parent=None):
        # self.parent.
        super(Highlighter, self).__init__(parent)

        # keywordFormat = QtGui.QTextCharFormat()
        # keywordFormat.setForeground(QtCore.Qt.darkBlue)
        # keywordFormat.setFontWeight(QtGui.QFont.Bold)
        #
        # keywordPatterns = ["\\bchar\\b", "\\bclass\\b", "\\bconst\\b",
        #         "\\bdouble\\b", "\\benum\\b", "\\bexplicit\\b", "\\bfriend\\b",
        #         "\\binline\\b", "\\bint\\b", "\\blong\\b", "\\bnamespace\\b",
        #         "\\boperator\\b", "\\bprivate\\b", "\\bprotected\\b",
        #         "\\bpublic\\b", "\\bshort\\b", "\\bsignals\\b", "\\bsigned\\b",
        #         "\\bslots\\b", "\\bstatic\\b", "\\bstruct\\b",
        #         "\\btemplate\\b", "\\btypedef\\b", "\\btypename\\b",
        #         "\\bunion\\b", "\\bunsigned\\b", "\\bvirtual\\b", "\\bvoid\\b",
        #         "\\bvolatile\\b","\\bwhile\\b", "\\bmain\\b", "\\bend\\b",
        #         "\\bif\\b", "\\belif\\b", "\\belse\\b", ]
        #
        # self.highlightingRules = [(QtCore.QRegExp(pattern), keywordFormat) for pattern in keywordPatterns]
        keywordFormat = QtGui.QTextCharFormat()
        keywordFormat.setForeground(QtGui.QBrush(QtGui.QColor(220, 140, 0, 255)))
        # keywordFormat.setFontWeight(QtGui.QFont.Bold)
        keywordsOrange = ["\\bdef\\b",
                      "\\bmain\\b",
                      "\\bactivate\\b",
                      "\\bdeactivate\\b",
                      "\\bif\\b",
                      "\\belif\\b",
                      "\\belse\\b",
                      "\\bwhen\\b",
                      "\\bwhile\\b",
                      "\\bend\\b",
                      "\\b,\\b",
                      # "\\b\\b",
                      ]
        self.highlightingRules = [(QtCore.QRegExp(pattern), keywordFormat) for pattern in keywordsOrange]

        keywordFormatMagenta = QtGui.QTextCharFormat()
        keywordFormatMagenta.setForeground(QtCore.Qt.darkMagenta)
        # keywordFormatMagenta.setFontWeight(QtGui.QFont.Bold)
        keywordsMagenta = [
                      "\\bnot\\b",
                      "\\bTrue\\b",
                      "\\bFalse\\b",
                      "\\bor\\b",
                      "\\band\\b"
                      ]
        self.highlightingRules += [(QtCore.QRegExp(pattern), keywordFormatMagenta) for pattern in keywordsMagenta]

        numberFormat = QtGui.QTextCharFormat()
        # numberFormat.setFontWeight(QtGui.QFont.Bold)
        numberFormat.setForeground(QtGui.QBrush(QtGui.QColor(31, 166, 255, 255)))
        self.highlightingRules.append((QtCore.QRegExp("\\b[0-9]+.*[0-9]+\\b"), numberFormat))
        self.highlightingRules.append((QtCore.QRegExp("\\b[0-9]+\\b"), numberFormat))


        singleLineCommentFormat = QtGui.QTextCharFormat()
        singleLineCommentFormat.setForeground(QtCore.Qt.lightGray)
        self.highlightingRules.append((QtCore.QRegExp("#[^\n]*"),
                singleLineCommentFormat))

        self.multiLineCommentFormat = QtGui.QTextCharFormat()
        self.multiLineCommentFormat.setForeground(QtCore.Qt.darkGreen)

        quotationFormat = QtGui.QTextCharFormat()
        quotationFormat.setForeground(QtCore.Qt.darkGreen)
        self.highlightingRules.append((QtCore.QRegExp("\".*\""),
                quotationFormat))

        functionFormat = QtGui.QTextCharFormat()
        functionFormat.setFontItalic(False)
        # functionFormat.setFontWeight(QtGui.QFont.Bold)
        functionFormat.setForeground(QtGui.QBrush(QtGui.QColor(242, 185, 0, 255)))
        functionFormat.setForeground(QtCore.Qt.darkMagenta)
        self.highlightingRules.append((QtCore.QRegExp("\\b[A-Za-z0-9_]+(?=\\()"),
                functionFormat))

        self.commentStartExpression = QtCore.QRegExp("'''")
        self.commentEndExpression = QtCore.QRegExp("'''")

    def highlightBlock(self, text):
        self.setFormat(0, len(text), QtCore.Qt.white)
        for pattern, format in self.highlightingRules:
            expression = QtCore.QRegExp(pattern)
            index = expression.indexIn(text)
            while index >= 0:
                length = expression.matchedLength()
                self.setFormat(index, length, format)
                index = expression.indexIn(text, index + length)
        self.setCurrentBlockState(0)

        startIndex = 0
        if self.previousBlockState() != 1:
            startIndex = self.commentStartExpression.indexIn(text)
        # print(self.previousBlockState() ,startIndex)
        while startIndex >= 0:
            endIndex = self.commentEndExpression.indexIn(text, startIndex+3)
            print(startIndex, endIndex)
            if endIndex == -1:
                self.setCurrentBlockState(1)
                commentLength = len(text) - startIndex
            else:
                commentLength = endIndex - startIndex + self.commentEndExpression.matchedLength()

            self.setFormat(startIndex, commentLength,self.multiLineCommentFormat)

            startIndex = self.commentStartExpression.indexIn(text, startIndex + commentLength + 3)
