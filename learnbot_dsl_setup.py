from setuptools import setup, find_packages
import os, sys, shutil


def read(fname):
    with open(os.path.join(os.path.dirname(__file__), fname)) as f:
        return f.read()


def readVersion(fname):
    with open(fname, 'r') as f:
        for l in f.readlines():
            if '__version__' in l:
                return l.split('=')[-1].replace("'", "").replace(" ", "")


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
      keywords='Visual programming language for robots.',
      description="Learnblock is an IDE for program robots using blocks",
      author="Ivan Barbecho, Pilar Bachiller",
      author_email="ivanbd@unex.es, pilarb@unex.es",
      project_urls={
          'Documentation': 'https://github.com/robocomp/learnbot/wiki',
          'Funding': 'https://www.paypal.com/cgi-bin/webscr?cmd=_s-xclick&hosted_button_id=N3VAYG9VP8S4L',
          # 'Say Thanks!': 'http://saythanks.io/to/example',
          'Source': 'https://github.com/robocomp/learnbot',
          'Tracker': 'https://github.com/robocomp/learnbot/issues',
      },
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
      classifiers = [
            'Development Status :: 4 - Beta',
            'Intended Audience :: Education',
            'License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)',
            'Operating System :: MacOS :: MacOS X',
            'Operating System :: POSIX',
            'Operating System :: POSIX :: Linux',
            # 'Programming Language :: Python :: 2',
            #'Programming Language :: Python :: 2.7',
            # 'Programming Language :: Python :: 3',
            # 'Programming Language :: Python :: 3.3',
            'Programming Language :: Python :: 3.4',
            'Programming Language :: Python :: 3.5',
            'Programming Language :: Python :: 3.6',
            'Programming Language :: Python :: 3.7',
            'Environment :: X11 Applications :: Qt',
          ],
      long_description_content_type='text/markdown',
      # python_requires='==2.7, ==3.4, ==3.5, ==3.6',
      platforms=["Posix",
                 "MacOS",],
      install_requires=[
          "apriltag",
          "requests>=2.20.0",
          "pyunpack>=0.1.2",
          # "patool",
          "opencv-python-headless>=3.4.3.18",
          # 'numpy>=1.14.5',
          # 'matplotlib>=2.2.2',
          'imutils>=0.5.1',
          'six>=1.10.0',
          # 'scipy>=1.0.0',
          'tensorflow>=1.10.1',
          'dlib>=19.13.1',
          # 'pandas>=0.19.1',
          'paramiko>=2.4.2',
          # 'Keras>=2.0.5',
          # 'h5py>=2.7.0',
          # 'epitran>=0.4',
          'Pillow>=5.3.0',
          # 'GitPython>=2.1.11',
          'paho_mqtt>=1.4.0',
          'PySide2',
          # 'zeroc-ice>=3.6.0',
          'pyparsing>=2.0.3',
          # 'cmake',
          'qdarkstyle',
          'future>=0.16.0'
          ],
      )
if os.path.exists("build.learnbot_dsl"):
    shutil.rmtree("build.learnbot_dsl")
if os.path.exists("build"):
    shutil.move("build", 'build.learnbot_dsl')
