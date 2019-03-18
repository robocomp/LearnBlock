from learnbot_dsl.Clients.Devices import Emotions

def am_I_Scared(lbot):
    if lbot.getCurrentEmotion() == Emotions.Fear:
        return True
    return False
