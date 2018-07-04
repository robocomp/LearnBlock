
import time

def sleep(lbot, seconds):
    time.sleep(seconds)
    lbot.publish_topic("sleep")
