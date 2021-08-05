import Ice
import sys
import time
import numpy as np
import subprocess

import cv2

Ice.loadSlice("-I ./src/ --all ./DetectionComponent.ice")

from RoboCompDetectionComponent import *

def connectComponent(ic, stringProxy, _class, tries=4):

    i = 0
    while True:
        try:
            i += 1
            print(f"Try {i}")
            basePrx = ic.stringToProxy(stringProxy)
            proxy = _class.checkedCast(basePrx)
            print("Connection Successful:", stringProxy)
            break
        except Ice.Exception as e:
            if i is tries:
                print("Cannot connect to the proxy:", stringProxy)
                return None
            else:
                time.sleep(1.5)
    return proxy


if __name__ == "__main__":
    # Initialize the communicator of Ice
    ic = Ice.initialize(sys.argv)

    # Uncomment the following line to open automatically the component
    #subprocess.Popen("/home/alejandro/LearnBlock/learnbot_dsl/components/Detection/src/detectioncomponent.py", shell=True, stdout=subprocess.PIPE)

    # Connecting to the component in the port 10010 of localhost
    component_proxy = connectComponent(ic, "detectioncomponent:tcp -h localhost -p 10010", DetectionComponentPrx,10)

    # Test the setter and getter of the threshold of the component
    print(component_proxy.getThreshold())
    component_proxy.setThreshold(0.1)
    print(component_proxy.getThreshold())
    component_proxy.setThreshold(0.3)

    # Test the processing of the image by the component

    # Prepare the image for the component
    img = cv2.imread("../test/test.jpg")
    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
    img = cv2.resize(img,(448,448))

    # Create the input of the component according to the interface
    frame = TImage()
    frame.width = img.shape[0]
    frame.height = img.shape[1]
    frame.depth = img.shape[2]
    frame.image = bytes(img)

    # Get the predictions of the component
    predictions = component_proxy.processImage(frame)

    # Print the predictions
    for pred in predictions:
        print(f"Box location=({pred.x},{pred.y}),Width={pred.w},Height={pred.h},Label={pred.label}")

    # Destroy the communicator to ensure the program finishes properly
    ic.destroy()
