from __future__ import print_function, absolute_import


def is_any_face_neutral(lbot):
    emotions = lbot.getEmotions()
    for e in emotions:
        if e.emotion =="Neutral":
            return True
    return False