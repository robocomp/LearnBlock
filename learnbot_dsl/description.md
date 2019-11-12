[![Donate](https://img.shields.io/badge/Donate-PayPal-green.svg)](https://www.paypal.com/cgi-bin/webscr?cmd=_s-xclick&hosted_button_id=N3VAYG9VP8S4L)
---

# LearnBlock

LearnBlock is an educational programming tool for programming learning. It has been designed to facilitate the learning process starting with a visual programming language and progressing towards a professional programming language. 

LearnBlock is robot-agnostic, i.e. the same program can be executed in several robots. Clients for new robots can be easily created adding device interfaces and implementing hardware access methods for those interfaces. Examples of existing clients can be found [here](https://github.com/robocomp/LearnBlock/tree/version-3/learnbot_dsl/Clients)

## Main features

Among other features, Learnblock includes the following:

- Available for different physical robots (EBO, Cozmo, Thymio and EV3) and simulated ones (EBO under RCIS and EV3 under V-REP).
- Robots can be programmed using different languages: visual language, Block-Text (textual representation of the visual language) and Python.
- New blocks can be created from code using the tool itself or external tools.
- A program can be run and stopped at any moment. When a program is interrupted, the robot is properly stopped and disconnected.

## Installation

To use all the features of LearnBlock, you will need to install additional software by executing the following command:

    sudo apt-get install python-zeroc-ice
    
Then, you can easily install LearnBlock by running the following command:

    sudo pip install learnbot-dsl
    

