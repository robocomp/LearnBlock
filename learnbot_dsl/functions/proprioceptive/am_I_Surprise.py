from learnbot_dsl.Clients.Devices import Emotions

def am_I_Surprise(lbot):
    if lbot.getCurrentEmotion() == Emotions.Surprise:
        return True
    return False
