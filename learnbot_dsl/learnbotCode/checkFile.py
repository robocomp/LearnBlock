import py_compile

def compile(file):
    try:
        py_compile.compile(file, doraise=True)
        return True
    except py_compile.PyCompileError as e:
        print e
        return False
