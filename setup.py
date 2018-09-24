from distutils.core import setup
import os
import inspect
path = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))+"/"
setup(name="learnbot",
      version="0.1",
      description="learnbot cliente",
      author="Ivan Barbecho",
#      author_email="",
#      url="",
      license="GPL",
#      scripts=["ejemplo.py"],
      packages=[path+"learnbot_dsl",path+"learnbot_dsl/functions",path+"learnbot_dsl/functions/motor",path+"learnbot_dsl/functions/others",path+"learnbot_dsl/functions/perceptual",path+"learnbot_dsl/functions/proprioceptive",path+"learnbot_dsl/functions/expressions"],
      )
