from __future__ import print_function, absolute_import
import py_compile, sys

def compile(file):
    try:
        py_compile.compile(file, doraise=True)
        return True
    except py_compile.PyCompileError as e:
        print(e)
        return False
