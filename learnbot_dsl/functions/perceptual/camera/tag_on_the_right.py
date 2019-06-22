from __future__ import print_function, absolute_import

def tag_on_the_right(lbot, idTag=None):
    pos = lbot.getPosTag(idTag)
    if pos is not None:
        if pos[0]-320/2 > 320//8:
            return True
        else:
            return False
    return False
