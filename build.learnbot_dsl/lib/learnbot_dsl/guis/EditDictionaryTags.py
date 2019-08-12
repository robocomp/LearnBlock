# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/ivan/robocomp/components/learnbot/learnbot_dsl/guis/EditDictionaryTags.ui',
# licensing of '/home/ivan/robocomp/components/learnbot/learnbot_dsl/guis/EditDictionaryTags.ui' applies.
#
# Created: Thu Mar 21 13:11:48 2019
#      by: pyside2-uic  running on PySide2 5.12.1
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_EditDictionaryTags(object):
    def setupUi(self, EditDictionaryTags):
        EditDictionaryTags.setObjectName("EditDictionaryTags")
        EditDictionaryTags.resize(361, 273)
        self.horizontalLayout = QtWidgets.QHBoxLayout(EditDictionaryTags)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.dictionarytable_tableWidget = QtWidgets.QTableWidget(EditDictionaryTags)
        self.dictionarytable_tableWidget.setObjectName("dictionarytable_tableWidget")
        self.dictionarytable_tableWidget.setColumnCount(0)
        self.dictionarytable_tableWidget.setRowCount(0)
        self.dictionarytable_tableWidget.horizontalHeader().setVisible(False)
        self.dictionarytable_tableWidget.verticalHeader().setVisible(False)
        self.horizontalLayout.addWidget(self.dictionarytable_tableWidget)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.delete_pushButton = QtWidgets.QPushButton(EditDictionaryTags)
        self.delete_pushButton.setObjectName("delete_pushButton")
        self.verticalLayout_2.addWidget(self.delete_pushButton)
        self.add_pushButton = QtWidgets.QPushButton(EditDictionaryTags)
        self.add_pushButton.setObjectName("add_pushButton")
        self.verticalLayout_2.addWidget(self.add_pushButton)
        self.ok_pushButton = QtWidgets.QPushButton(EditDictionaryTags)
        self.ok_pushButton.setObjectName("ok_pushButton")
        self.verticalLayout_2.addWidget(self.ok_pushButton)
        self.export_pushButton = QtWidgets.QPushButton(EditDictionaryTags)
        self.export_pushButton.setObjectName("export_pushButton")
        self.verticalLayout_2.addWidget(self.export_pushButton)
        self.load_from_file_pushButton = QtWidgets.QPushButton(EditDictionaryTags)
        self.load_from_file_pushButton.setObjectName("load_from_file_pushButton")
        self.verticalLayout_2.addWidget(self.load_from_file_pushButton)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem)
        self.horizontalLayout.addLayout(self.verticalLayout_2)

        self.retranslateUi(EditDictionaryTags)
        QtCore.QMetaObject.connectSlotsByName(EditDictionaryTags)

    def retranslateUi(self, EditDictionaryTags):
        EditDictionaryTags.setWindowTitle(QtWidgets.QApplication.translate("EditDictionaryTags", "Edit Tags Dictionary", None, -1))
        self.delete_pushButton.setText(QtWidgets.QApplication.translate("EditDictionaryTags", "Delete", None, -1))
        self.add_pushButton.setText(QtWidgets.QApplication.translate("EditDictionaryTags", "Add", None, -1))
        self.ok_pushButton.setText(QtWidgets.QApplication.translate("EditDictionaryTags", "Ok", None, -1))
        self.export_pushButton.setText(QtWidgets.QApplication.translate("EditDictionaryTags", "Export", None, -1))
        self.load_from_file_pushButton.setText(QtWidgets.QApplication.translate("EditDictionaryTags", "Load from file", None, -1))

