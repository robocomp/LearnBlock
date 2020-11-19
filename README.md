
[![Donate](https://img.shields.io/badge/Donate-PayPal-green.svg)](https://www.paypal.com/cgi-bin/webscr?cmd=_s-xclick&hosted_button_id=N3VAYG9VP8S4L)

---

[LearnBlock v 3.0](http://robocomp.org)
===============================
LearnBlock is an educational programming tool for learning programming. It has been designed to facilitate the learning process starting with a visual programming language and progressing towards a professional programming language.

LearnBlock is robot-agnostic, i.e. the same program can be executed in several robots. Clients for new robots can be easily created adding device interfaces and implementing hardware access methods for those interfaces. Examples of existing clients can be found [here](https://github.com/robocomp/LearnBlock/tree/version-3/learnbot_dsl/Clients)

# Main features

Among other features, LearnBlock includes the following:

* Available for different physical robots (EBO, Cozmo, Thymio and EV3) and simulated ones (EBO under RCIS and EV3 under V-REP).
* Robots can be programmed using different languages: visual language, Block-Text (textual representation of the visual language) and Python.
* New blocks can be created from code (Python) using the tool itself or external tools.
* A program can be run and stopped at any moment. When a program is interrupted the robot is properly stopped and disconnected. 
    

# Installation

LearnBlock can be installed from PyPi or from sources. To install the last release of LearnBlock, you can follow the steps described in [https://pypi.org/project/learnblock/](https://pypi.org/project/learnblock/)

If you want to install LearnBlock from sources, the following packages must be installed:

    sudo apt update

    sudo apt install python3-pip cmake python3-zeroc-ice libnss3 libxcomposite1 libxcursor1 libxi6 libxkbcommon0 libasound2

    sudo pip3 install apriltag requests pyunpack opencv-python-headless imutils six tensorflow dlib paramiko Pillow paho_mqtt PySide2 pyparsing qdarkstyle future

*cd* to your home directory and type:

    git clone https://github.com/robocomp/LearnBlock.git

Edit your ~/.bashrc file:

    gedit ~/.bashrc

Add these lines at the end:

    export PYTHONPATH="${PYTHONPATH}:~/LearnBlock"

Update the bash process by typing:

    source ~/.bashrc

Copy the following files to /usr/local/bin:

    sudo cp -p ~/LearnBlock/learnbot_dsl/learnbotCode/LearnBlock ~/LearnBlock/learnbot_dsl/components/apriltag/src/aprilTag.py ~/LearnBlock/learnbot_dsl/components/emotionrecognition2/src/emotionrecognition2.py /usr/local/bin

You can now start LearnBlock by typing *LearnBlock*

# Contributing
Thanks for your interest in contributing code!
If you find an error or some improvement, I'd appreciate you told me. Please, use [this template](https://github.com/robocomp/LearnBlock/blob/91275d466a7d4269f8451047b3928c9c65d3f363/PULL_REQUEST_TEMPLATE)

---------------------------------------------------------------------
Drop comments and ask questions in:

- https://groups.google.com/forum/?hl=es#!forum/robocomp-dev
- https://gitter.im/robocomp/robocomp

Please, report any bug to pilarb@unex.es



