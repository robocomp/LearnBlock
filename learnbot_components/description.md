# learnbot_components

This project has been designed as a tool to learn different topics, like programing, logic, math, emotions, physic, robotic, ... 

The methodology used to teach this knowledges is the following:
The kids make programs, with a IDE (Learnblock) this programs and this programs control a smal robot (EBO).

## Learnblock

This program is the main.  It is here where the kids make his/her programs. This programs can be created with language similar to scratch, that is to say, using blocks.

## EBO 

EBO is a small robot, that run some components that offer interfaces to control it.

## How to Install learnbot_components?

For install learnbot_components first is necessary install some dependencies:

### Step 1: Install driver of motors

    cd ~
    git clone https://github.com/pololu/drv8835-motor-driver-rpi.git
    cd drv8835-motor-driver-rpi
    sudo python setup.py install

### Step 2: Install learnbot_components

    pip3 install learnbot_components


