from __future__ import print_function, absolute_import
import py_compile, sys, traceback

def compile(file):
    try:
        py_compile.compile(file, doraise=True)
        return True
    except py_compile.PyCompileError as e:
        traceback.print_exc()
        return False
