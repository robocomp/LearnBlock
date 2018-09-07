from __future__ import print_function


def is_there_somebody_sad(lbot, params=None, verbose=False):
    emotions = lbot.getEmotions()
    print(emotions)
    for e in emotions:
        if e.emotion =="Sad":
            return True
    return False