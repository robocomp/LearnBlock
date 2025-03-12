import os
import json
import numpy as np
import cv2

pathBlocks = os.path.dirname(os.path.realpath(__file__))

# Theme config file
filepath = "/home/usuario/LearnBlock/learnbot_dsl/blocksConfig/blockThemes.json"

# Colo keys
HSV_KEYS = [
    "HSV_CONTROL", "HSV_MOTOR", "HSV_PERCEPTUAL", "HSV_PROPIOPERCEPTIVE",
    "HSV_OPERATOR", "HSV_EXPRESS", "HSV_OTHERS", "HSV_USERFUNCTION",
    "HSV_LIBRARY", "HSV_VARIABLE", "HSV_STRING", "HSV_NUMBER", "HSV_WHEN"
]

# Loadin JSON file with themes
try:
    with open(filepath, "r", encoding="utf-8") as file:
        data = json.load(file)

    # Looking for the actual theme
    actual_theme = data.get("actualTheme", "")
    theme = next((t for t in data.get("themes", []) if t["name"] == actual_theme), None)

    if theme:
        categories = theme.get("categories", {})

        for key in HSV_KEYS:
            category_name = key.replace("HSV_", "")
            if category_name in categories:
                color = categories[category_name]

                # RGB to HSV conversion
                bgr_color = np.uint8([[[color["Blue"], color["Green"], color["Red"]]]])
                #TODO: Remove
                #print(f"bgr_color: {bgr_color}")
                hsv_color = cv2.cvtColor(bgr_color, cv2.COLOR_BGR2HSV)
                # TODO: Remove
                #print(f"hsv_color: {hsv_color}")

                h, s, v = hsv_color[0][0]  # Extraer H, S y V
                globals()[key] = (int(h), int(s), int(v))  # Guardar como tupla (H, S, V)

                # TODO: Remove
                # Printing category name and HUE value
                #print(f"{category_name}: HUE = {globals()[key]}")
            else:
                globals()[key] = 0  # Valor por defecto si no se encuentra

    else:
        print(f"No se encontró el tema: {actual_theme}")
except Exception as e:
    print(f"Error al leer el archivo de configuración: {e}")

# Exponer variables globalmente
__all__ = ["pathBlocks"] + HSV_KEYS
