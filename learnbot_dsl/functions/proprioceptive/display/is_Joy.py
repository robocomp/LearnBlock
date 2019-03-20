from learnbot_dsl.Clients.Devices import Emotions

def is_Joy(lbot):
    if lbot.getCurrentEmotion() == Emotions.Joy:
        return True
    return False
