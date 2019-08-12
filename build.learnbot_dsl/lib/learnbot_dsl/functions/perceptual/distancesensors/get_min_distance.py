def get_min_distance(lbot, left=0, front=1, right=0):
    sonarsValue = lbot.getSonars()
    if left:
        return min(sonarsValue["left"])
    elif front:
        return min(sonarsValue["front"])
    elif right:
        return min(sonarsValue["right"])
    else:
        return min(map(lambda x: min(x), sonarsValue.values()))
