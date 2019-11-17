# -*- coding: utf-8 -*-

from __future__ import print_function, absolute_import
import os, json
from learnbot_dsl.blocksConfig.blocks import pathBlocks as pathImgBlocks

pathConfig = os.path.dirname(os.path.realpath(__file__))

renamedB = {"blockVertical":"block1", "blockBoth":"block3", "blockLeft":"block4"}


def reload_functions(selected_path=None):
    blocks = None

    if selected_path is None:
        selected_path = os.path.join(pathConfig, "default")

    basic_path = os.path.join(pathConfig, "basic")

    pathsConfig = [basic_path, selected_path,
                   os.path.join(os.getenv('HOME'), ".learnblock", "block")
                   ]
    for path in pathsConfig:
        if not os.path.exists(path):
            continue
        for f in os.listdir(path):
            if os.path.splitext(f)[-1] == ".conf":
                f = os.path.join(path, f)
                print(f)
                with open(f, "rb") as f:
                    text = f.read()
                if blocks is None:
                    blocks = json.loads(text)
                else:
                    blocks += json.loads(text)

    return blocks

def renameBlock(name):
    if name in renamedB.keys():
        return renamedB[name]
    return name

def getOrigNameBlock(name):
    if name in renamedB.values():
        return list(renamedB.keys())[list(renamedB.values()).index(name)]
    return name


if __name__ == '__main__':
    blocks = reload_functions()
    from learnbot_dsl.functions import getFuntions
    functions = getFuntions()
    nameconfigBlocks = [x["name"] for x in blocks]
    for x in nameconfigBlocks:
        if x not in functions:
            print(x)
