from setuptools import setup, find_packages
import os,sys, shutil
def read(fname):
      with open(os.path.join(os.path.dirname(__file__), fname)) as f:
            return f.read()
def readVersion(fname):
    with open(fname,'rb') as f:
        for l in f.readlines():
            if '__version__' in l:
                return l.split("=")[-1].replace("'","").replace(" ","")
setup(name="EBO_components",
      version=readVersion(os.path.join(os.path.dirname(__file__), "EBO_components", "__init__.py")),
      description="EBO_components contains some components to install in learnbot robot.",
      author="Ivan Barbecho",
      author_email="ivanbd@unex.es",
      url="https://github.com/robocomp/learnbot/tree/version-2-component-pip",
      license="GPL",
      scripts=[
          'EBO_components/baserobot/src/baserobot.py',
          'EBO_components/camera/camera.py',
          'EBO_components/display/src/display.py',
          'EBO_components/emotionalMotor/src/emotionalMotor.py',
          'EBO_components/jointMotor/src/jointMotor.py',
          'EBO_components/laser/src/laser.py',
          'EBO_components/startComponents',
          ],
      packages=find_packages(where=".", exclude=['learnbot_dsl*']),
      include_package_data=True,
      package_data={'':["*"]},
      zip_safe=False,
      long_description=read('EBO_components/description.md'),
      long_description_content_type='text/markdown',
      python_requires='!=2.*, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, !=3.4.*, <4',
      install_requires=[
            'matplotlib==2.2.2',
            'epitran==0.4',
            'opencv_python_headless==3.4.3.18',
            'numpy==1.13.3',
            'Adafruit_PCA9685==1.0.1',
            'ice==0.0.2',
            'PySide==1.2.4',
            'EBO_components==0.0.3',
            'paho_mqtt==1.4.0',
            'picamera==1.13',
            'wiringpi==2.46.0',
            'wiringpi2'],
      )
if os.path.exists("build.EBO_components"):
    shutil.rmtree("build.EBO_components")
shutil.move("build", 'build.EBO_components')
