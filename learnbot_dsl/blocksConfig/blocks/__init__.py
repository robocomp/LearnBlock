import os
import json
import numpy as np
import cv2

pathBlocks = os.path.dirname(os.path.realpath(__file__))

# Archivo de configuración
filepath = "/home/usuario/LearnBlock/learnbot_dsl/blocksConfig/blockThemes.json"

# Claves de colores
HUE_KEYS = [
    "HUE_CONTROL", "HUE_MOTOR", "HUE_PERCEPTUAL", "HUE_PROPIOPERCEPTIVE",
    "HUE_OPERATOR", "HUE_EXPRESS", "HUE_OTHERS", "HUE_USERFUNCTION",
    "HUE_LIBRARY", "HUE_VARIABLE", "HUE_STRING", "HUE_NUMBER", "HUE_WHEN"
]

# Cargar archivo JSON con temas
try:
    with open(filepath, "r", encoding="utf-8") as file:
        data = json.load(file)

    # Buscar el tema actual
    actual_theme = data.get("actualTheme", "")
    theme = next((t for t in data.get("themes", []) if t["name"] == actual_theme), None)

    if theme:
        categories = theme.get("categories", {})

        for key in HUE_KEYS:
            category_name = key.replace("HUE_", "")
            if category_name in categories:
                color = categories[category_name]

                # Convertimos de RGB a HSV
                bgr_color = np.uint8([[[color["Blue"], color["Green"], color["Red"]]]])
                print(f"bgr_color: {bgr_color}")
                hsv_color = cv2.cvtColor(bgr_color, cv2.COLOR_BGR2HSV)
                print(f"hsv_color: {hsv_color}")

                # Asignamos solo el canal Hue (H)
                globals()[key] = int(hsv_color[0][0][0])  # H está en el rango 0-179 en OpenCV

                # Imprimir el nombre de la categoría y el valor de Hue
                print(f"{category_name}: HUE = {globals()[key]}")
            else:
                globals()[key] = 0  # Valor por defecto si no se encuentra

    else:
        print(f"No se encontró el tema: {actual_theme}")
except Exception as e:
    print(f"Error al leer el archivo de configuración: {e}")

# Exponer variables globalmente
__all__ = ["pathBlocks"] + HUE_KEYS
