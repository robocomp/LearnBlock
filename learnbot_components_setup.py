from setuptools import setup, find_packages
import os,sys, shutil
def read(fname):
      with open(os.path.join(os.path.dirname(__file__), fname)) as f:
            return f.read()
setup(name="learnbot_components",
    version=read('version'),
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
    packages=find_packages(where=".", exclude=['learnbot_dsl*']),
    include_package_data=True,
    package_data={'':["*"]},
    zip_safe=False,
    long_description=read('learnbot_components/description.md'),
    long_description_content_type='text/markdown',
    python_requires='!=2.*, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, !=3.4.*, <4',
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
if os.path.exists("build.learnbot_components"):
    shutil.rmtree("build.learnbot_components")
shutil.move("build", 'build.learnbot_components')