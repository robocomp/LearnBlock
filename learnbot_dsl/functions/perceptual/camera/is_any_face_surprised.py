from __future__ import print_function, absolute_import


def is_any_face_surprised(lbot, params=None, verbose=False):
    emotions = lbot.getEmotions()
    for e in emotions:
        if e.emotion =="Surprised":
            return True
    return False