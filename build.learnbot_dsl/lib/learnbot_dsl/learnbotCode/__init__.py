from __future__ import print_function, absolute_import
import os, json

file = os.path.join(os.getenv('HOME'), ".learnblock", "AprilDict.json")

def getAprilTextDict():
    if os.path.exists(file):
        with open(file, "r") as f:
            dictAprilTags = json.load(f)
        return dictAprilTags
    return {}
