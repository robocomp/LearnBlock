from learnbot_dsl.LearnBotClient import *

def am_I_Disgust(lbot):
    if lbot.getCurrentEmotion() == Disgust:
        return True
    return False
