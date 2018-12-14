from learnbot_dsl.LearnBotClient import *

def am_I_Scared(lbot):
    if lbot.getCurrentEmotion() == Fear:
        return True
    return False
