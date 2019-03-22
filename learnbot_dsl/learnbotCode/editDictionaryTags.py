from learnbot_dsl.guis.EditDictionaryTags import Ui_EditDictionaryTags
from PySide2.QtWidgets import QApplication, QDialog, QLineEdit, QFileDialog
from PySide2.QtGui import QIntValidator
import sys, json, os

pathAprildict = os.path.join(os.getenv('HOME'), ".learnblock", "AprilDict.json")


class EditDictionaryTags(QDialog):

    def __init__(self, parent=None):
        super(EditDictionaryTags, self).__init__(parent)
        self.createUI()

    def createUI(self):
        self.ui = Ui_EditDictionaryTags()
        self.ui.setupUi(self)
        self.ui.add_pushButton.clicked.connect(self.addRow)
        self.ui.delete_pushButton.clicked.connect(self.deleteRow)
        self.ui.ok_pushButton.clicked.connect(self.ok)
        self.ui.load_from_file_pushButton.clicked.connect(self.loadButton)
        self.ui.export_pushButton.clicked.connect(self.export)
        self.ui.dictionarytable_tableWidget.setColumnCount(2)
        self.loadFromFile(pathAprildict)

    def loadFromFile(self, file):
        if os.path.exists(file):
            with open(file, "r") as f:
                dictAprilTags = json.load(f)
                for k,v in iter(dictAprilTags.items()):
                    self.addRow(k,v)

    def loadButton(self):
        file, ext = QFileDialog.getOpenFileName(self, self.tr('Load from File'), os.getenv('HOME'),
                                                          self.tr('Json File(*.json)'))
        if file != "":
            while self.ui.dictionarytable_tableWidget.rowCount() != 0:
                self.ui.dictionarytable_tableWidget.removeRow(0)
            self.loadFromFile(file)

    def export(self):
        file, ext  = QFileDialog.getSaveFileName(self, self.tr('Save as'), os.getenv('HOME'),
                                                         self.tr('Json File(*.json)'))
        if file != "":
            if ".json" not in file:
                file += ".json"
            self.save(file)

    def addRow(self, textValue = None, tagValue = None):
        table = self.ui.dictionarytable_tableWidget
        table.insertRow(table.rowCount())
        tag = QLineEdit()
        tag.setValidator(QIntValidator())
        text = QLineEdit()
        if textValue is not None:
            text.setText(textValue)
        if tagValue is not None:
            tag.setText(str(tagValue))
        table.setCellWidget(table.rowCount()-1, 0, tag)
        table.setCellWidget(table.rowCount()-1, 1, text)
        text.text()

    def deleteRow(self):
        table = self.ui.dictionarytable_tableWidget
        table.removeRow(table.currentRow())

    def ok(self):
        self.save(pathAprildict)
        self.close()

    def save(self, file):
        table = self.ui.dictionarytable_tableWidget
        dictAprilTags = {table.cellWidget(r, 1).text(): int(table.cellWidget(r, 0).text()) for r in
                         range(table.rowCount())}
        print(dictAprilTags)
        with open(file, "w") as f:
            json.dump(dictAprilTags, f)



if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = EditDictionaryTags()
    ex.show()
    sys.exit(app.exec_())