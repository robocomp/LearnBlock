import inspect
import os
path = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))

__all__ = ["pathBlocks"]

pathBlocks = path