from setuptools import setup, find_packages
# from distutils.core import setup
import tempfile
import os

def read(fname):
    try:
         text = open(os.path.join(os.path.dirname(__file__), fname)).read()
    except:
          text = ""
    return text
exclude=['components']

setup(name="learnbot_dsl",
      version="0.1.19",
      description="Learnblock is a IDE for program learnbot using blocks",
      author="Ivan Barbecho",
      author_email="ivanbd@unex.es",
      url="https://github.com/robocomp/learnbot",
      license="GPL",
      scripts=[
            'learnbot_dsl/learnbotCode/Learnblock',
            'learnbot_dsl/components/apriltag/src/aprilTag.py',
            'learnbot_dsl/components/emotionrecognition2/src/emotionrecognition2.py'],
      packages=find_packages(exclude=exclude),
      include_package_data=True,
      package_data={'':["*"], 'learnbot_dsl':["*", "interfaces/*","*.md"]},
      zip_safe=False,
      long_description=read('learnbot_dsl/description.md'),
      long_description_content_type='text/markdown',
      install_requires=[
            "requests",
            "pyunpack",
            "patool",
            "opencv-python-headless==3.4.3.18",
            # 'numpy==1.14.5',
            'matplotlib==2.2.2',
            # 'pyparsing==2.0.3',
            'imutils==0.5.1',
            'six==1.10.0',
            'scipy==1.0.0',
            'tensorflow==1.10.1',
            'dlib==19.13.1',
            'pandas==0.19.1',
            'paramiko==2.4.1',
            'Keras==2.0.5',
            'h5py==2.7.0',
            'epitran==0.4',
            # 'zeroc-ice==3.6.0',
            'Pillow==5.3.0',
            # 'PySide',
            'GitPython==2.1.11',
            'paho_mqtt==1.4.0'],
      )


# from pyunpack import Archive
# import requests
# tempfile.tempdir = tempfile.mkdtemp("xmls-ebo")
# r = requests.get("https://github.com/robocomp/learnbot/archive/xmls.zip")
# pathzip = os.path.join(tempfile.gettempdir(),"xmls.zip")
#
# with open(pathzip, "wb") as code:
#     code.write(r.content)
#
# Archive(pathzip).extractall(os.environ.get('HOME'))
#
# for f in os.listdir(tempfile.gettempdir()):
#       os.remove(os.path.join(tempfile.gettempdir(),f))
# os.removedirs(tempfile.gettempdir())

# deskLauncher = raw_input("Do you want to have a launcher on your desk?[Y/N]")
#
# if deskLauncher == "Y":
#       with open(os.path.join(os.getenv('DESKTOP_DIR'),"Learnblock.desktop"),'wr') as f:
#             f.write("[Desktop Entry]")
#             f.write("Version = 1.0")
#             f.write("Type = Application")
#             f.write("Name = Learnblock")
#             f.write("Comment = ")
#             f.write("Exec = Learnblock")
#             f.write("Icon =$path/learnbot_dsl/learnbotCode/ico.png")
#             f.write("Path = ~")
#             f.write("Terminal = false")
#             f.write("StartupNotify = false")
