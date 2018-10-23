from setuptools import setup, find_packages
import os

def read(fname):
      with open(os.path.join(os.path.dirname(__file__), fname)) as f:
            return f.read()
exclude=[]

setup(name="learnbot_components",
      version="0.0.3",
      description="learnbot_components contains some components to install in learnbot robot.",
      author="Ivan Barbecho",
      author_email="ivanbd@unex.es",
      url="https://github.com/robocomp/learnbot/tree/version-2-component-pip",
      license="GPL",
      scripts=[
            'learnbot_components/baserobot/src/baserobot.py',
            'learnbot_components/camera/camera.py',
            'learnbot_components/display/src/display.py',
            'learnbot_components/emotionalMotor/src/emotionalMotor.py',
            'learnbot_components/jointMotor/src/jointMotor.py',
            'learnbot_components/laser/src/laser.py',
            ],
      packages=find_packages(exclude=exclude),
      include_package_data=True,
      package_data={'':["*"]},
      zip_safe=False,
      long_description=read('learnbot_components/description.md'),
      long_description_content_type='text/markdown',
      install_requires=[
            'matplotlib==2.2.2',
            'opencv_python_headless==3.4.3.18',
            'scipy==1.0.0',
            'tensorflow==1.10.1',
            'pandas==0.19.1',
            'Keras==2.0.5',
            'h5py==2.7.0',
            'epitran==0.4',
            'numpy==1.13.3',
            'Adafruit-PCA9685==1.0.1',
            'ice==0.0.2',
            'PySide==1.2.4',
            'paho_mqtt==1.4.0',
            'picamera==1.13',
            'wiringpi==2.46.0',
            'wiringpi2==2.32.3'],
      )
