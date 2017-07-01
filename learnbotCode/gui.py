# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'interface.ui'
#
# Created: Sat Jul  1 15:54:41 2017
#      by: pyside-uic 0.2.15 running on PySide 1.2.2
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setEnabled(True)
        MainWindow.resize(681, 638)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout_2 = QtGui.QHBoxLayout(self.centralwidget)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.Tabwi = QtGui.QTabWidget(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.Tabwi.setFont(font)
        self.Tabwi.setTabPosition(QtGui.QTabWidget.North)
        self.Tabwi.setTabShape(QtGui.QTabWidget.Rounded)
        self.Tabwi.setObjectName("Tabwi")
        self.program_text = QtGui.QWidget()
        self.program_text.setObjectName("program_text")
        self.horizontalLayout = QtGui.QHBoxLayout(self.program_text)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout_6 = QtGui.QVBoxLayout()
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.label_3 = QtGui.QLabel(self.program_text)
        self.label_3.setObjectName("label_3")
        self.verticalLayout_6.addWidget(self.label_3)
        self.plainTextEdit_2 = QtGui.QPlainTextEdit(self.program_text)
        self.plainTextEdit_2.setObjectName("plainTextEdit_2")
        self.verticalLayout_6.addWidget(self.plainTextEdit_2)
        self.horizontalLayout.addLayout(self.verticalLayout_6)
        self.verticalLayout_5 = QtGui.QVBoxLayout()
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.camera = QtGui.QFrame(self.program_text)
        self.camera.setMinimumSize(QtCore.QSize(320, 240))
        self.camera.setMaximumSize(QtCore.QSize(320, 240))
        self.camera.setFrameShape(QtGui.QFrame.StyledPanel)
        self.camera.setFrameShadow(QtGui.QFrame.Raised)
        self.camera.setObjectName("camera")
        self.verticalLayout_5.addWidget(self.camera)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout_5.addItem(spacerItem)
        self.horizontalLayout_5 = QtGui.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.pushButton_3 = QtGui.QPushButton(self.program_text)
        self.pushButton_3.setObjectName("pushButton_3")
        self.horizontalLayout_5.addWidget(self.pushButton_3)
        self.pushButton_4 = QtGui.QPushButton(self.program_text)
        self.pushButton_4.setObjectName("pushButton_4")
        self.horizontalLayout_5.addWidget(self.pushButton_4)
        self.verticalLayout_5.addLayout(self.horizontalLayout_5)
        self.horizontalLayout.addLayout(self.verticalLayout_5)
        self.Tabwi.addTab(self.program_text, "")
        self.program_visual = QtGui.QWidget()
        self.program_visual.setObjectName("program_visual")
        self.gridLayout = QtGui.QGridLayout(self.program_visual)
        self.gridLayout.setObjectName("gridLayout")
        self.splitter = QtGui.QSplitter(self.program_visual)
        self.splitter.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setObjectName("splitter")
        self.tabWidget_2 = QtGui.QTabWidget(self.splitter)
        self.tabWidget_2.setMaximumSize(QtCore.QSize(500, 16777215))
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setWeight(50)
        font.setItalic(False)
        font.setStrikeOut(False)
        font.setBold(False)
        self.tabWidget_2.setFont(font)
        self.tabWidget_2.setTabPosition(QtGui.QTabWidget.West)
        self.tabWidget_2.setObjectName("tabWidget_2")
        self.control = QtGui.QWidget()
        self.control.setObjectName("control")
        self.verticalLayout_7 = QtGui.QVBoxLayout(self.control)
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        self.tableControl = QtGui.QTableWidget(self.control)
        self.tableControl.setObjectName("tableControl")
        self.tableControl.setColumnCount(0)
        self.tableControl.setRowCount(0)
        self.verticalLayout_7.addWidget(self.tableControl)
        self.tabWidget_2.addTab(self.control, "")
        self.move = QtGui.QWidget()
        self.move.setObjectName("move")
        self.tabWidget_2.addTab(self.move, "")
        self.sensors = QtGui.QWidget()
        self.sensors.setObjectName("sensors")
        self.tabWidget_2.addTab(self.sensors, "")
        self.operators = QtGui.QWidget()
        self.operators.setObjectName("operators")
        self.tabWidget_2.addTab(self.operators, "")
        self.vars = QtGui.QWidget()
        self.vars.setObjectName("vars")
        self.tabWidget_2.addTab(self.vars, "")
        self.layoutWidget = QtGui.QWidget(self.splitter)
        self.layoutWidget.setObjectName("layoutWidget")
        self.verticalLayout_3 = QtGui.QVBoxLayout(self.layoutWidget)
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.frame = QtGui.QFrame(self.layoutWidget)
        self.frame.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtGui.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.verticalLayout_3.addWidget(self.frame)
        self.horizontalLayout_4 = QtGui.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.pushButton = QtGui.QPushButton(self.layoutWidget)
        self.pushButton.setMaximumSize(QtCore.QSize(16777215, 27))
        self.pushButton.setObjectName("pushButton")
        self.horizontalLayout_4.addWidget(self.pushButton)
        self.pushButton_2 = QtGui.QPushButton(self.layoutWidget)
        self.pushButton_2.setMaximumSize(QtCore.QSize(16777215, 27))
        self.pushButton_2.setObjectName("pushButton_2")
        self.horizontalLayout_4.addWidget(self.pushButton_2)
        self.verticalLayout_3.addLayout(self.horizontalLayout_4)
        self.gridLayout.addWidget(self.splitter, 0, 0, 1, 1)
        self.Tabwi.addTab(self.program_visual, "")
        self.new_funtion = QtGui.QWidget()
        self.new_funtion.setObjectName("new_funtion")
        self.verticalLayout = QtGui.QVBoxLayout(self.new_funtion)
        self.verticalLayout.setObjectName("verticalLayout")
        self.gridLayout_3 = QtGui.QGridLayout()
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.label = QtGui.QLabel(self.new_funtion)
        self.label.setObjectName("label")
        self.gridLayout_3.addWidget(self.label, 0, 0, 1, 1)
        self.label_4 = QtGui.QLabel(self.new_funtion)
        self.label_4.setObjectName("label_4")
        self.gridLayout_3.addWidget(self.label_4, 0, 1, 1, 1)
        self.lineEdit = QtGui.QLineEdit(self.new_funtion)
        self.lineEdit.setObjectName("lineEdit")
        self.gridLayout_3.addWidget(self.lineEdit, 1, 0, 1, 1)
        self.comboBox = QtGui.QComboBox(self.new_funtion)
        self.comboBox.setObjectName("comboBox")
        self.gridLayout_3.addWidget(self.comboBox, 1, 1, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout_3)
        self.verticalLayout_2 = QtGui.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.label_2 = QtGui.QLabel(self.new_funtion)
        self.label_2.setObjectName("label_2")
        self.verticalLayout_2.addWidget(self.label_2)
        self.plainTextEdit = QtGui.QPlainTextEdit(self.new_funtion)
        self.plainTextEdit.setObjectName("plainTextEdit")
        self.verticalLayout_2.addWidget(self.plainTextEdit)
        self.verticalLayout.addLayout(self.verticalLayout_2)
        self.Tabwi.addTab(self.new_funtion, "")
        self.exist_funtion = QtGui.QWidget()
        self.exist_funtion.setObjectName("exist_funtion")
        self.horizontalLayout_3 = QtGui.QHBoxLayout(self.exist_funtion)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.listWidget_3 = QtGui.QListWidget(self.exist_funtion)
        self.listWidget_3.setMaximumSize(QtCore.QSize(181, 16777215))
        self.listWidget_3.setObjectName("listWidget_3")
        self.horizontalLayout_3.addWidget(self.listWidget_3)
        self.verticalLayout_8 = QtGui.QVBoxLayout()
        self.verticalLayout_8.setObjectName("verticalLayout_8")
        self.gridLayout_4 = QtGui.QGridLayout()
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.label_6 = QtGui.QLabel(self.exist_funtion)
        self.label_6.setObjectName("label_6")
        self.gridLayout_4.addWidget(self.label_6, 0, 0, 1, 1)
        self.label_7 = QtGui.QLabel(self.exist_funtion)
        self.label_7.setObjectName("label_7")
        self.gridLayout_4.addWidget(self.label_7, 0, 1, 1, 1)
        self.lineEdit_2 = QtGui.QLineEdit(self.exist_funtion)
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.gridLayout_4.addWidget(self.lineEdit_2, 1, 0, 1, 1)
        self.comboBox_2 = QtGui.QComboBox(self.exist_funtion)
        self.comboBox_2.setObjectName("comboBox_2")
        self.gridLayout_4.addWidget(self.comboBox_2, 1, 1, 1, 1)
        self.verticalLayout_8.addLayout(self.gridLayout_4)
        self.verticalLayout_4 = QtGui.QVBoxLayout()
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.label_5 = QtGui.QLabel(self.exist_funtion)
        self.label_5.setObjectName("label_5")
        self.verticalLayout_4.addWidget(self.label_5)
        self.plainTextEdit_3 = QtGui.QPlainTextEdit(self.exist_funtion)
        self.plainTextEdit_3.setObjectName("plainTextEdit_3")
        self.verticalLayout_4.addWidget(self.plainTextEdit_3)
        self.verticalLayout_8.addLayout(self.verticalLayout_4)
        self.horizontalLayout_3.addLayout(self.verticalLayout_8)
        self.Tabwi.addTab(self.exist_funtion, "")
        self.horizontalLayout_2.addWidget(self.Tabwi)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 681, 25))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtGui.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionExit = QtGui.QAction(MainWindow)
        self.actionExit.setObjectName("actionExit")
        self.actionHola = QtGui.QAction(MainWindow)
        self.actionHola.setObjectName("actionHola")
        self.menuFile.addAction(self.actionHola)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionExit)
        self.menubar.addAction(self.menuFile.menuAction())

        self.retranslateUi(MainWindow)
        self.Tabwi.setCurrentIndex(1)
        self.tabWidget_2.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtGui.QApplication.translate("MainWindow", "MainWindow", None, QtGui.QApplication.UnicodeUTF8))
        self.Tabwi.setWhatsThis(QtGui.QApplication.translate("MainWindow", "<html><head/><body><p>H</p><p><br/></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("MainWindow", "Programa", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_3.setText(QtGui.QApplication.translate("MainWindow", "Iniciar", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_4.setText(QtGui.QApplication.translate("MainWindow", "Parar", None, QtGui.QApplication.UnicodeUTF8))
        self.Tabwi.setTabText(self.Tabwi.indexOf(self.program_text), QtGui.QApplication.translate("MainWindow", "Programar (Texto)", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget_2.setTabText(self.tabWidget_2.indexOf(self.control), QtGui.QApplication.translate("MainWindow", "Control", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget_2.setTabText(self.tabWidget_2.indexOf(self.move), QtGui.QApplication.translate("MainWindow", "Movimiento", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget_2.setTabText(self.tabWidget_2.indexOf(self.sensors), QtGui.QApplication.translate("MainWindow", "Sensores", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget_2.setTabText(self.tabWidget_2.indexOf(self.operators), QtGui.QApplication.translate("MainWindow", "Operadores", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget_2.setTabText(self.tabWidget_2.indexOf(self.vars), QtGui.QApplication.translate("MainWindow", "Varialbes", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton.setText(QtGui.QApplication.translate("MainWindow", "Iniciar", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_2.setText(QtGui.QApplication.translate("MainWindow", "Parar", None, QtGui.QApplication.UnicodeUTF8))
        self.Tabwi.setTabText(self.Tabwi.indexOf(self.program_visual), QtGui.QApplication.translate("MainWindow", "Programar (Visual)", None, QtGui.QApplication.UnicodeUTF8))
        self.new_funtion.setToolTip(QtGui.QApplication.translate("MainWindow", "<html><head/><body><p>ASD</p><p><br/></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("MainWindow", "Nombre Función", None, QtGui.QApplication.UnicodeUTF8))
        self.label_4.setText(QtGui.QApplication.translate("MainWindow", "TIpo", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("MainWindow", "Código de la Función", None, QtGui.QApplication.UnicodeUTF8))
        self.Tabwi.setTabText(self.Tabwi.indexOf(self.new_funtion), QtGui.QApplication.translate("MainWindow", "Nueva Función", None, QtGui.QApplication.UnicodeUTF8))
        self.label_6.setText(QtGui.QApplication.translate("MainWindow", "Nombre Función", None, QtGui.QApplication.UnicodeUTF8))
        self.label_7.setText(QtGui.QApplication.translate("MainWindow", "TIpo", None, QtGui.QApplication.UnicodeUTF8))
        self.label_5.setText(QtGui.QApplication.translate("MainWindow", "Código de la Función", None, QtGui.QApplication.UnicodeUTF8))
        self.Tabwi.setTabText(self.Tabwi.indexOf(self.exist_funtion), QtGui.QApplication.translate("MainWindow", "Funciones Existentes", None, QtGui.QApplication.UnicodeUTF8))
        self.menuFile.setTitle(QtGui.QApplication.translate("MainWindow", "File", None, QtGui.QApplication.UnicodeUTF8))
        self.actionExit.setText(QtGui.QApplication.translate("MainWindow", "Salir", None, QtGui.QApplication.UnicodeUTF8))
        self.actionHola.setText(QtGui.QApplication.translate("MainWindow", "Añadir Nueva Metodo", None, QtGui.QApplication.UnicodeUTF8))

