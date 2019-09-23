[![Donate](https://img.shields.io/badge/Donate-PayPal-green.svg)](https://www.paypal.com/cgi-bin/webscr?cmd=_s-xclick&hosted_button_id=N3VAYG9VP8S4L)
---

# learnbot-dsl

This project has been designed as a set of tools for education to learn different topics like programing, logic, math, emotions, physic, robotic, ... 

The project include the following tools:

- A robot (EBO) capable of exhibiting not only motor behaviours, but also emotional ones.

- A programming tool (LearnBlock) where the user can create and run programs using visual and textual programming languages.

- A simulator that allows the user to run the programs when the physical robot is not available. 


## Learnblock

Learnblock is the main component of learnbot-dsl. It is a programming tool created to teach programming concepts to children using visual and textual programming languages. Among other features, Learnblock includes the following:

- Avalaible for different robot (EBO, Cozmo, Thymio and EV3) and easily to adapt to other robots.
- Robots can be programmed using different languages: visual language, Block-Text (textual representation of the visual language) and Python.
- New blocks and functions can be created from the tool itself or using external tools.
- A program can be run and stopped at any moment using different options.
- A visual program is translated to a Python code that can work well in different robots sharing common features.

## EBO 

EBO is an educational robot created by RoboLab to help children to learn programming concepts. EBO can exhibit not only motor behaviors, but also emotional ones, which makes it an interesting tool for the design of activities related to emotional management.

## How to Install learnbot-dsl?

To install learnbot-dsl it is necessary to firstly install some depencies:

### Step 1: Install Robocomp (only if you want to use the EBO simulator)

For install robocomp you should do the steps descrip on here:

[https://github.com/robocomp/robocomp](https://github.com/robocomp/robocomp)

### Step 2: Install Apriltag

For installing apriltag you should run the following command:
    
    pip install apriltag
    
or

    git clone https://github.com/ibarbech/apriltag
    cd apriltag
    mkdir build
    cd build
    cmake ..
    make -j4
    sudo make install
    cd ..
    cd python
    sudo python setup.py install

### Step 3: Install learnbot-dsl

learnbot-dsl can be easily installed by running the following command:

    sudo pip install learnbot-dsl
    
__Note__: If your PC is previous to 2011 and you can't run:

    emotionrecognition2.py
    
Yoy should change the version of **tensorflow** to 1.5 with:

    sudo pip install tensorflow==1.5
    

