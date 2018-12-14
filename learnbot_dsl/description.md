# learnbot-dsl

This project has been designed as a tool to learn different topics, like programing, logic, math, emotions, physic, robotic, ... 

The methodology used to teach this knowledges is the following:
The kids make programs, with a IDE (Learnblock) this programs and this programs control a smal robot (EBO).

## Learnblock

This program is the main.  It is here where the kids make his/her programs. This programs can be created with language similar to scratch, that is to say, using blocks.

## EBO 

EBO is a smal robot, that run some components that ofert interfaces to control it.

## How to Install learnbot-dsl?

For install learnbot-dsl first is necessary install some depencies:

### Step 1: Install Robocomp

For install robocomp you should do the steps descrip on here:

[https://github.com/robocomp/robocomp](https://github.com/robocomp/robocomp)

### Step 2: Install Apriltag

For install apriltag you should run the follow command:

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

For install learnbot-dsl you should run the follow command:

    sudo pip install learnbot-dsl
    
__Note__: If your PC is previous at 2011 and you can't run:

    emotionrecognition2.py
    
Yoy should change the version of **tensorflow** to 1.5 with:

    sudo pip install tensorflow==1.5