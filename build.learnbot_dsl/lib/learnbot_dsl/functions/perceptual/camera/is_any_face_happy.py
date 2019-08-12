from __future__ import print_function, absolute_import


def is_any_face_happy(lbot):
    emotions = lbot.getEmotions()
    for e in emotions:
        if e.emotion =="Happy":
            return True
    return False