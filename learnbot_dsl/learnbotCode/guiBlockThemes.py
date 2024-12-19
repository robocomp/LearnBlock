from PySide6 import QtWidgets
from PySide6.QtGui import QColor
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

    def __init__(self, parent=None):
        QtWidgets.QDialog.__init__(self)
        self.ui.setupUi(self)

        #TODO: Conectar señales

        filepath = "/home/usuario/LearnBlock/learnbot_dsl/blocksConfig/blockThemes.json"
        themes = self.load_block_themes(filepath)

        self.printBlockThemes(themes)

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

    # Método para leer y deserializar el JSON
    def load_block_themes(self, filepath: str) -> List[BlockTheme]:
        try:
            with open(filepath, "r", encoding="utf-8") as file:
                raw_data = json.load(file)
                themes = [BlockTheme.from_dict(theme_data) for theme_data in raw_data["themes"]]
                return themes
        except FileNotFoundError:
            print(f"The file '{filepath}' doesn't exist.")
            return []
        except json.JSONDecodeError as e:
            print(f"Error reading JSON: {e}")
            return []



