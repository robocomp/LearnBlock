from PySide6 import QtWidgets, QtGui
from PySide6.QtGui import QColor, QPalette
import json
from typing import List, Dict

import learnbot_dsl.guis.BlockThemes as BlockThemes

def color_to_hex(color):
    """Convierte un QColor a su representación hexadecimal."""
    return f"#{color.red():02X}{color.green():02X}{color.blue():02X}"

# Estructura de datos
# Clase Theme
class BlockTheme:
    def __init__(self, name: str, editable: bool, categories: Dict[str, QColor]):
        self.name = name
        self.editable = editable
        self.categories = categories

    @staticmethod
    def from_dict(data: Dict) -> "BlockTheme":
        # Convertir las categorías del diccionario en un map {nombre: QColor}
        categories = {
            category_name: QColor(
                values.get("Red", 0),
                values.get("Green", 0),
                values.get("Blue", 0)
            )
            for category_name, values in data["categories"].items()
        }
        return BlockTheme(
            name=data["name"],
            editable=data["editable"],
            categories=categories
        )

class guiBlockThemes(QtWidgets.QDialog):

    ui = BlockThemes.Ui_BlockThemes()
    filepath = "/home/usuario/LearnBlock/learnbot_dsl/blocksConfig/blockThemes.json"

    def __init__(self, parent=None):
        QtWidgets.QDialog.__init__(self)
        self.ui.setupUi(self)
        self.actualTheme = "Default Theme"

        self.load_block_themes(self.filepath)

        # Setting theme box values
        self.ui.themesBox.addItems([theme.name for theme in self.themes])
        index = self.ui.themesBox.findText(self.actualTheme)
        if index != -1:
            self.ui.themesBox.setCurrentIndex(index)
        else:
            print(f"Theme not found: {self.actualTheme}")

        # Signal connection
        self.ui.themesBox.currentIndexChanged.connect(self.refreshCategoriesButton)

        print(self.actualTheme)

        # Setting button color for the actual theme
        self.settingGuiActualTheme(next((theme for theme in self.themes if theme.name == self.actualTheme), None))

    def refreshCategoriesButton(self):
        self.actualTheme = self.ui.themesBox.currentText()
        self.settingGuiActualTheme(
            next((theme for theme in self.themes if theme.name == self.actualTheme), None))

    def settingGuiActualTheme(self, theme : BlockTheme):

        self.ui.themeInfoBox.setEnabled(theme.editable)

        self.ui.themeNameInput.setText(theme.name)

        self.settingGuiCategorieButton(theme, self.ui.controlButton, "CONTROL")
        self.settingGuiCategorieButton(theme, self.ui.motorButton, "MOTOR")
        self.settingGuiCategorieButton(theme, self.ui.perceptualButton, "PERCEPTUAL")
        self.settingGuiCategorieButton(theme, self.ui.propioPerceptiveButton, "PROPIOPERCEPTIVE")
        self.settingGuiCategorieButton(theme, self.ui.operatorButton, "OPERATOR")
        self.settingGuiCategorieButton(theme, self.ui.expressButton, "EXPRESS")
        self.settingGuiCategorieButton(theme, self.ui.othersButton, "OTHERS")
        self.settingGuiCategorieButton(theme, self.ui.usersFunctionsButton, "USERFUNCTION")
        self.settingGuiCategorieButton(theme, self.ui.libraryButton, "LIBRARY")
        self.settingGuiCategorieButton(theme, self.ui.variableButton, "VARIABLE")
        self.settingGuiCategorieButton(theme, self.ui.stringButton, "STRING")
        self.settingGuiCategorieButton(theme, self.ui.numberButton, "NUMBER")
        self.settingGuiCategorieButton(theme, self.ui.whenButton, "WHEN")

    def settingGuiCategorieButton(self, theme: BlockTheme, button: QtWidgets.QPushButton, category: str):
        button.setStyleSheet("background-color: {}".format(theme.categories[category].name()))
        self.refreshButtonColor(button)

    def printBlockThemes(self, themes):
        # Mostrar los temas cargados
        for theme in themes:
            print(f"Tema: {theme.name}, Editable: {theme.editable}")
            for category, color in theme.categories.items():
                print(f"  - Categoría: {category}, Color (RGB): ({color.red()}, {color.green()}, {color.blue()})")

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

    # Method to read and desealize JSON
    def load_block_themes(self, filepath: str) -> None:
        try:
            with open(filepath, "r", encoding="utf-8") as file:
                raw_data = json.load(file)
                self.actualTheme = raw_data["actualTheme"]
                self.themes = [BlockTheme.from_dict(theme_data) for theme_data in raw_data["themes"]]
        except FileNotFoundError:
            print(f"The file '{filepath}' doesn't exist.")
            return []
        except json.JSONDecodeError as e:
            print(f"Error reading JSON: {e}")
            return []



