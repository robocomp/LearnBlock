from learnbot_dsl.Clients.Devices import Emotions

def is_Disgust(lbot):
    if lbot.getCurrentEmotion() == Emotions.Disgust:
        return True
    return False
