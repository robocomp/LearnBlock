from __future__ import print_function, absolute_import

def is_any_tag(lbot):
    lbot.lookingLabel(0)
    return len(lbot.listTags()) is not 0
