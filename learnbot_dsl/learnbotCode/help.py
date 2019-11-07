# -*- coding: utf-8 -*-
from __future__ import print_function
import learnbot_dsl
from learnbot_dsl.guis.help import *
from PySide2 import QtCore, QtGui, QtWebEngineWidgets, QtWidgets
import sys, os, markdown
# path = os.path.dirname(os.path.realpath(__file__))
from builtins import str
from io import open
class MarkdownView(QtWebEngineWidgets.QWebEngineView):

    def __init__(self):
        QtWebEngineWidgets.QWebEngineView.__init__(self)

def decode(string, encoding):
    try:
        return u"".join(string.decode(encoding))
    except:
        return string

def encode(string, encoding):
    try:
        return u"".join(string.encode(encoding))
    except:
        return string

class helper(Ui_Help,QtWidgets.QDialog):

    def __init__(self, Lang):
        Ui_Help.__init__(self)
        QtWidgets.QDialog.__init__(self)
        self.setupUi(self)
        self.webView = MarkdownView()
        self.webView.setUrl(QtCore.QUrl("about:blank"))

        self.layoutWebKit.addWidget(self.webView)
        self.dictDocs = {}
        self.absModel = QtCore.QAbstractListModel
        self.hidePath = os.path.join(os.environ["HOME"], ".learnblock", "mdfiles")
        paths = os.path.dirname(learnbot_dsl.__file__)+ ":" + os.environ["XDG_DATA_DIRS"]
        curItem = None
        for sharepath in paths.split(":"):
            if os.path.exists(os.path.join(sharepath,"mdfiles")):
                # print(sharepath)
                self.sharePath = os.path.join(sharepath, "mdfiles")
                # self.css = open(os.path.join(self.sharePath, "styles.css"), "r").read()
                self.css = os.path.join(self.sharePath, "styles.css")
                curItem = os.path.join(self.sharePath, Lang)
                if os.path.exists(curItem):
                    self.treeWidget.addTopLevelItems(self.getItems(os.path.join(self.sharePath, Lang)))
                    break
        self.treeWidget.itemClicked.connect(self.load_MarkDonw)
        self.load_MarkDonw(self.treeWidget.topLevelItem(0), 0)
        if curItem is not None and os.path.exists(curItem):
            self.empty = False
        else:
            self.empty = True

        self.pushButtonPrevious.clicked.connect(self.webView.back)
        self.pushButtonNext.clicked.connect(self.webView.forward)

    def getItems(self,path_):
        listItems = []
        for name in os.listdir(path_):
            absPath = os.path.join(path_, name)
            # name = u"".join(name.decode("utf-8"))
            name = decode(name, "utf-8")
            if os.path.isdir(absPath):
                item = QtWidgets.QTreeWidgetItem()
                item.setText(0, name)
                if os.path.exists(os.path.join(absPath, "README.md")):
                    self.dictDocs[item] = self.generateHTMLFile(os.path.join(absPath, "README.md"))
                listItems.append(item)
                item.addChildren(self.getItems(absPath))
            elif os.path.splitext(absPath)[-1] == ".md" and name != "README.md":
                item = QtWidgets.QTreeWidgetItem()
                self.dictDocs[item] = self.generateHTMLFile(absPath)
                item.setText(0, os.path.splitext(name)[0])
                listItems.append(item)
        # return listItems
        return sorted(listItems, key=lambda a: a.text(0))

    def createHideDir(self, path, isredy=False):
        if not isredy:
            path = path[path.rfind("learnbot_dsl/") + len("learnbot_dsl/"):]
            path = os.path.join(os.environ["HOME"], ".learnblock", path)
        if not os.path.exists(path):
            try:
                os.mkdir(path)
            except:
                self.createHideDir(os.path.dirname(path), isredy=True)
                os.mkdir(path)

    def getHidePath(self, path_):
        htmlPath = os.path.splitext(path_)[0]
        htmlPath = htmlPath[htmlPath.rfind("learnbot_dsl/") + len("learnbot_dsl/"):]
        htmlPath = os.path.join(os.environ["HOME"], ".learnblock", htmlPath)
        return htmlPath

    def generateHTMLFile(self,path_):
        htmlPath = self.getHidePath(path_) + ".html"
        if not os.path.exists(htmlPath) or os.path.getmtime(path_) > os.path.getmtime(htmlPath) or True:
            text = open(path_, "r").read().replace("<hidepath>", self.hidePath).replace("<sharepath>", self.sharePath)
            text = decode(text, "utf-8")
            content = ''.join([
                "<html><head>",
                '<meta http-equiv="Content-Type" content="text/html; charset=utf-8"/>',
                '<link rel="stylesheet" type="text/css" href="file://'+ self.css +'">'
                "</head><body>",
                markdown.markdown(text),
                "</body></html>"
            ])
            content = encode(content, "utf-8")
            if not os.path.exists(os.path.dirname(htmlPath)):
                self.createHideDir(os.path.dirname(htmlPath),isredy=True)
            with open(htmlPath, "w") as f:
                f.write(content)
        return htmlPath

    def load_MarkDonw(self, item, column_no):
        if item in self.dictDocs:
            path = decode(self.dictDocs[item], "utf-8")
            self.webView.load(QtCore.QUrl("file://"+path))

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)

    h =helper("ES")
    h.show()
    sys.exit(app.exec_())
