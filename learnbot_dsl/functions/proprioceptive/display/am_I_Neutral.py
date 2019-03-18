from learnbot_dsl.Clients.Devices import Emotions

def am_I_Neutral(lbot):
    if lbot.getCurrentEmotion() == Emotions.Neutral:
        return True
    return False
