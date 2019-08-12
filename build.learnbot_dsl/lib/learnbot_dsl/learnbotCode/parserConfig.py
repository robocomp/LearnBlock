from __future__ import print_function, absolute_import
import os, sys, traceback
from pyparsing import *

path = os.path.dirname(os.path.realpath(__file__))

reserved_words = (Keyword('=') | Keyword('command.') | Keyword('learnbot.') | Keyword('ip') | Keyword('user') | Keyword(
    'pass') | Keyword('start') | Keyword('stop'))
iden = Word(alphanums + "_")
identifier = Group(~reserved_words + iden)

IP = Suppress("learnbot.ip") + Suppress("=") + QuotedString('"').setResultsName("ip")
USER = Suppress("learnbot.user") + Suppress("=") + QuotedString('"').setResultsName("user")
PASS = Suppress("learnbot.pass") + Suppress("=") + QuotedString('"').setResultsName("pass")
START = Suppress("learnbot.command.start") + Suppress("=") + QuotedString('"').setResultsName("start")
START_SIMULATOR = Suppress("learnbot.command.start_simulator") + Suppress("=") + QuotedString('"').setResultsName(
    "start_simulator")
STOP = Suppress("learnbot.command.stop") + Suppress("=") + QuotedString('"').setResultsName("stop")

PARSERCONFIG = OneOrMore(IP | USER | PASS | START | STOP | START_SIMULATOR)


def __parserFromFile(file):
    with open(file) as f:
        text = f.read()
        ret = __parserFromString(text)
        # print(ret)
        return ret


def __parserFromString(text):
    try:
        PARSERCONFIG.ignore(pythonStyleComment)
        return PARSERCONFIG.parseString(text)
    except Exception as e:
        traceback.print_exc()
        print("line: {}".format(e.line))
        print("    " + " " * e.col + "^")
        raise e
        exit(-1)


configSSH = __parserFromFile(os.path.join(path, "etc","config"))


def reloadConfig():
    global configSSH
    configSSH = __parserFromFile(os.path.join(path, "etc","config"))


__all__ = ['configSSH']
