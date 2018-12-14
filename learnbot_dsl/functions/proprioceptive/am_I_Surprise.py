from learnbot_dsl.LearnBotClient import *

def am_I_Surprise(lbot):
    if lbot.getCurrentEmotion() == Surprise:
        return True
    return False
