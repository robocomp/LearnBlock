from __future__ import print_function, absolute_import


def is_any_face_angry(lbot):
    emotions = lbot.getEmotions()
    for e in emotions:
        if e.emotion =="Angry":
            return True
    return False