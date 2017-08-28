import py_compile

def compile(file):
    try:
        py_compile.compile(file, doraise=True)
        return True
    except:
        return False
