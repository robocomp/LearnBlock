from __future__ import print_function, absolute_import

def is_there_ground(lbot):
    gsensors = lbot.getGroundSensors()
    if gsensors is not None:
        for key in gsensors.keys():
            if gsensors[key] is not None:
                if gsensors[key]<=50:
                    return False
    return True
