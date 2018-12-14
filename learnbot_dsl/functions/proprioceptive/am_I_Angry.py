from learnbot_dsl.LearnBotClient import *

def am_I_Angry(lbot):
    if lbot.getCurrentEmotion() == Anger:
        return True
    return False
