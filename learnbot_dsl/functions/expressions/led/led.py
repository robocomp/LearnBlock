


def led(lbot,intensity,keyLed):
    if keyLed is None:
        keyLed="ROBOT"
    lbot.setLedColorState(intensity,keyLed)
