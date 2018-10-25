from __future__ import print_function, absolute_import


def is_there_somebody_surprised(lbot, params=None, verbose=False):
    emotions = lbot.getEmotions()
    print(emotions)
    for e in emotions:
        if e.emotion =="Surprised":
            return True
    return False