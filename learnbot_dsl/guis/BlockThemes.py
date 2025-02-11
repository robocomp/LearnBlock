# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'BlockThemes.ui'
##
## Created by: Qt User Interface Compiler version 6.8.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QComboBox, QGridLayout, QGroupBox,
    QHBoxLayout, QLabel, QLineEdit, QPushButton,
    QSizePolicy, QSpacerItem, QWidget)

class Ui_BlockThemes(object):
    def setupUi(self, BlockThemes):
        if not BlockThemes.objectName():
            BlockThemes.setObjectName(u"BlockThemes")
        BlockThemes.setEnabled(True)
        BlockThemes.resize(653, 432)
        BlockThemes.setMinimumSize(QSize(0, 0))
        self.horizontalLayout = QHBoxLayout(BlockThemes)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer, 3, 0, 1, 1)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout.addItem(self.verticalSpacer, 4, 0, 1, 1)

        self.addThemeButton = QPushButton(BlockThemes)
        self.addThemeButton.setObjectName(u"addThemeButton")
        self.addThemeButton.setMinimumSize(QSize(0, 0))
        self.addThemeButton.setMaximumSize(QSize(30, 16777215))

        self.gridLayout.addWidget(self.addThemeButton, 2, 1, 1, 1)

        self.label = QLabel(BlockThemes)
        self.label.setObjectName(u"label")

        self.gridLayout.addWidget(self.label, 1, 0, 1, 1)

        self.themesBox = QComboBox(BlockThemes)
        self.themesBox.setObjectName(u"themesBox")

        self.gridLayout.addWidget(self.themesBox, 2, 0, 1, 1)

        self.acceptButton = QPushButton(BlockThemes)
        self.acceptButton.setObjectName(u"acceptButton")

        self.gridLayout.addWidget(self.acceptButton, 5, 0, 1, 1)


        self.horizontalLayout.addLayout(self.gridLayout)

        self.themeInfoBox = QGroupBox(BlockThemes)
        self.themeInfoBox.setObjectName(u"themeInfoBox")
        self.gridLayout_2 = QGridLayout(self.themeInfoBox)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.libraryLabel = QLabel(self.themeInfoBox)
        self.libraryLabel.setObjectName(u"libraryLabel")
        self.libraryLabel.setMaximumSize(QSize(150, 16777215))

        self.gridLayout_2.addWidget(self.libraryLabel, 10, 0, 1, 1)

        self.expressLabel = QLabel(self.themeInfoBox)
        self.expressLabel.setObjectName(u"expressLabel")
        self.expressLabel.setMaximumSize(QSize(150, 16777215))

        self.gridLayout_2.addWidget(self.expressLabel, 7, 0, 1, 1)

        self.numberLabel = QLabel(self.themeInfoBox)
        self.numberLabel.setObjectName(u"numberLabel")
        self.numberLabel.setMaximumSize(QSize(150, 16777215))

        self.gridLayout_2.addWidget(self.numberLabel, 13, 0, 1, 1)

        self.whenLabel = QLabel(self.themeInfoBox)
        self.whenLabel.setObjectName(u"whenLabel")
        self.whenLabel.setMaximumSize(QSize(150, 16777215))

        self.gridLayout_2.addWidget(self.whenLabel, 14, 0, 1, 1)

        self.perceptualLabel = QLabel(self.themeInfoBox)
        self.perceptualLabel.setObjectName(u"perceptualLabel")
        self.perceptualLabel.setMaximumSize(QSize(150, 16777215))

        self.gridLayout_2.addWidget(self.perceptualLabel, 4, 0, 1, 1)

        self.variableLabel = QLabel(self.themeInfoBox)
        self.variableLabel.setObjectName(u"variableLabel")
        self.variableLabel.setMaximumSize(QSize(150, 16777215))

        self.gridLayout_2.addWidget(self.variableLabel, 11, 0, 1, 1)

        self.motorLabel = QLabel(self.themeInfoBox)
        self.motorLabel.setObjectName(u"motorLabel")
        self.motorLabel.setMaximumSize(QSize(150, 16777215))

        self.gridLayout_2.addWidget(self.motorLabel, 3, 0, 1, 1)

        self.themeNameInput = QLineEdit(self.themeInfoBox)
        self.themeNameInput.setObjectName(u"themeNameInput")
        self.themeNameInput.setMaximumSize(QSize(150, 16777215))

        self.gridLayout_2.addWidget(self.themeNameInput, 0, 1, 1, 1)

        self.controlLabel = QLabel(self.themeInfoBox)
        self.controlLabel.setObjectName(u"controlLabel")
        self.controlLabel.setMaximumSize(QSize(150, 16777215))

        self.gridLayout_2.addWidget(self.controlLabel, 2, 0, 1, 1)

        self.userFunctionsLabel = QLabel(self.themeInfoBox)
        self.userFunctionsLabel.setObjectName(u"userFunctionsLabel")
        self.userFunctionsLabel.setMaximumSize(QSize(150, 16777215))

        self.gridLayout_2.addWidget(self.userFunctionsLabel, 9, 0, 1, 1)

        self.othersLabel = QLabel(self.themeInfoBox)
        self.othersLabel.setObjectName(u"othersLabel")
        self.othersLabel.setMaximumSize(QSize(150, 16777215))

        self.gridLayout_2.addWidget(self.othersLabel, 8, 0, 1, 1)

        self.propioPerceptiveLabel = QLabel(self.themeInfoBox)
        self.propioPerceptiveLabel.setObjectName(u"propioPerceptiveLabel")
        self.propioPerceptiveLabel.setMaximumSize(QSize(150, 16777215))

        self.gridLayout_2.addWidget(self.propioPerceptiveLabel, 5, 0, 1, 1)

        self.operatorLabel = QLabel(self.themeInfoBox)
        self.operatorLabel.setObjectName(u"operatorLabel")
        self.operatorLabel.setMaximumSize(QSize(150, 16777215))

        self.gridLayout_2.addWidget(self.operatorLabel, 6, 0, 1, 1)

        self.stringLabel = QLabel(self.themeInfoBox)
        self.stringLabel.setObjectName(u"stringLabel")
        self.stringLabel.setMaximumSize(QSize(150, 16777215))

        self.gridLayout_2.addWidget(self.stringLabel, 12, 0, 1, 1)

        self.label_2 = QLabel(self.themeInfoBox)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setMaximumSize(QSize(150, 16777215))

        self.gridLayout_2.addWidget(self.label_2, 0, 0, 1, 1)

        self.verticalSpacer_2 = QSpacerItem(20, 5, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)

        self.gridLayout_2.addItem(self.verticalSpacer_2, 1, 0, 1, 1)

        self.controlButton = QPushButton(self.themeInfoBox)
        self.controlButton.setObjectName(u"controlButton")
        self.controlButton.setMaximumSize(QSize(100, 20))
        self.controlButton.setStyleSheet(u"background-color: red;")

        self.gridLayout_2.addWidget(self.controlButton, 2, 1, 1, 1)

        self.motorButton = QPushButton(self.themeInfoBox)
        self.motorButton.setObjectName(u"motorButton")
        self.motorButton.setMaximumSize(QSize(100, 20))
        self.motorButton.setStyleSheet(u"background-color: red;")

        self.gridLayout_2.addWidget(self.motorButton, 3, 1, 1, 1)

        self.perceptualButton = QPushButton(self.themeInfoBox)
        self.perceptualButton.setObjectName(u"perceptualButton")
        self.perceptualButton.setMaximumSize(QSize(100, 20))
        self.perceptualButton.setStyleSheet(u"background-color: red;")

        self.gridLayout_2.addWidget(self.perceptualButton, 4, 1, 1, 1)

        self.propioPerceptiveButton = QPushButton(self.themeInfoBox)
        self.propioPerceptiveButton.setObjectName(u"propioPerceptiveButton")
        self.propioPerceptiveButton.setMaximumSize(QSize(100, 20))
        self.propioPerceptiveButton.setStyleSheet(u"background-color: red;")

        self.gridLayout_2.addWidget(self.propioPerceptiveButton, 5, 1, 1, 1)

        self.operatorButton = QPushButton(self.themeInfoBox)
        self.operatorButton.setObjectName(u"operatorButton")
        self.operatorButton.setMaximumSize(QSize(100, 20))
        self.operatorButton.setStyleSheet(u"background-color: red;")

        self.gridLayout_2.addWidget(self.operatorButton, 6, 1, 1, 1)

        self.expressButton = QPushButton(self.themeInfoBox)
        self.expressButton.setObjectName(u"expressButton")
        self.expressButton.setMaximumSize(QSize(100, 20))
        self.expressButton.setStyleSheet(u"background-color: red;")

        self.gridLayout_2.addWidget(self.expressButton, 7, 1, 1, 1)

        self.othersButton = QPushButton(self.themeInfoBox)
        self.othersButton.setObjectName(u"othersButton")
        self.othersButton.setMaximumSize(QSize(100, 20))
        self.othersButton.setStyleSheet(u"background-color: red;")

        self.gridLayout_2.addWidget(self.othersButton, 8, 1, 1, 1)

        self.usersFunctionsButton = QPushButton(self.themeInfoBox)
        self.usersFunctionsButton.setObjectName(u"usersFunctionsButton")
        self.usersFunctionsButton.setMaximumSize(QSize(100, 20))
        self.usersFunctionsButton.setStyleSheet(u"background-color: red;")

        self.gridLayout_2.addWidget(self.usersFunctionsButton, 9, 1, 1, 1)

        self.libraryButton = QPushButton(self.themeInfoBox)
        self.libraryButton.setObjectName(u"libraryButton")
        self.libraryButton.setMaximumSize(QSize(100, 20))
        self.libraryButton.setStyleSheet(u"background-color: red;")

        self.gridLayout_2.addWidget(self.libraryButton, 10, 1, 1, 1)

        self.variableButton = QPushButton(self.themeInfoBox)
        self.variableButton.setObjectName(u"variableButton")
        self.variableButton.setMaximumSize(QSize(100, 20))
        self.variableButton.setStyleSheet(u"background-color: red;")

        self.gridLayout_2.addWidget(self.variableButton, 11, 1, 1, 1)

        self.stringButton = QPushButton(self.themeInfoBox)
        self.stringButton.setObjectName(u"stringButton")
        self.stringButton.setMaximumSize(QSize(100, 20))
        self.stringButton.setStyleSheet(u"background-color: red;")

        self.gridLayout_2.addWidget(self.stringButton, 12, 1, 1, 1)

        self.numberButton = QPushButton(self.themeInfoBox)
        self.numberButton.setObjectName(u"numberButton")
        self.numberButton.setMaximumSize(QSize(100, 20))
        self.numberButton.setStyleSheet(u"background-color: red;")

        self.gridLayout_2.addWidget(self.numberButton, 13, 1, 1, 1)

        self.whenButton = QPushButton(self.themeInfoBox)
        self.whenButton.setObjectName(u"whenButton")
        self.whenButton.setMaximumSize(QSize(100, 20))
        self.whenButton.setStyleSheet(u"background-color: red;")

        self.gridLayout_2.addWidget(self.whenButton, 14, 1, 1, 1)


        self.horizontalLayout.addWidget(self.themeInfoBox)


        self.retranslateUi(BlockThemes)

        QMetaObject.connectSlotsByName(BlockThemes)
    # setupUi

    def retranslateUi(self, BlockThemes):
        BlockThemes.setWindowTitle(QCoreApplication.translate("BlockThemes", u"Form", None))
        self.addThemeButton.setText(QCoreApplication.translate("BlockThemes", u"+", None))
        self.label.setText(QCoreApplication.translate("BlockThemes", u"Block Themes", None))
        self.acceptButton.setText(QCoreApplication.translate("BlockThemes", u"Accept", None))
        self.themeInfoBox.setTitle(QCoreApplication.translate("BlockThemes", u"Theme colors", None))
        self.libraryLabel.setText(QCoreApplication.translate("BlockThemes", u"Library", None))
        self.expressLabel.setText(QCoreApplication.translate("BlockThemes", u"Express", None))
        self.numberLabel.setText(QCoreApplication.translate("BlockThemes", u"Number", None))
        self.whenLabel.setText(QCoreApplication.translate("BlockThemes", u"When", None))
        self.perceptualLabel.setText(QCoreApplication.translate("BlockThemes", u"Perceptual", None))
        self.variableLabel.setText(QCoreApplication.translate("BlockThemes", u"Variable", None))
        self.motorLabel.setText(QCoreApplication.translate("BlockThemes", u"Motor", None))
        self.controlLabel.setText(QCoreApplication.translate("BlockThemes", u"Control", None))
        self.userFunctionsLabel.setText(QCoreApplication.translate("BlockThemes", u"User Functions", None))
        self.othersLabel.setText(QCoreApplication.translate("BlockThemes", u"Others", None))
        self.propioPerceptiveLabel.setText(QCoreApplication.translate("BlockThemes", u"PropioPerceptive", None))
        self.operatorLabel.setText(QCoreApplication.translate("BlockThemes", u"Operator", None))
        self.stringLabel.setText(QCoreApplication.translate("BlockThemes", u"String", None))
        self.label_2.setText(QCoreApplication.translate("BlockThemes", u"Name", None))
        self.controlButton.setText("")
        self.motorButton.setText("")
        self.perceptualButton.setText("")
        self.propioPerceptiveButton.setText("")
        self.operatorButton.setText("")
        self.expressButton.setText("")
        self.othersButton.setText("")
        self.usersFunctionsButton.setText("")
        self.libraryButton.setText("")
        self.variableButton.setText("")
        self.stringButton.setText("")
        self.numberButton.setText("")
        self.whenButton.setText("")
    # retranslateUi

