from PySide6 import QtGui, QtWidgets, QtCore
from PySide6.QtCore import QObject, Signal, Qt
from PySide6.QtGui import QPalette, QColor
from PySide6.QtWidgets import QLabel, QPushButton

import learnbot_dsl.guis.BlockThemes as BlockThemes

def color_to_hex(color):
    """Convierte un QColor a su representación hexadecimal."""
    return f"#{color.red():02X}{color.green():02X}{color.blue():02X}"

class guiBlockThemes(QtWidgets.QDialog):

    ui = BlockThemes.Ui_BlockThemes()

    def __init__(self, parent=None):
        QtWidgets.QDialog.__init__(self)
        self.ui.setupUi(self)

        #TODO: Conectar señales




    def openColorPicker(self, button) -> QColor:
        color = QtWidgets.QColorDialog.getColor()
        if color.isValid():
            button.setStyleSheet("background-color: {}".format(color.name()))  # Convertir a hexadecimal
            self.refreshButtonColor(button)
            return color
        else:
            return None


    def refreshButtonColor(self, button):
        bg_color = button.palette().color(button.backgroundRole())
        # Convertir a hexadecimal
        hex_color = color_to_hex(bg_color)
        # Establecer el texto del botón
        button.setText(hex_color)



