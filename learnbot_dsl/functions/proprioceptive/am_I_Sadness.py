from learnbot_dsl.LearnBotClient import *

def am_I_Sadness(lbot):
    if lbot.getCurrentEmotion() == Sadness:
        return True
    return False
