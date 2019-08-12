from learnbot_dsl.Clients.Devices import Emotions

def is_Scared(lbot):
    if lbot.getCurrentEmotion() == Emotions.Fear:
        return True
    return False
