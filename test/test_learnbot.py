import json
import os
import pickle
import random
import shutil
import tempfile
import unittest

from learnbot_dsl.blocksConfig import pathImgBlocks
from learnbot_dsl.blocksConfig.parserConfigBlock import reload_functions
from learnbot_dsl.learnbotCode.LearnBlock import LearnBlock
from learnbot_dsl.learnbotCode.Parser import Parser, PythonGenerator, Typechecker, parserLearntBotCodeFromCode, \
    parserLearntBotCode
from learnbot_dsl.functions import getFuntions
from learnbot_dsl.learnbotCode.VisualBlock import toLBotPy

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
RESOURCES_DIR = os.path.join(CURRENT_DIR, "resources")
REF_EXAMPLES_PATH = os.path.join(RESOURCES_DIR, "reference_examples")


TEST_TEXT = \
    """

main:
    x = 2
end

"""



# class ParserConfigBlockTesting(unittest.TestCase):
#     def assertNestedDictEqual(self, first, second, ignored_keys=None, msg=None):
#         if ignored_keys is not None:
#             for key in ignored_keys:
#                 if key in first:
#                     del first[key]
#                 if key in second:
#                     del second[key]
#         j1 = json.dumps(first, sort_keys=True, indent=4)
#         j2 = json.dumps(second, sort_keys=True, indent=4)
#
#         self.maxDiff = None
#         # with open('last_json1.txt', 'w') as outfile:
#         #     json.dump(first, outfile, sort_keys=True, indent=4)
#         # with open('last_json2.txt', 'w') as outfile:
#         #     json.dump(second, outfile, sort_keys=True, indent=4)
#         self.assertEqual(j1, j2, msg)
#
#     def test_blocks(self):
#         blocks = reload_functions()
#         self.assertNestedDictEqual(blocks,
#                                    [
#                                        {
#                                            "type": "operator",
#                                            "category": "operator",
#                                            "name": "+",
#                                            "shape": ["block3"],
#                                            "tooltip": {
#                                                "ES": "Realiza la operación suma de los bloques conectados",
#                                                "EN": "",
#                                            },
#                                            "inputs": ["number", "number"],
#                                            "output": "number",
#                                        },
#                                        {
#                                            "type": "operator",
#                                            "category": "operator",
#                                            "name": "-",
#                                            "shape": ["block3"],
#                                            "tooltip": {
#                                                "ES": "Realiza la operación resta de los bloques conectados",
#                                                "EN": "",
#                                            },
#                                            "inputs": ["number", "number"],
#                                            "output": "number",
#                                        },
#                                        {
#                                            "type": "operator",
#                                            "category": "operator",
#                                            "name": "*",
#                                            "shape": ["block3"],
#                                            "tooltip": {
#                                                "ES": "Realiza la operación multiplicación de los bloques conectados",
#                                                "EN": "",
#                                            },
#                                            "inputs": ["number", "number"],
#                                            "output": "number",
#                                        },
#                                        {
#                                            "type": "operator",
#                                            "category": "operator",
#                                            "name": "/",
#                                            "shape": ["block3"],
#                                            "tooltip": {
#                                                "ES": "Realiza la operación división de los bloques conectados",
#                                                "EN": "",
#                                            },
#                                            "inputs": ["number", "number"],
#                                            "output": "number",
#                                        },
#                                        {
#                                            "type": "operator",
#                                            "category": "operator",
#                                            "name": "=",
#                                            "shape": ["block3"],
#                                            "tooltip": {
#                                                "ES": "Iguala el bloque de la izquierda al bloque de la derecha",
#                                                "EN": "",
#                                            },
#                                        },
#                                        {
#                                            "type": "operator",
#                                            "category": "operator",
#                                            "name": "==",
#                                            "shape": ["block3"],
#                                            "tooltip": {
#                                                "ES": "Compara los bloques conectados retornando verdadero en caso de que sean iguales y falso en caso contrario",
#                                                "EN": "",
#                                            },
#                                            "inputs": ["bool", "bool"],
#                                            "output": "bool",
#                                        },
#                                        {
#                                            "type": "operator",
#                                            "category": "operator",
#                                            "name": "+=",
#                                            "shape": ["block3"],
#                                            "tooltip": {
#                                                "ES": "Operador de adicción a una variable, previamente inicializada",
#                                                "EN": "",
#                                            },
#                                        },
#                                        {
#                                            "type": "operator",
#                                            "category": "operator",
#                                            "name": "-=",
#                                            "shape": ["block3"],
#                                            "tooltip": {
#                                                "ES": "Operador de resta a una variable, previamente inicializada",
#                                                "EN": "",
#                                            },
#                                        },
#                                        {
#                                            "type": "operator",
#                                            "category": "operator",
#                                            "name": "/=",
#                                            "shape": ["block3"],
#                                            "tooltip": {
#                                                "ES": "Operador de división a una variable, previamente inicializada",
#                                                "EN": "",
#                                            },
#                                        },
#                                        {
#                                            "type": "operator",
#                                            "category": "operator",
#                                            "name": "*=",
#                                            "shape": ["block3"],
#                                            "tooltip": {
#                                                "ES": "Operador de multiplicación a una variable, previamente inicializada",
#                                                "EN": "",
#                                            },
#                                        },
#                                        {
#                                            "type": "operator",
#                                            "category": "operator",
#                                            "name": "True",
#                                            "shape": ["block4"],
#                                            "languages": {"ES": "Verdad", "EN": "True"},
#                                            "tooltip": {"ES": "Verdad", "EN": "True"},
#                                            "output": "bool",
#                                        },
#                                        {
#                                            "type": "operator",
#                                            "category": "operator",
#                                            "name": "False",
#                                            "shape": ["block4"],
#                                            "languages": {"ES": "Falso", "EN": "False"},
#                                            "tooltip": {"ES": "Falso", "EN": "False"},
#                                            "output": "bool",
#                                        },
#                                        {
#                                            "type": "operator",
#                                            "category": "operator",
#                                            "name": "<",
#                                            "shape": ["block3"],
#                                            "tooltip": {
#                                                "ES": "Compara los bloques conectados retornando verdadero en caso de que menor el de la derecha y falso en caso contrario.",
#                                                "EN": "",
#                                            },
#                                            "inputs": ["bool", "bool"],
#                                            "output": "bool",
#                                        },
#                                        {
#                                            "type": "operator",
#                                            "category": "operator",
#                                            "name": ">",
#                                            "shape": ["block3"],
#                                            "tooltip": {
#                                                "ES": "Compara los bloques conectados retornando verdadero en caso de que sea menor el de la derecha y falso en caso contrario.",
#                                                "EN": "",
#                                            },
#                                            "inputs": ["bool", "bool"],
#                                            "output": "bool",
#                                        },
#                                        {
#                                            "type": "operator",
#                                            "category": "operator",
#                                            "name": "and",
#                                            "shape": ["block3"],
#                                            "languages": {"ES": "Y", "EN": "and"},
#                                            "tooltip": {"ES": "Concatena operaciones con la operación lógica Y",
#                                                        "EN": ""},
#                                            "inputs": ["bool", "bool"],
#                                            "output": "bool",
#                                        },
#                                        {
#                                            "type": "operator",
#                                            "category": "operator",
#                                            "name": "or",
#                                            "shape": ["block3"],
#                                            "languages": {"ES": "O", "EN": "or"},
#                                            "tooltip": {"ES": "Concatena operaciones con la operación lógica O",
#                                                        "EN": ""},
#                                            "inputs": ["bool", "bool"],
#                                            "output": "bool",
#                                        },
#                                        {
#                                            "type": "operator",
#                                            "category": "operator",
#                                            "name": "not",
#                                            "shape": ["block3"],
#                                            "languages": {"ES": "No", "EN": "not"},
#                                            "tooltip": {"ES": "Niega una comparación", "EN": ""},
#                                            "inputs": ["bool"],
#                                            "output": "bool",
#                                        },
#                                        {
#                                            "type": "operator",
#                                            "category": "operator",
#                                            "name": ")",
#                                            "shape": ["block3"],
#                                            "languages": {"ES": ")", "EN": ")"},
#                                            "tooltip": {"ES": ")", "EN": ""},
#                                        },
#                                        {
#                                            "type": "operator",
#                                            "category": "operator",
#                                            "name": "(",
#                                            "shape": ["block3"],
#                                            "languages": {"ES": "(", "EN": "("},
#                                            "tooltip": {"ES": "(", "EN": ""},
#                                        },
#                                        {
#                                            "type": "control",
#                                            "category": "control",
#                                            "name": "main",
#                                            "shape": ["block8"],
#                                            "languages": {"ES": "principal", "EN": "main"},
#                                            "tooltip": {
#                                                "ES": "Este bloque se ejecutara cuando los eventos esten desactivados, debera contener el codigo a ejecutar",
#                                                "EN": "",
#                                            },
#                                        },
#                                        {
#                                            "type": "control",
#                                            "category": "control",
#                                            "name": "if",
#                                            "shape": ["block6"],
#                                            "languages": {"ES": "si", "EN": "if"},
#                                            "tooltip": {
#                                                "ES": "Se trata de una estructura de control que permite redirigir un curso de acción segun la evaluación de una condición, sea falsa o verdadera. Debe debajo de un bloque si",
#                                                "EN": "",
#                                            },
#                                            "inputs": ["bool"],
#                                        },
#                                        {
#                                            "type": "control",
#                                            "category": "control",
#                                            "name": "elif",
#                                            "shape": ["block6"],
#                                            "languages": {"ES": "sino si", "EN": "else if"},
#                                            "tooltip": {
#                                                "ES": "Se trata de una estructura de control que permite redirigir un curso de acción segun la evaluación de una condición, sea falsa o verdadera. Debe debajo de un bloque si o un bloque sino si",
#                                                "EN": "",
#                                            },
#                                            "inputs": ["bool"],
#                                        },
#                                        {
#                                            "type": "control",
#                                            "category": "control",
#                                            "name": "else",
#                                            "shape": ["block5"],
#                                            "languages": {"ES": "sino", "EN": "else"},
#                                            "tooltip": {
#                                                "ES": "Se trata de una estructura de control que permite redirigir un curso de acción segun la evaluación de una condición, sea falsa o verdadera. Debe debajo de un bloque si o un bloque sino si",
#                                                "EN": "",
#                                            },
#                                            "inputs": ["bool"],
#                                        },
#                                        {
#                                            "type": "control",
#                                            "category": "control",
#                                            "name": "while",
#                                            "shape": ["block6"],
#                                            "languages": {"ES": "mientras", "EN": "while"},
#                                            "tooltip": {
#                                                "ES": "Se repetira la secuencia de codigo contenida en el bloque hasta que la condición no se cumpla.",
#                                                "EN": "",
#                                            },
#                                            "inputs": ["bool"],
#                                        },
#                                        {
#                                            "type": "control",
#                                            "category": "control",
#                                            "name": "while True",
#                                            "shape": ["block5"],
#                                            "languages": {"ES": "por siempre", "EN": "forever"},
#                                            "tooltip": {
#                                                "ES": "Se repetira la secuencia de codigo contenida en el bloque por siempre.",
#                                                "EN": "",
#                                            },
#                                        },
#                                        {
#                                            "type": "control",
#                                            "category": "control",
#                                            "name": "elapsedTime",
#                                            "variables": [
#                                                {
#                                                    "type": "float",
#                                                    "name": "threshold",
#                                                    "default": "0",
#                                                    "translate": {"ES": "umbral", "EN": "threshold"},
#                                                }
#                                            ],
#                                            "shape": ["block4", "block3"],
#                                            "languages": {"ES": "tiempo_transcurrido", "EN": "elapsed_Time"},
#                                            "tooltip": {
#                                                "ES": "Devuelve verdadero si el tiempo total del programa es mayor o igual que threshold sino devuelve falso",
#                                                "EN": "",
#                                            },
#                                        },
#                                        {
#                                            "type": "others",
#                                            "category": "control",
#                                            "name": "sleep",
#                                            "variables": [
#                                                {
#                                                    "type": "float",
#                                                    "name": "seconds",
#                                                    "default": "1",
#                                                    "translate": {"ES": "segundos", "EN": "seconds"},
#                                                }
#                                            ],
#                                            "shape": ["block1"],
#                                            "languages": {"ES": "esperar", "EN": "wait"},
#                                            "tooltip": {"ES": "Espera un tiempo determinado", "EN": ""},
#                                        },
#                                        {
#                                            "type": "motor",
#                                            "category": "Base",
#                                            "name": "move_left",
#                                            "shape": ["blockVertical"],
#                                            "languages": {"ES": "mover_izquierda", "EN": "move_left"},
#                                            "tooltip": {"ES": "Mueve el robot a la izquierda", "EN": ""},
#                                        },
#                                        {
#                                            "type": "motor",
#                                            "category": "Base",
#                                            "name": "move_right",
#                                            "shape": ["blockVertical"],
#                                            "languages": {"ES": "mover_derecha", "EN": "move_right"},
#                                            "tooltip": {"ES": "Mueve el robot a la derecha", "EN": ""},
#                                        },
#                                        {
#                                            "type": "motor",
#                                            "category": "Base",
#                                            "name": "move_straight",
#                                            "shape": ["blockVertical"],
#                                            "languages": {"ES": "mover_recto", "EN": "move_straight"},
#                                            "tooltip": {"ES": "Mueve el robot a la recto", "EN": ""},
#                                        },
#                                        {
#                                            "type": "motor",
#                                            "category": "Base",
#                                            "name": "set_move",
#                                            "variables": [
#                                                {
#                                                    "type": "float",
#                                                    "name": "avance",
#                                                    "default": "0",
#                                                    "translate": {"ES": "avance", "EN": "advance"},
#                                                },
#                                                {
#                                                    "type": "float",
#                                                    "name": "rotacion",
#                                                    "default": "0",
#                                                    "translate": {"ES": "rotacion", "EN": "rotation"},
#                                                },
#                                            ],
#                                            "shape": ["blockVertical"],
#                                            "languages": {"ES": "poner_movimiento", "EN": "set_move"},
#                                            "tooltip": {
#                                                "ES": "Mueve el robot con la velocida de avance y la rotacion indicada",
#                                                "EN": "",
#                                            },
#                                        },
#                                        {
#                                            "type": "motor",
#                                            "category": "Base",
#                                            "name": "stop_bot",
#                                            "shape": ["blockVertical"],
#                                            "languages": {"ES": "parar", "EN": "stop_bot"},
#                                            "tooltip": {"ES": "Para el robot", "EN": ""},
#                                        },
#                                        {
#                                            "type": "motor",
#                                            "category": "Base",
#                                            "name": "reset_orientation",
#                                            "shape": ["blockVertical"],
#                                            "languages": {"ES": "orientacion_a_cero", "EN": "reset_orientation"},
#                                            "tooltip": {"ES": "Establece la orientación actual a 0º", "EN": ""},
#                                        },
#                                        {
#                                            "type": "motor",
#                                            "category": "Base",
#                                            "name": "set_orientation",
#                                            "variables": [
#                                                {
#                                                    "type": "float",
#                                                    "name": "angle",
#                                                    "default": "0",
#                                                    "translate": {"ES": "angulo", "EN": "angle"},
#                                                }
#                                            ],
#                                            "shape": ["blockVertical"],
#                                            "languages": {"ES": "pon_orientacion", "EN": "set_orientation"},
#                                            "tooltip": {
#                                                "ES": "Sitúa la base del robot en una cierta orientación",
#                                                "EN": "",
#                                            },
#                                        },
#                                        {
#                                            "type": "motor",
#                                            "category": "Base",
#                                            "name": "turn",
#                                            "variables": [
#                                                {
#                                                    "type": "float",
#                                                    "name": "angle",
#                                                    "default": "0",
#                                                    "translate": {"ES": "angulo", "EN": "angle"},
#                                                }
#                                            ],
#                                            "shape": ["blockVertical"],
#                                            "languages": {"ES": "girar", "EN": "turn"},
#                                            "tooltip": {"ES": "Gira el robot con una velocidad angular", "EN": ""},
#                                        },
#                                        {
#                                            "type": "motor",
#                                            "category": "Base",
#                                            "name": "turn_back",
#                                            "shape": ["blockVertical"],
#                                            "languages": {"ES": "girar_atras", "EN": "turn_back"},
#                                            "tooltip": {"ES": "Gira el robot hacia atras", "EN": ""},
#                                        },
#                                        {
#                                            "type": "motor",
#                                            "category": "Base",
#                                            "name": "turn_left",
#                                            "shape": ["blockVertical"],
#                                            "languages": {"ES": "girar_izquierda", "EN": "turn_left"},
#                                            "tooltip": {"ES": "Gira al robot a la izquierda", "EN": ""},
#                                        },
#                                        {
#                                            "type": "motor",
#                                            "category": "Base",
#                                            "name": "turn_right",
#                                            "shape": ["blockVertical"],
#                                            "languages": {"ES": "girar_derecha", "EN": "turn_right"},
#                                            "tooltip": {"ES": "Gira al robot a la derecha", "EN": ""},
#                                        },
#                                        {
#                                            "type": "motor",
#                                            "category": "Base",
#                                            "name": "slow_down",
#                                            "shape": ["blockVertical"],
#                                            "languages": {"ES": "mas_despacio", "EN": "slow_down"},
#                                            "tooltip": {"ES": "Reduce la velocidad del robot", "EN": ""},
#                                        },
#                                        {
#                                            "type": "motor",
#                                            "category": "Motor",
#                                            "name": "look_floor",
#                                            "shape": ["blockVertical"],
#                                            "languages": {"ES": "mirar_suelo", "EN": "look_floor"},
#                                            "tooltip": {
#                                                "ES": "Gira la camara del robot para que este mire al suelo",
#                                                "EN": "",
#                                            },
#                                        },
#                                        {
#                                            "type": "motor",
#                                            "category": "Motor",
#                                            "name": "look_up",
#                                            "shape": ["blockVertical"],
#                                            "languages": {"ES": "mirar_arriba", "EN": "look_up"},
#                                            "tooltip": {"ES": "Mueve la camara hacia arriba.", "EN": ""},
#                                        },
#                                        {
#                                            "type": "motor",
#                                            "category": "Motor",
#                                            "name": "look_front",
#                                            "shape": ["blockVertical"],
#                                            "languages": {"ES": "mirar_frente", "EN": "look_front"},
#                                            "tooltip": {"ES": "Mueve la camara hacia el frente", "EN": ""},
#                                        },
#                                        {
#                                            "type": "motor",
#                                            "category": "Motor",
#                                            "name": "setAngleCamera",
#                                            "variables": [
#                                                {
#                                                    "type": "float",
#                                                    "name": "angle",
#                                                    "default": "0",
#                                                    "translate": {"ES": "angulo", "EN": "angle"},
#                                                }
#                                            ],
#                                            "shape": ["blockVertical"],
#                                            "languages": {"ES": "ponerAnguloCamara", "EN": "setAngleCamera"},
#                                            "tooltip": {"ES": "Mueve la camara a un angulo determinado", "EN": ""},
#                                        },
#                                        {
#                                            "type": "motor",
#                                            "category": "Motor",
#                                            "name": "setAngleMotor",
#                                            "variables": [
#                                                {
#                                                    "type": "string",
#                                                    "name": "key",
#                                                    "default": "KEY",
#                                                    "translate": {"ES": "clave", "EN": "key"},
#                                                },
#                                                {
#                                                    "type": "float",
#                                                    "name": "angle",
#                                                    "default": "0",
#                                                    "translate": {"ES": "angulo", "EN": "angle"},
#                                                },
#                                            ],
#                                            "shape": ["blockVertical"],
#                                            "languages": {"ES": "ponerAnguloMotor", "EN": "setAngleMotor"},
#                                            "tooltip": {"ES": "Mueve la camara a un angulo determinado", "EN": ""},
#                                        },
#                                        {
#                                            "type": "express",
#                                            "category": "Emotion",
#                                            "name": "expressNeutral",
#                                            "shape": ["blockVertical"],
#                                            "languages": {"ES": "no_expresar_nada", "EN": "express_Neutral"},
#                                            "tooltip": {
#                                                "ES": "Muestra la cara de neutralidad en el robot",
#                                                "EN": "Show the face of neutral in the robot",
#                                            },
#                                        },
#                                        {
#                                            "type": "express",
#                                            "category": "Emotion",
#                                            "name": "expressJoy",
#                                            "shape": ["blockVertical"],
#                                            "languages": {"ES": "expresar_alegria", "EN": "express_Joy"},
#                                            "tooltip": {
#                                                "ES": "Muestra la cara de alegria en el robot",
#                                                "EN": "Show the face of joy in the robot",
#                                            },
#                                        },
#                                        {
#                                            "type": "express",
#                                            "category": "Emotion",
#                                            "name": "expressFear",
#                                            "shape": ["blockVertical"],
#                                            "languages": {"ES": "expresar_miedo", "EN": "express_Fear"},
#                                            "tooltip": {
#                                                "ES": "Muestra la cara de miedo en el robot",
#                                                "EN": "Show the face of fear in the robot",
#                                            },
#                                        },
#                                        {
#                                            "type": "express",
#                                            "category": "Emotion",
#                                            "name": "expressSadness",
#                                            "shape": ["blockVertical"],
#                                            "languages": {"ES": "expresar_tristeza", "EN": "express_Sadness"},
#                                            "tooltip": {
#                                                "ES": "Muestra la cara de tristeza en el robot",
#                                                "EN": "Show the face of sadness in the robot",
#                                            },
#                                        },
#                                        {
#                                            "type": "express",
#                                            "category": "Emotion",
#                                            "name": "expressAnger",
#                                            "shape": ["blockVertical"],
#                                            "languages": {"ES": "expresar_ira", "EN": "express_Anger"},
#                                            "tooltip": {
#                                                "ES": "Muestra la cara de ira en el robot",
#                                                "EN": "Show the face of anger in the robot",
#                                            },
#                                        },
#                                        {
#                                            "type": "express",
#                                            "category": "Emotion",
#                                            "name": "expressDisgust",
#                                            "shape": ["blockVertical"],
#                                            "languages": {"ES": "expresar_asco", "EN": "express_Disgust"},
#                                            "tooltip": {
#                                                "ES": "Muestra la cara de asco en el robot",
#                                                "EN": "Show the face of disgust in the robot",
#                                            },
#                                        },
#                                        {
#                                            "type": "express",
#                                            "category": "Emotion",
#                                            "name": "expressSurprise",
#                                            "shape": ["blockVertical"],
#                                            "languages": {"ES": "expresar_sorpresa", "EN": "express_Surprise"},
#                                            "tooltip": {
#                                                "ES": "Muestra la cara de sorpresa en el robot",
#                                                "EN": "Show the face of surprise in the robot",
#                                            },
#                                        },
#                                        {
#                                            "type": "express",
#                                            "category": "Speaker",
#                                            "name": "say_Text",
#                                            "variables": [
#                                                {
#                                                    "type": "string",
#                                                    "name": "text",
#                                                    "default": "text",
#                                                    "translate": {"ES": "texto", "EN": "text"},
#                                                }
#                                            ],
#                                            "shape": ["blockVertical"],
#                                            "languages": {"ES": "decir_Texto", "EN": "say_Text"},
#                                            "tooltip": {"ES": "Decir texto", "EN": "Say text"},
#                                        },
#                                        {
#                                            "type": "proprioceptive",
#                                            "category": "Emotion",
#                                            "name": "is_Angry",
#                                            "shape": ["blockLeft", "blockBoth"],
#                                            "languages": {"ES": "estoy_Enfadado", "EN": "is_Angry"},
#                                        },
#                                        {
#                                            "type": "proprioceptive",
#                                            "category": "Emotion",
#                                            "name": "is_Disgust",
#                                            "shape": ["blockLeft", "blockBoth"],
#                                            "languages": {"ES": "estoy_Disgustado", "EN": "is_Disgust"},
#                                        },
#                                        {
#                                            "type": "proprioceptive",
#                                            "category": "Emotion",
#                                            "name": "is_Joy",
#                                            "shape": ["blockLeft", "blockBoth"],
#                                            "languages": {"ES": "estoy_Alegre", "EN": "is_Joy"},
#                                        },
#                                        {
#                                            "type": "proprioceptive",
#                                            "category": "Emotion",
#                                            "name": "is_Neutral",
#                                            "shape": ["blockLeft", "blockBoth"],
#                                            "languages": {"ES": "estoy_Neutral", "EN": "is_Neutral"},
#                                        },
#                                        {
#                                            "type": "proprioceptive",
#                                            "category": "Emotion",
#                                            "name": "is_Sadness",
#                                            "shape": ["blockLeft", "blockBoth"],
#                                            "languages": {"ES": "estoy_Triste", "EN": "is_Sadness"},
#                                        },
#                                        {
#                                            "type": "proprioceptive",
#                                            "category": "Emotion",
#                                            "name": "is_Scared",
#                                            "shape": ["blockLeft", "blockBoth"],
#                                            "languages": {"ES": "estoy_Asustado", "EN": "is_Scared"},
#                                        },
#                                        {
#                                            "type": "proprioceptive",
#                                            "category": "Emotion",
#                                            "name": "is_Surprised",
#                                            "shape": ["blockLeft", "blockBoth"],
#                                            "languages": {"ES": "estoy_Sorprendido", "EN": "is_Surprised"},
#                                        },
#                                        {
#                                            "type": "proprioceptive",
#                                            "category": "Base",
#                                            "name": "is_moving_left",
#                                            "shape": ["blockLeft", "blockBoth"],
#                                            "languages": {"ES": "estoy_moviendo_<--", "EN": "is_moving_left"},
#                                        },
#                                        {
#                                            "type": "proprioceptive",
#                                            "category": "Base",
#                                            "name": "is_moving_right",
#                                            "shape": ["blockLeft", "blockBoth"],
#                                            "languages": {"ES": "estoy_moviendo_-->", "EN": "is_moving_right"},
#                                        },
#                                        {
#                                            "type": "proprioceptive",
#                                            "category": "Base",
#                                            "name": "is_moving_straight",
#                                            "shape": ["blockLeft", "blockBoth"],
#                                            "languages": {"ES": "estoy_moviendo_recto", "EN": "is_moving_straight"},
#                                        },
#                                        {
#                                            "type": "proprioceptive",
#                                            "category": "Base",
#                                            "name": "is_turning",
#                                            "shape": ["blockLeft", "blockBoth"],
#                                            "languages": {"ES": "estoy_girando", "EN": "is_turning"},
#                                        },
#                                        {
#                                            "type": "proprioceptive",
#                                            "category": "Base",
#                                            "name": "is_turning_left",
#                                            "shape": ["blockLeft", "blockBoth"],
#                                            "languages": {"ES": "estoy_girando_<--", "EN": "is_turning_left"},
#                                        },
#                                        {
#                                            "type": "proprioceptive",
#                                            "category": "Base",
#                                            "name": "is_turning_right",
#                                            "shape": ["blockLeft", "blockBoth"],
#                                            "languages": {"ES": "estoy_girando_-->", "EN": "is_turning_right"},
#                                        },
#                                        {
#                                            "type": "perceptual",
#                                            "category": "Camera",
#                                            "name": "is_center_red_line",
#                                            "shape": ["blockLeft", "blockBoth"],
#                                            "languages": {"ES": "linea_roja_centro", "EN": "is_center_red_line"},
#                                        },
#                                        {
#                                            "type": "perceptual",
#                                            "category": "Camera",
#                                            "name": "is_left_red_line",
#                                            "shape": ["blockLeft", "blockBoth"],
#                                            "languages": {"ES": "linea_roja_izquierda", "EN": "is_left_red_line"},
#                                        },
#                                        {
#                                            "type": "perceptual",
#                                            "category": "Camera",
#                                            "name": "is_right_red_line",
#                                            "shape": ["blockLeft", "blockBoth"],
#                                            "languages": {"ES": "linea_roja_derecha", "EN": "is_right_red_line"},
#                                        },
#                                        {
#                                            "type": "perceptual",
#                                            "category": "Camera",
#                                            "name": "is_there_red_line",
#                                            "shape": ["blockLeft", "blockBoth"],
#                                            "languages": {"ES": "hay_linea_roja", "EN": "is_there_red_line"},
#                                        },
#                                        {
#                                            "type": "perceptual",
#                                            "category": "Camera",
#                                            "name": "is_center_black_line",
#                                            "shape": ["blockLeft", "blockBoth"],
#                                            "languages": {"ES": "linea_negra_centro", "EN": "is_center_black_line"},
#                                        },
#                                        {
#                                            "type": "perceptual",
#                                            "category": "Camera",
#                                            "name": "is_left_black_line",
#                                            "shape": ["blockLeft", "blockBoth"],
#                                            "languages": {"ES": "linea_negra_izquierda", "EN": "is_left_black_line"},
#                                        },
#                                        {
#                                            "type": "perceptual",
#                                            "category": "Camera",
#                                            "name": "is_right_black_line",
#                                            "shape": ["blockLeft", "blockBoth"],
#                                            "languages": {"ES": "linea_negra_derecha", "EN": "is_right_black_line"},
#                                        },
#                                        {
#                                            "type": "perceptual",
#                                            "category": "Camera",
#                                            "name": "is_there_black_line",
#                                            "shape": ["blockLeft", "blockBoth"],
#                                            "languages": {"ES": "hay_linea_negra", "EN": "is_there_black_line"},
#                                        },
#                                        {
#                                            "type": "perceptual",
#                                            "category": "Camera",
#                                            "name": "is_center_blue_line",
#                                            "shape": ["blockLeft", "blockBoth"],
#                                            "languages": {"ES": "linea_azul_centro", "EN": "is_center_blue_line"},
#                                        },
#                                        {
#                                            "type": "perceptual",
#                                            "category": "Camera",
#                                            "name": "is_left_blue_line",
#                                            "shape": ["blockLeft", "blockBoth"],
#                                            "languages": {"ES": "linea_azul_izquierda", "EN": "is_left_blue_line"},
#                                        },
#                                        {
#                                            "type": "perceptual",
#                                            "category": "Camera",
#                                            "name": "is_right_blue_line",
#                                            "shape": ["blockLeft", "blockBoth"],
#                                            "languages": {"ES": "linea_azul_derecha", "EN": "is_right_blue_line"},
#                                        },
#                                        {
#                                            "type": "perceptual",
#                                            "category": "Camera",
#                                            "name": "is_there_blue_line",
#                                            "shape": ["blockLeft", "blockBoth"],
#                                            "languages": {"ES": "hay_linea_azul", "EN": "is_there_blue_line"},
#                                        },
#                                        {
#                                            "type": "perceptual",
#                                            "category": "Camera",
#                                            "name": "is_left_face",
#                                            "shape": ["blockLeft", "blockBoth"],
#                                            "languages": {"ES": "cara_a_la_izquierda", "EN": "is_left_face"},
#                                        },
#                                        {
#                                            "type": "perceptual",
#                                            "category": "Camera",
#                                            "name": "is_right_face",
#                                            "shape": ["blockLeft", "blockBoth"],
#                                            "languages": {"ES": "cara_a_la_derecha", "EN": "is_right_face"},
#                                        },
#                                        {
#                                            "type": "perceptual",
#                                            "category": "Camera",
#                                            "name": "is_up_face",
#                                            "shape": ["blockLeft", "blockBoth"],
#                                            "languages": {"ES": "cara_arriba", "EN": "is_up_face"},
#                                        },
#                                        {
#                                            "type": "perceptual",
#                                            "category": "Camera",
#                                            "name": "is_down_face",
#                                            "shape": ["blockLeft", "blockBoth"],
#                                            "languages": {"ES": "cara_abajo", "EN": "is_down_face"},
#                                        },
#                                        {
#                                            "type": "perceptual",
#                                            "category": "Camera",
#                                            "name": "is_center_face",
#                                            "shape": ["blockLeft", "blockBoth"],
#                                            "languages": {"ES": "cara_en_el_centro", "EN": "is_center_face"},
#                                        },
#                                        {
#                                            "type": "perceptual",
#                                            "category": "Camera",
#                                            "name": "is_there_face",
#                                            "shape": ["blockLeft", "blockBoth"],
#                                            "languages": {"ES": "hay_cara", "EN": "is_there_face"},
#                                        },
#                                        {
#                                            "type": "perceptual",
#                                            "category": "Distances",
#                                            "name": "is_front_obstacle",
#                                            "variables": [
#                                                {
#                                                    "type": "float",
#                                                    "name": "threshold",
#                                                    "default": "200",
#                                                    "translate": {"ES": "umbral", "EN": "threshold"},
#                                                }
#                                            ],
#                                            "shape": ["blockLeft", "blockBoth"],
#                                            "languages": {"ES": "hay_algo_delante", "EN": "is_front_obstacle"},
#                                        },
#                                        {
#                                            "type": "perceptual",
#                                            "category": "Distances",
#                                            "name": "is_left_obstacle",
#                                            "variables": [
#                                                {
#                                                    "type": "float",
#                                                    "name": "threshold",
#                                                    "default": "200",
#                                                    "translate": {"ES": "umbral", "EN": "threshold"},
#                                                }
#                                            ],
#                                            "shape": ["blockLeft", "blockBoth"],
#                                            "languages": {"ES": "hay_algo_izquierda", "EN": "is_left_obstacle"},
#                                        },
#                                        {
#                                            "type": "perceptual",
#                                            "category": "Distances",
#                                            "name": "get_min_distance",
#                                            "variables": [
#                                                {
#                                                    "type": "boolean",
#                                                    "name": "left",
#                                                    "default": "0",
#                                                    "translate": {"ES": "izquierda", "EN": "left"},
#                                                },
#                                                {
#                                                    "type": "boolean",
#                                                    "name": "front",
#                                                    "default": "1",
#                                                    "translate": {"ES": "frente", "EN": "front"},
#                                                },
#                                                {
#                                                    "type": "boolean",
#                                                    "name": "right",
#                                                    "default": "0",
#                                                    "translate": {"ES": "derecha", "EN": "right"},
#                                                },
#                                            ],
#                                            "shape": ["blockLeft", "blockBoth"],
#                                            "languages": {"ES": "obtener_distancia", "EN": "get_min_distance"},
#                                        },
#                                        {
#                                            "type": "perceptual",
#                                            "category": "Camera",
#                                            "name": "is_line_crossing",
#                                            "shape": ["blockLeft", "blockBoth"],
#                                            "languages": {"ES": "hay_cruce", "EN": "is_line_crossing"},
#                                        },
#                                        {
#                                            "type": "perceptual",
#                                            "category": "Distances",
#                                            "name": "is_obstacle_free",
#                                            "variables": [
#                                                {
#                                                    "type": "float",
#                                                    "name": "threshold",
#                                                    "default": "200",
#                                                    "translate": {"ES": "umbral", "EN": "threshold"},
#                                                }
#                                            ],
#                                            "shape": ["blockLeft", "blockBoth"],
#                                            "languages": {"ES": "no_hay_obstaculos", "EN": "is_obstacle_free"},
#                                        },
#                                        {
#                                            "type": "perceptual",
#                                            "category": "Distances",
#                                            "name": "is_right_obstacle",
#                                            "variables": [
#                                                {
#                                                    "type": "float",
#                                                    "name": "threshold",
#                                                    "default": "200",
#                                                    "translate": {"ES": "umbral", "EN": "threshold"},
#                                                }
#                                            ],
#                                            "shape": ["blockLeft", "blockBoth"],
#                                            "languages": {"ES": "hay_algo_derecha", "EN": "is_right_obstacle"},
#                                        },
#                                        {
#                                            "type": "perceptual",
#                                            "category": "Camera",
#                                            "name": "is_any_face_happy",
#                                            "shape": ["blockLeft", "blockBoth"],
#                                            "languages": {"ES": "hay_alguien_alegre", "EN": "is_any_face_happy"},
#                                        },
#                                        {
#                                            "type": "perceptual",
#                                            "category": "Camera",
#                                            "name": "is_any_face_angry",
#                                            "shape": ["blockLeft", "blockBoth"],
#                                            "languages": {"ES": "hay_alguien_enfadado", "EN": "is_any_face_angry"},
#                                        },
#                                        {
#                                            "type": "perceptual",
#                                            "category": "Camera",
#                                            "name": "is_any_face_neutral",
#                                            "shape": ["blockLeft", "blockBoth"],
#                                            "languages": {"ES": "hay_alguien_neutral", "EN": "is_any_face_neutral"},
#                                        },
#                                        {
#                                            "type": "perceptual",
#                                            "category": "Camera",
#                                            "name": "is_any_face_sad",
#                                            "shape": ["blockLeft", "blockBoth"],
#                                            "languages": {"ES": "hay_alguien_triste", "EN": "is_any_face_sad"},
#                                        },
#                                        {
#                                            "type": "perceptual",
#                                            "category": "Camera",
#                                            "name": "is_any_face_surprised",
#                                            "shape": ["blockLeft", "blockBoth"],
#                                            "languages": {"ES": "hay_alguien_sorprendido",
#                                                          "EN": "is_any_face_surprised"},
#                                        },
#                                        {
#                                            "type": "perceptual",
#                                            "category": "Camera",
#                                            "name": "is_tag",
#                                            "variables": [
#                                                {
#                                                    "type": "float",
#                                                    "name": "idTag",
#                                                    "default": "8",
#                                                    "translate": {"ES": "id_marca", "EN": "id_Tag"},
#                                                }
#                                            ],
#                                            "shape": ["blockLeft", "blockBoth"],
#                                            "languages": {"ES": "veo_el_tag", "EN": "is_tag"},
#                                        },
#                                        {
#                                            "type": "perceptual",
#                                            "category": "Camera",
#                                            "name": "tag_on_the_left",
#                                            "shape": ["blockLeft", "blockBoth"],
#                                            "languages": {"ES": "tag_a_la_izquierda", "EN": "tag_on_the_left"},
#                                        },
#                                        {
#                                            "type": "perceptual",
#                                            "category": "Camera",
#                                            "name": "tag_on_the_right",
#                                            "shape": ["blockLeft", "blockBoth"],
#                                            "languages": {"ES": "tag_a_la_derecha", "EN": "tag_on_the_right"},
#                                        },
#                                        {
#                                            "type": "perceptual",
#                                            "category": "Camera",
#                                            "name": "tag_on_the_center",
#                                            "variables": [
#                                                {
#                                                    "type": "float",
#                                                    "name": "idTag",
#                                                    "default": "None",
#                                                    "translate": {"ES": "id_marca", "EN": "id_Tag"},
#                                                }
#                                            ],
#                                            "shape": ["blockLeft", "blockBoth"],
#                                            "languages": {"ES": "tag_en_el_centro", "EN": "tag_on_the_center"},
#                                        },
#                                        {
#                                            "type": "perceptual",
#                                            "category": "Camera",
#                                            "name": "is_any_tag",
#                                            "shape": ["blockLeft", "blockBoth"],
#                                            "languages": {"ES": "veo_algun_tag", "EN": "is_any_tag"},
#                                        },
#                                        {
#                                            "type": "perceptual",
#                                            "category": "Camera",
#                                            "name": "is_image",
#                                            "variables": [
#                                                {
#                                                    "type": "apriltext",
#                                                    "name": "id",
#                                                    "default": "0",
#                                                    "translate": {"ES": "identificador", "EN": "id"},
#                                                }
#                                            ],
#                                            "shape": ["blockLeft", "blockBoth"],
#                                            "languages": {"ES": "esta_la_imagen", "EN": "is_image"},
#                                            "tooltip": {
#                                                "ES": "Devuelve cierto si el robot esta viendo la imagen indicada como identificador",
#                                                "EN": "",
#                                            },
#                                        },
#                                        {
#                                            "type": "perceptual",
#                                            "category": "Ground",
#                                            "name": "is_there_ground",
#                                            "shape": ["blockLeft", "blockBoth"],
#                                            "languages": {"ES": "hay_suelo", "EN": "is_there_ground"},
#                                        },
#                                        {
#                                            "type": "perceptual",
#                                            "category": "Ground",
#                                            "name": "is_center_ground_line",
#                                            "shape": ["blockLeft", "blockBoth"],
#                                            "languages": {"ES": "linea_central_en_suelo", "EN": "is_center_ground_line"},
#                                        },
#                                        {
#                                            "type": "perceptual",
#                                            "category": "Ground",
#                                            "name": "is_right_ground_line",
#                                            "shape": ["blockLeft", "blockBoth"],
#                                            "languages": {"ES": "linea_derecha_en_suelo", "EN": "is_right_ground_line"},
#                                        },
#                                        {
#                                            "type": "perceptual",
#                                            "category": "Ground",
#                                            "name": "is_left_ground_line",
#                                            "shape": ["blockLeft", "blockBoth"],
#                                            "languages": {"ES": "linea_izquierda_en_suelo", "EN": "is_left_ground_line"},
#                                        },
#                                    ])



class ParserTesting(unittest.TestCase):
    def setUp(self):
        self.tree = Parser.parse_str(TEST_TEXT)

    def renew_temp_dir(self, name=None):
        self.tempdir = os.path.join(tempfile.gettempdir(), 'testlearnbot_tempdir_' + str(random.random())[2:])
        if name:
            self.tempdir = os.path.join(self.tempdir, name)
        shutil.rmtree(self.tempdir, ignore_errors=True)
        os.makedirs(self.tempdir)

    def test_parse_tree(self):
        self.assertEqual(self.tree.defs, [])
        self.assertEqual(self.tree.defs, [])
        self.assertEqual(self.tree.imports, [])
        self.assertEqual(self.tree.inits, [])
        self.assertEqual(self.tree.end, (5, 4, 21))
        self.assertEqual(self.tree.start, (3, 1, 2))
        self.assertEqual(self.tree.used_vars, {'x'})

    def test_python_generator(self):
        python_text = PythonGenerator.generate(self.tree)
        self.assertEqual(python_text, "x = 2")

    def test_type_checker(self):
        mismatches = Typechecker.check(self.tree)
        self.assertEqual(mismatches, [])

    def test_parser_learnbot(self):
        result = parserLearntBotCodeFromCode(TEST_TEXT, "robots")
        self.assertEqual(result, ('\n'
                                  '#EXECUTION: python code.py\n'
                                  'from __future__ import print_function, absolute_import\n'
                                  'import sys, os, time, traceback\n'
                                  'sys.path.insert(0, os.path.join(os.getenv(\'HOME\'), ".learnblock", "clients"))\n'
                                  'from robots import Robot\n'
                                  'import signal\n'
                                  'import sys\n'
                                  '\n'
                                  'usedFunctions = []\n'
                                  '\n'
                                  'try:\n'
                                  '\trobot = Robot(availableFunctions = usedFunctions)\n'
                                  'except Exception as e:\n'
                                  '\tprint("Problems creating a robot instance")\n'
                                  '\ttraceback.print_exc()\n'
                                  '\traise(e)\n'
                                  '\n'
                                  '\n'
                                  'time_global_start = time.time()\n'
                                  'def elapsedTime(umbral):\n'
                                  '\tglobal time_global_start\n'
                                  '\ttime_global = time.time()-time_global_start\n'
                                  '\treturn time_global > umbral\n'
                                  '\n'
                                  '\n'
                                  'def signal_handler(sig, frame):\n'
                                  '\trobot.stop()\n'
                                  '\tsys.exit(0)\n'
                                  '\n'
                                  'signal.signal(signal.SIGTERM, signal_handler)\n'
                                  'signal.signal(signal.SIGINT, signal_handler)\n'
                                  '\n'
                                  'x = 2\n'
                                  'robot.stop()\n'
                                  'sys.exit(0)\n'
                                  '\n'
                                  '', []))

    def test_block_examples_genaration(self):
        # if not os.path.isdir("resources/examples") or len(os.listdir("resources/examples"))==0:
        #     os.system("curl -L https://github.com/robocomp/LearnBlock/archive/examples.tar.gz | tar -xz --one-top-level=reference_examples --strip-components=1 -C resources")

        code_blocks_found = []
        for root, dirs, files in os.walk("resources/reference_examples"):
            for name in files:
                if name.endswith(".blockText"):
                    code_blocks_found.append((root, name))
        self.code_generation(code_blocks_found)

    def code_generation(self, block_file_list):
        for current_block_path, current_block_file in block_file_list:
            full_block_file_path = os.path.join(CURRENT_DIR, current_block_path, current_block_file)
            self.renew_temp_dir(current_block_path)
            block_file_path = shutil.copy(full_block_file_path, self.tempdir)
            self.olddir = os.getcwd()
            os.chdir(self.tempdir)
            output_python_file = current_block_file.replace('.blockProject', '.py')
            output_python_path = os.path.join(self.tempdir, output_python_file)
            client_name = "EBO"
            try:
                parserLearntBotCode(block_file_path, output_python_path,client_name)
            except Exception as e:
                self.fail(str(e))
            else:
                reference_python_path = full_block_file_path.replace(".blockText", ".py")
                print(f"Comparing generated python code from \n\t{full_block_file_path} with {reference_python_path}")
                self.assertFilesSame(reference_python_path, output_python_path)
            finally:
                os.chdir(self.olddir)
                shutil.rmtree(self.tempdir, ignore_errors=True)

    # def test_invalid_language(self):
    #     self.renew_temp_dir("Invalid")
    #     cdsl = os.path.join(RESOURCES_DIR, "InvalidLanguage.cdsl")
    #     # self.assertRaises(ValueError, FilesGenerator().generate, cdsl, self.tempdir, [])
    #     shutil.rmtree(self.tempdir, ignore_errors=True)


    def assertFilesSame(self, path1, path2):
        with open(path1, 'r', encoding='utf-8', errors='ignore') as f1, open(path2, 'r', encoding='utf-8', errors='ignore') as f2:
            text1 = f1.readlines()
            text2 = f2.readlines()
        self.assertEqual(text1, text2)

    # def compare_generated_code(self, reference, generated):
    #     for root, dirnames, filenames in os.walk(reference):
    #         ref_root = root.replace(reference, generated)
    #         generated_files = os.listdir(ref_root)
    #         for filename in filenames:
    #             with self.subTest("Component comparation for %s" % root, directory=root, filename=filename):
    #                 if filename in generated_files:
    #                     self.assertFilesSame(
    #                         os.path.join(root, filename),
    #                         os.path.join(ref_root, filename)
    #                     )
    #                 else:
    #                     self.fail("File %s found in reference is not in generated comp" % filename)



if __name__ == '__main__':
    unittest.main()
