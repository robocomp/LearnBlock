from __future__ import print_function, absolute_import


def is_any_face_sad(lbot, params=None, verbose=False):
    emotions = lbot.getEmotions()
    for e in emotions:
        if e.emotion =="Sad":
            return True
    return False