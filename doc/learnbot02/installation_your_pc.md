
## Installation on your pc

For install all project you should follow this steps.

### Install OpenCv 3.4

    $ sudo git clone https://github.com/opencv/opencv_contrib.git
    $ sudo git clone https://github.com/opencv/opencv.git
    $ cd opencv_contrib
    $ git checkout 3.4.0
    $ cd ../opencv_contrib
    $ git checkout 3.4.0
    $ mkdir build
    $ cmake -D CMAKE_BUILD_TYPE=RELEASE \
      -D CMAKE_INSTALL_PREFIX=/usr/local \
      -D INSTALL_C_EXAMPLES=ON \
      -D INSTALL_PYTHON_EXAMPLES=ON \
      -D WITH_TBB=ON \
      -D WITH_V4L=ON \
      -D WITH_QT=ON \
      -D WITH_OPENGL=ON \
      -D OPENCV_EXTRA_MODULES_PATH=../../opencv_contrib/modules \
      -D BUILD_EXAMPLES=ON ..
    $ make -j<number of cores>
    $ sudo make install


### Install Robocomp

Learnbot's project use the simulator of Robocomp, thus you should install the project Robocomp, the branch highlyunstable

    https://github.com/robocomp/robocomp/tree/highlyunstable

### Install Learnbot

Clone this repository in the path /home/robocomp/robocomp/components/

    $ cd /home/robocomp/robocomp/components/
    $ git clone https://github.com/robocomp/learnbot
    $ git checkout emorobotic


This project has a IDE, which is being created as a facilitator environment, similar to Scrach.

You should install Learnbot project with the flollowing command:

    $ chmod +x setupLearnblock
    $ sudo ./setupLearnblock install
<!---
### Configuration for your pc

Grant execution permissions:

    $ chmod +x startLearnblock.sh

Edit the Learnblock.desktop file so that the path command was correct.   
-->
