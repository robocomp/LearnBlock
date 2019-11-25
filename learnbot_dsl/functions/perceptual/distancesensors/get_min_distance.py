def get_min_distance(lbot, left=0, front=1, right=0):
    distanceValues = lbot.getDistanceSensors()
    if distanceValues is not None:
        if left:
            return min(distanceValues["left"])
        elif front:
            return min(distanceValues["front"])
        elif right:
            return min(distanceValues["right"])
        else:
            return min(map(lambda x: min(x), distanceValues.values()))
    return 0
