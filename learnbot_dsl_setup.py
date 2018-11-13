from setuptools import setup, find_packages
import os, sys, shutil


def read(fname):
    with open(os.path.join(os.path.dirname(__file__), fname)) as f:
        return f.read()


def readVersion(fname):
    with open(fname, 'rb') as f:
        for l in f.readlines():
            if '__version__' in l:
                return l.split("=")[-1].replace("'", "").replace(" ", "")


def listmdfiles(path, rpPath):
    dirs = [path]
    ret = []
    for dir in dirs:
        sublist = []
        for subpath in os.listdir(dir):
            absPath = os.path.join(dir, subpath)
            if os.path.isdir(absPath):
                dirs.append(absPath)
            else:
                sublist.append(absPath.replace(rpPath, ""))
        if len(sublist) is not 0:
            ret.append((os.path.join("share", os.path.dirname(absPath).replace(rpPath, "")), sublist))
    return ret


data_files = listmdfiles(os.path.join(os.path.dirname(__file__), "learnbot_dsl", "mdfiles"), os.path.dirname(__file__))
data_files += [
    ('share/applications', ['learnbot_dsl/Learnblock.desktop']),
    ('share/icons', ['learnbot_dsl/learnbotCode/Learnbot_ico.png']),
]
# preinstall qmake
# sudo apt install qt4-dev-tools

setup(name="learnbot_dsl",
      version=readVersion(os.path.join(os.path.dirname(__file__), "learnbot_dsl", "__init__.py")),
      description="Learnblock is a IDE for program learnbot using blocks",
      author="Ivan Barbecho",
      author_email="ivanbd@unex.es",
      url="https://github.com/robocomp/learnbot",
      license="GPL",
      scripts=[
          'learnbot_dsl/learnbotCode/Learnblock',
          'learnbot_dsl/components/apriltag/src/aprilTag.py',
          'learnbot_dsl/components/emotionrecognition2/src/emotionrecognition2.py'],
      packages=find_packages(where=".", exclude=['learnbot_components*']),
      include_package_data=True,
      package_data={'': ["*"], 'learnbot_dsl': ["*", "interfaces/*", "*.md"]},
      data_files=data_files,
      zip_safe=False,
      long_description=read('learnbot_dsl/description.md'),
      long_description_content_type='text/markdown',
      python_requires='>=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, !=3.4.*, <4',
      install_requires=[
          "requests",
          "pyunpack",
          # "patool",
          "opencv-python-headless==3.4.3.18",
          # 'numpy==1.14.5',
          # 'matplotlib==2.2.2',
          'imutils==0.5.1',
          'six==1.10.0',
          # 'scipy==1.0.0',
          'tensorflow==1.10.1',
          'dlib==19.13.1',
          # 'pandas==0.19.1',
          'paramiko==2.4.1',
          # 'Keras==2.0.5',
          # 'h5py==2.7.0',
          # 'epitran==0.4',
          'Pillow==5.3.0',
          # 'GitPython==2.1.11',
          'paho_mqtt==1.4.0',
          # 'pyside',
          # 'zeroc-ice==3.6.0',
          # 'pyparsing==2.0.3',
          # 'cmake',
          'future'
          ],
      )
if os.path.exists("build.learnbot_dsl"):
    shutil.rmtree("build.learnbot_dsl")
if os.path.exists("build"):
    shutil.move("build", 'build.learnbot_dsl')
