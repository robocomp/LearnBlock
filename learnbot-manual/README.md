# Learnbot 2.0 installation and assembly manual
## Raspberry Pi 3B+ and PiTFT display

The first step to install Learnbot is to connect the PiTFT screen using the pins 4 (5V),12(GPIO 18),15(GPIO 22),16(GPIO 23),17(3.3V),19(GPIO 10),20(GND),21(GPIO 9),22(GPIO 25),24(GPIO 8) which are the minimum necessary pins to operate the screen correctly.
![Connection scheme](https://github.com/brickbit/learnbot/blob/master/learnbot-manual/screen-raspberry.jpg "Connection scheme")
Then download the version of Raspbian Jessie that runs the screen from this [link](https://learn.adafruit.com/adafruit-pitft-3-dot-5-touch-screen-for-raspberry-pi/easy-install) in our computer and and transfer it to the micro-SD card using Etcher [download here](https://etcher.io/) in which we will only have to select the previously downloaded Raspbian img file, select the drive (the card) and click on flash. Now you have the micro-SD card ready to connect to Raspberry and load the OS correctly.


The next step is to turn on Raspberry and expand the file system for it, open a terminal(Cntrl+alt+t to open a terminal) and write:
  ```
  sudo raspi-config
  (expand filesystem)
  sudo reboot
  ```
  
Here are some necessary settings and some tips that will be needed to make learnbot work properly so if you have already made the assembly of Learnbot 2.0 you will realize that when you turn on the screen it shows everything 
in reverse so we will need to turn the screen 180 degrees for them to type in the terminal (Cntrl+alt+t to open a terminal):
```
sudo nano /boot/config.txt 
```
Locate the line in the file:
```
dtoverlay=pitft28r,rotate=90,speed=62000000,fps=25
```
And we replace _"rotate = 90"_ by _"rotate = 270"_ to rotate the screen 180 degrees. Press Cntrl + X, then Y and finally Enter to save and exit. 
This will ensure that the screen is displayed correctly.

It is very likely that during the installation of Learnbot2.0 you will want to use the HDMI port to view the contents on a 
larger screen so you should do the following:

Open a terminal(Cntrl+alt+t to open a terminal) and type:
```
sudo nano /usr/share/X11/xorg.conf.d/99-fbdev.conf
```
Now edit the empty file by typing the following:
```
Section "Device"
  Identifier "display"
  Driver "fbdev"
  Option "fbdev" "/dev/fb0"
EndSection
```
Change the Option "fbdev" "/dev/fb0" line to Option "fbdev" "/dev/fb1" if you want the xdisplay on the PiTFT
Press Cntrl + X, then Y and finally Enter to save and exit.
TIP:If you have connected to a screen for HDMI and there has been any problem that your Raspberry has been turned off or blocked it is likely that when you restart it does not turn on neither the screen connected by HDMI nor the PiTFT screen to solve it removes the micro card -SD of your Raspberry insert into your computer opens a terminal and writes the following:
```
cd /media/(here writes your username without parenthesis or press tab to see wich can be it)/(the SD card name, something like 402bfe3d-37db-48a7-a515-31edccf953df)
```
Resets the file that configures the screen
```
sudo nano /usr/share/X11/xorg.conf.d/99-fbdev.conf
```
Change 0 by 1
```
Section "Device"
  Identifier "display"
  Driver "fbdev"
  Option "fbdev" "/dev/fb0"
EndSection
```
## Get the Learnbot 2.0's emotions
To get the emotions you have to open a terminal and write:
```
git clone https://github.com/mhaut/learnbot-emotions.git
cd learnbot-emotions/tkinter/
python learnbotFace.py

```
We are still working on it

## Streaming Learnbot 2.0 camera
The first step is to connect and enable the Raspberry camera so  we open a terminal and write:
```
sudo raspi-config
```
We go down to the option _"5 Interfacing Options"_ with key-down and press Enter. Then select the option _"P1 Camera"_ pressing the key Enter and finally the raspi-configuation asks us "Would you like the camera interface to be enabled?", we select _"Yes"_ and press Enter and confirm the ok by pressing enter again.
Next we update our Raspberry by typing in the terminal:
```
sudo apt-get update
sudo apt-get dist-upgrade
```
Both commands take quite a while to finish.
We cloned the program code hosted on github
```
git clone https://github.com/silvanmelchior/RPi_Cam_Web_Interface.git
```
We go to the folder  _"RPi_Cam_Web_Interface"_ by typing:
```
cd RPi_Cam_Web_Interface
```
We install the program:
```
./install.sh
```
And finally we start the program
```
./start.sh
```
