from __future__ import print_function


def is_there_somebody_neutral(lbot, params=None, verbose=False):
    emotions = lbot.getEmotions()
    print(emotions)
    for e in emotions:
        if e.emotion =="Neutral":
            return True
    return False