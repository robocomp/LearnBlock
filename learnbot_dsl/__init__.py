from __future__ import print_function, absolute_import
import os, sys
# import learnbot_dsl.LearnBotClient as LearnBotClient
# import learnbot_dsl.learnbotCode as learnbotCode
# import learnbot_dsl.components as components
# import learnbot_dsl.LearnBotClient_PhysicalRobot as LearnBotClient_PhysicalRobot
# import learnbot_dsl.functions as functions
# import learnbot_dsl.guis as guis
# __all__ = ['LearnBotClient', 'learnbotCode', 'components', 'LearnBotClient_PhysicalRobot', 'functions', 'guis']

path = os.path.dirname(os.path.realpath(__file__))
# sys.path.append(path)


# ignore = [
#     '__init__.py',
#     # 'functions',
#     '__pycache__',
#     'interfaces'
# ]
# for filename in os.listdir(path):
#     fullname = os.path.join(path, filename)
#     name, extension = os.path.splitext(filename)
#     if (os.path.isfile(fullname) and extension != '.py') or filename in ignore:
#         continue
#     __all__.append(name)
# print(__all__)