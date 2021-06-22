def is_this_code_IR(lbot, code=0):
    IRValue=lbot.getIR()
    if IRValue == None:
        return False
    if IRValue == code:
        return True
    return False
