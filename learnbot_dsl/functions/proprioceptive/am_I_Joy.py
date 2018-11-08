from learnbot_dsl.LearnBotClient import *

def am_I_Joy(lbot):
    if lbot.getCurrentEmotion() == Joy:
        return True
    return False
