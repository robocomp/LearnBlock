from threading import Lock

LANGUAGE = "ES"
mutex = Lock()


def changeLanguageTo(l):
    global LANGUAGE
    global mutex
    mutex.acquire()
    LANGUAGE = l
    mutex.release()


def getLanguage():
    global LANGUAGE
    global mutex
    mutex.acquire()
    l = LANGUAGE
    mutex.release()
    return l
