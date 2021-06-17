


def RGBled(lbot, r,g,b,keyLed):
    if keyLed is None:
        keyLed="ROBOT"
    lbot.setLedColorState(r,g,b,keyLed)
