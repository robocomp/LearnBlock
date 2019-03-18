from learnbot_dsl.Clients.Devices import Emotions

def am_I_Disgust(lbot):
    if lbot.getCurrentEmotion() == Emotions.Disgust:
        return True
    return False
