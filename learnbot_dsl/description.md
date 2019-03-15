[![Donate](https://img.shields.io/badge/Donate-PayPal-green.svg)](https://www.paypal.com/donate/?token=kY7sGShfBszy9Ncwd-H5ltsagLnyGPNl2n8zdwadOdUZomsU9XuaC7d6u0BNk--QqmyJJ0&country.x=ES&locale.x=ES)
---

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

For install learnbot-dsl you should run the follow command:

    sudo pip install learnbot-dsl
    
__Note__: If your PC is previous at 2011 and you can't run:

    emotionrecognition2.py
    
Yoy should change the version of **tensorflow** to 1.5 with:

    sudo pip install tensorflow==1.5
    

<form action="https://www.paypal.com/cgi-bin/webscr" method="post" target="_top">
<input type="hidden" name="cmd" value="_s-xclick" />
<input type="hidden" name="hosted_button_id" value="N3VAYG9VP8S4L" />
<input type="image" src="https://www.paypalobjects.com/es_ES/ES/i/btn/btn_donateCC_LG.gif" border="0" name="submit" title="PayPal - The safer, easier way to pay online!" alt="Donate with PayPal button" />
<img alt="" border="0" src="https://www.paypal.com/es_ES/i/scr/pixel.gif" width="1" height="1" />
</form>
