


class Variable():
    def __init__(self,type,name,defaul):
        self.type = type
        self.name = name
        self.defaul = defaul

class Block():
    def __init__(self,name,funtionType,listVar = None,file = None):
        self.listImg=[]
        self.name = name
        self.funtionType = funtionType
        self.listVar = listVar
        self.file = file