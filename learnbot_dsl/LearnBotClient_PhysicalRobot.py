#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys, traceback, Ice, os, math, time, json, ast, copy, threading
import json
import cv2
import urllib
from collections import namedtuple
import numpy as np
import time

ROBOCOMP = ''
try:
    ROBOCOMP = os.environ['ROBOCOMP']
except KeyError:
    print '$ROBOCOMP environment variable not set, using the default value /opt/robocomp'
    ROBOCOMP = '/opt/robocomp'

preStr = "-I/opt/robocomp/interfaces/ -I"+ROBOCOMP+"/interfaces/ --all /opt/robocomp/interfaces/"

Ice.loadSlice(preStr+"Ultrasound.ice")
Ice.loadSlice(preStr+"Laser.ice")
Ice.loadSlice(preStr+"DifferentialRobot.ice")
Ice.loadSlice(preStr+"JointMotor.ice")
Ice.loadSlice(preStr+"GenericBase.ice")
Ice.loadSlice(preStr+"EmotionalMotor.ice")


import RoboCompUltrasound
import RoboCompLaser
import RoboCompDifferentialRobot
import RoboCompJointMotor
import RoboCompGenericBase
import RoboCompEmotionalMotor


import signal
signal.signal(signal.SIGINT, signal.SIG_DFL)

ic = None



class Client(Ice.Application, threading.Thread):

    def __init__(self, argv,name):
        threading.Thread.__init__(self)

        self.mutex = threading.Lock()
        self.newImg = False
        self.reading = False

        self.adv = 0
        self.rot = 0
        self.max_rot= 0.4
        self.image = np.zeros((240,320,3), np.uint8)
        self.simage = self.image
        self.usList = [1000]*7
        self.angleCamera = 0
        self.message = "Not Updated"
        self.name = name
        global ic
        params = copy.deepcopy(sys.argv)
        if len(params) > 1:
            if not params[1].startswith('--Ice.Config='):
                params[1] = '--Ice.Config=' + params[1]
        elif len(params) == 1:
            params.append('--Ice.Config=config')
        ic = Ice.initialize(params)


        status = 0
        try:

            # Remote object connection for DifferentialRobot
            try:
                proxyString = ic.getProperties().getProperty('DifferentialRobotProxy')
                try:
                    basePrx = ic.stringToProxy(proxyString)
                    self.differentialrobot_proxy = RoboCompDifferentialRobot.DifferentialRobotPrx.checkedCast(basePrx)
                    print "Connection Successful: ", proxyString
                except Ice.Exception:
                    print 'Cannot connect to the remote object (DifferentialRobot)', proxyString
                    raise
            except Ice.Exception, e:
                print e
                print 'Cannot get DifferentialRobotProxy property.'
                raise

            # try:
            #     proxyString = ic.getProperties().getProperty('LaserProxy')
            #     try:
            #         basePrx = ic.stringToProxy(proxyString)
            #         self.laser_proxy = RoboCompLaser.LaserPrx.checkedCast(basePrx)
            #         print "Connection Successful: ", proxyString
            #     except Ice.Exception:
            #         print 'Cannot connect to the remote object (Laser)', proxyString
            #         raise
            # except Ice.Exception, e:
            #     print e
            #     print 'Cannot get Laser', i, 'Proxy property.'
            #     raise



            # Remote object connection for EmotionalMotor
            try:
                proxyString = ic.getProperties().getProperty('EmotionalMotorProxy')
                try:
                    basePrx = ic.stringToProxy(proxyString)
                    self.emotionalmotor_proxy = RoboCompEmotionalMotor.EmotionalMotorPrx.checkedCast(basePrx)
                    print "Connection Successful: ", proxyString
                except Ice.Exception:
                    print 'Cannot connect to the remote object (EmotionalMotor)', proxyString
                    raise
            except Ice.Exception, e:
                print e
                print 'Cannot get EmotionalMotor property.'
                raise

            # Remote object connection for JointMotor
            try:
                proxyString = ic.getProperties().getProperty('JointMotorProxy')
                try:
                    basePrx = ic.stringToProxy(proxyString)
                    self.jointmotor_proxy = RoboCompJointMotor.JointMotorPrx.checkedCast(basePrx)
                except Ice.Exception:
                    print 'Cannot connect to the remote object (JointMotor)', proxyString
                    raise
            except Ice.Exception, e:
                print e
                print 'Cannot get UltrasoundProxy property.'
                raise

            self.stream = urllib.urlopen('http://192.168.16.1:8080/?action=stream')
            self.bytes=''

        except:
                traceback.print_exc()
                raise
        				
	if (self.name == "Robot 1"):
     			broker="iot.eclipse.org"
			port=1883
			self.client = paho.Client("Robot1")                           #create client object
			#self.client.on_publish = self.on_publish                          #assign function to callback
			self.client.connect(broker,port)                                 #establish connection   
				
	else:
			self.client = mqtt.Client()
			#self.client.on_connect = self.on_connect
			#self.client.on_message = self.on_message
			self.client.connect("iot.eclipse.org", 1883)


        self.active = True
        self.start()

    def run(self):
        while self.active:
            self.reading = True
            self.mutex.acquire()
            self.getImageStream()
            # self.readSonars()
            self.mutex.release()
            self.reading = False
            time.sleep(0.002)

    def getImageStream(self):
        self.bytes += self.stream.read(5120)
        a = self.bytes.find('\xff\xd8')
        b = self.bytes.find('\xff\xd9')
        if a!=-1 and b!=-1:
            jpg = self.bytes[a:b+2]
            self.bytes = self.bytes[b+2:]
            image = cv2.imdecode(np.fromstring(jpg, dtype=np.uint8), cv2.IMREAD_COLOR)
            try:
                tempimage = cv2.cvtColor(image,cv2.COLOR_BGR2RGB)
                image = cv2.flip(tempimage, 0)
            except:
                print "Error retrieving images!"
                return None
            # self.mutex.acquire()
            self.image = image
            self.newImg = True
            # self.mutex.release()
        return True

    def readSonars(self):
        try:
            laserdata = ast.literal_eval(self.laser_proxy.getLaserData())
            self.usList = [d.dist for d in laserdata]
            # for nombre, sensor in ultrasound.items():
            #     if (nombre == "sensor0"):
            #         self.usList["front"] = sensor["dist"]*10
            #     elif (nombre == "sensor1"):
            #         self.usList["back"] = sensor["dist"]*10
            #     elif (nombre == "sensor2"):
            #         self.usList["right"] = sensor["dist"]*10
            #     elif (nombre == "sensor3"):
            #         self.usList["left"] = sensor["dist"]*10
        except Exception as e:
            print "Error readSonars"

    def getSonars(self):
        # self.readSonars()
        while self.reading:
            time.sleep(0.005)
        self.mutex.acquire()
        localUSList = self.usList
        print self.usList
        self.mutex.release()
        # time.sleep(0.1)
        return localUSList

    def getImage(self):
        while self.reading:
            time.sleep(0.005)
        self.mutex.acquire()
        # if self.newImg:
        self.simage = self.image
        self.newImg = False
        self.mutex.release()

        # time.sleep(0.05)
        return self.simage

    def getPose(self):
        try:
            x, y, alpha = self.differentialrobot_proxy.getBasePose()
            return x, y, alpha
        except Exception as e:
            print "Error getPose"

    def setAngleJointMotor(self, angle):
        try:
            goal = RoboCompJointMotor.MotorGoalPosition()
            goal.position = -angle
            self.jointmotor_proxy.setPosition(goal)
        except Exception as e:
            print "Error setAngleJointMotor\n",e, type(angle)

    def setRobotSpeed(self, vAdvance=0, vRotation=0):
        try:
            print vAdvance, vRotation
            # if vAdvance!=0 or vRotation!=0:ll
            self.adv = vAdvance
            self.rot = vRotation
            self.differentialrobot_proxy.setSpeedBase(-self.adv*8,self.rot*15)
        except Exception as e:
            print "Error setRobotSpeed"

    def expressJoy(self):
        try:
            self.emotionalmotor_proxy.expressJoy()
        except Exception as e:
            print "Error expressJoy"

    def expressSadness(self):
        try:
            self.emotionalmotor_proxy.expressSadness()
        except Exception as e:
            print "Error expressSadness"

    def expressSurprise(self):
        try:
            self.emotionalmotor_proxy.expressSurprise()
        except Exception as e:
            print "Error expressSurprise"

    def expressFear(self):
        try:
            self.emotionalmotor_proxy.expressFear()
        except Exception as e:
            print "Error expressFear"

    def expressAnger(self):
        try:
            self.emotionalmotor_proxy.expressAnger()
        except Exception as e:
            print "Error expressAnger"

    def expressDisgust(self):
        try:
            self.emotionalmotor_proxy.expressDisgust()
        except Exception as e:
            print "Error expressDisgust"

    def setJointAngle(self, angle):
        self.angleCamera = angle
        print "Enviando anglulo", angle
        goal = RoboCompJointMotor.MotorGoalPosition()
        goal.name = 'servo'
        goal.position = angle
        self.jointmotor_proxy.setPosition(goal)

    def __del__(self):
            self.active = False

    def publish_topic(self,State):
		msg = self.name + State
		self.client.publish("Robot",msg)
		
    #def subscribe_topic(self,Robot):
	#	self.client.subscribe("Robot")

    def on_publish(client,userdata,result):             #create function for callback
	    print("data published \n")
	    pass
        
    def on_connect(client, userdata, flags, rc):
            print("Connected with result code "+str(rc))
            self.client.subscribe("Robot")
            
    def on_message(client, userdata, msg):
            print(msg.topic+" "+str(msg.payload))
            self.message = msg.payload
            
            
    def subscribe_topic(self,name, timeWait):
    	startTime = time.time()
	waitTime = timeWait
	name = name + " "
	while True:
        	self.client.loop()
        	elapsedTime = time.time() - startTime
        	if elapsedTime > waitTime:
        	        self.client.disconnect()
        	        return "Not Found"
        	        break
        	        
    		if name in self.message:
    			msg = self.message.replace(name,'')
    			return msg
    	  
        
        
