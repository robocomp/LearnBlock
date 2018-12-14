from learnbot_dsl.LearnBotClient import *

def am_I_Neutral(lbot):
    if lbot.getCurrentEmotion() == Neutral:
        return True
    return False
