from learnbot_dsl.Clients.Devices import Emotions


def expressJoy(lbot):
    print("expressJoy")
    lbot.express(Emotions.Joy)
