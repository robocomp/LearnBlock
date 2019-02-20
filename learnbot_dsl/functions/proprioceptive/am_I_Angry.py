from learnbot_dsl.Clients.Devices import Emotions

def am_I_Angry(lbot):
    if lbot.getCurrentEmotion() == Emotions.Anger:
        return True
    return False
