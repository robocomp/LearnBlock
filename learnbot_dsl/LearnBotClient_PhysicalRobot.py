#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys, traceback, Ice, os, apriltag, time, copy, threading, cv2
from collections import namedtuple
import numpy as np
import io
from PIL import Image
import paho.mqtt.client
ROBOCOMP = ''
try:
    ROBOCOMP = os.environ['ROBOCOMP']
except KeyError:
    print '$ROBOCOMP environment variable not set, using the default value /opt/robocomp'
    ROBOCOMP = '/opt/robocomp'

ICEs = ["Laser.ice", "DifferentialRobot.ice", "JointMotor.ice", "EmotionRecognition.ice", "EmotionalMotor.ice", "GenericBase.ice", "Apriltag.ice" ]

icePaths = []
try:
    SLICE_PATH = os.environ['SLICE_PATH'].split(':')
    for p in SLICE_PATH:
        icePaths.append(p)
    icePaths.append(os.path.join(ROBOCOMP, "interfaces"))
except:
    print 'SLICE_PATH environment variable was not exported. Using only the default paths'
    pass

for ice in ICEs:
    for p in icePaths:
        if os.path.isfile(os.path.join(p, ice)):
            wholeStr = ' -I' + p + " --all " + os.path.join(p, ice)
            Ice.loadSlice(wholeStr)
            break

import RoboCompLaser
import RoboCompDifferentialRobot
import RoboCompJointMotor
import RoboCompGenericBase
import RoboCompEmotionalMotor
import RoboCompEmotionRecognition
import RoboCompApriltag

import subprocess

import signal
signal.signal(signal.SIGINT, signal.SIG_DFL)

ic = None


# class MySignal(QtCore.QObject):
#     signalUpdateStreamer = QtCore.Signal(np.ndarray)

# signalCamera = None
open_cv_image = np.zeros((240,320,3), np.uint8)
newImage = False
def on_message(client, userdata, message):
    global open_cv_image, newImage
    newImage = True
    data = message.payload
    image_stream = io.BytesIO()
    image_stream.write(data)
    image = Image.open(image_stream)
    open_cv_image = np.array(image)
    open_cv_image = cv2.flip(open_cv_image, 0)

class Client(Ice.Application, threading.Thread):

    def __init__(self, argv):
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
        self.emotion_current_exist = False
        self.currents_emotions = []
        global ic
        params = copy.deepcopy(sys.argv)
        if len(params) > 1:
            if not params[1].startswith('--Ice.Config='):
                params[1] = '--Ice.Config=' + params[1]
        elif len(params) == 1:
            params.append('--Ice.Config=config')
        ic = Ice.initialize(params)

        print "iniciando componente emotionrecognition"
        # subprocess.Popen("python /home/robocomp/robocomp/components/learnbot/components/emotionrecognition2/src/emotionrecognition2.py /home/robocomp/robocomp/components/learnbot/components/emotionrecognition2/etc/config", shell=True, stdout=subprocess.PIPE)


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

            try:
                proxyString = ic.getProperties().getProperty('LaserProxy')
                try:
                    basePrx = ic.stringToProxy(proxyString)
                    self.laser_proxy = RoboCompLaser.LaserPrx.checkedCast(basePrx)
                    print "Connection Successful: ", proxyString
                except Ice.Exception:
                    print 'Cannot connect to the remote object (Laser)', proxyString
                    raise
            except Ice.Exception, e:
                print e
                print 'Cannot get Laser Proxy property.'
                raise



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
                print 'Cannot get JointMotor property.'
                raise

            # Remote object connection for EmotionRecognition
            try:
                proxyString = ic.getProperties().getProperty('EmotionRecognition')
                i = 0
                try:
                    while(True):
                        try:
                            i += 1
                            basePrx = ic.stringToProxy(proxyString)
                            self.emotionrecognition_proxy = RoboCompEmotionRecognition.EmotionRecognitionPrx.checkedCast(basePrx)
                            break
                        except Ice.Exception:
                            if i is 4:
                                raise
                            else:
                                print "try ", i
                                time.sleep(1.5)
                except Ice.Exception:
                    print 'Cannot connect to the remote object (EmotionRecognition)', proxyString
                    raise
            except Ice.Exception, e:
                print e
                print 'Cannot get EmotionRecognition property.'
                raise
            # Remote object connection for AprilTag
            try:
                proxyString = ic.getProperties().getProperty('ApriltagProxy')
                try:
                    basePrx = ic.stringToProxy(proxyString)
                    self.apriltagProxy = RoboCompApriltag.ApriltagPrx.checkedCast(basePrx)
                    print "Connection Successful: ", proxyString
                except Ice.Exception:
                    print 'Cannot connect to the remote object (Apriltag)', proxyString
                    raise
            except Ice.Exception, e:
                print e
                print 'Cannot get JointMotorPrx property.'
                raise
            try:
                # self.stream = urllib.urlopen('http://192.168.16.1:8080/?action=stream')

                # self.stream = urllib2.urlopen('http://192.168.16.1:8080/?action=stream',timeout=4)
                self.client = paho.mqtt.client.Client(client_id='learnbotClient', clean_session=False)
                # self.client.on_connect = on_connect
                self.client.on_message = on_message
                self.client.connect(host='192.168.16.1', port=50000)
                self.client.subscribe(topic='camara', qos=2)
                self.client.loop_start()
                self.count = 0
                self.startfps = time.time()

                self.streamOK = True
                print "Streamer iniciado correctamente"
            except Exception as e:
                print "Error connect Streamer\n", e
                self.streamOK = False
            self.bytes = ''

        except:
                traceback.print_exc()
                raise

        self.active = True
        self.apriltag_current_exist = True
        self._stop_event = threading.Event()
        self.listIDs = []
        self.start()

    def __detectAprilTags(self):
        if not self.apriltag_current_exist:
            frame = RoboCompApriltag.TImage()
            frame.width = self.image.shape[0]
            frame.height = self.image.shape[1]
            frame.depth = self.image.shape[2]
            frame.image = np.fromstring(self.image, np.uint8)
            aprils = self.apriltagProxy.processimage(frame)
            self.apriltag_current_exist = True
            self.listIDs = [a.id for a in aprils]

    def run(self):
        global open_cv_image,newImage
        while self.active:
            self.reading = True
            self.mutex.acquire()
            if self.streamOK and newImage:
                newImage=False
                self.getImageStream(open_cv_image)
            self.readSonars()
            self.mutex.release()
            self.reading = False
            time.sleep(0.002)

    def lookingLabel(self, id):
        self.__detectAprilTags()
        return id in self.listIDs

    def stop(self):
        self.client.disconnect()
        del self.client
        self._stop_event.set()

    def stopped(self):
        return self._stop_event.is_set()

    def getImageStream(self,image):
        self.image = image
        self.newImg = True
        self.emotion_current_exist = False
        self.apriltag_current_exist = False
        self.count += 1
        if self.count == 60:
            finish = time.time()
            if self.count / (finish - self.startfps) < 15:
                print '\033[91m' + str(self.count / (finish - self.startfps))[:5], "fps" + '\033[0m'
            else:
                print str(self.count / (finish - self.startfps))[:5], "fps"
                self.count = 0
            self.startfps = time.time()
        return True

    def readSonars(self):
        try:
            laserdata = self.laser_proxy.getLaserData()
            self.usList = [d.dist for d in laserdata]
        except Exception as e:
            print "Error readSonars"

    def getSonars(self):
        # self.readSonars()
        self.mutex.acquire()
        localUSList = self.usList
        self.mutex.release()
        # time.sleep(0.1)
        # print localUSList
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
            # print vAdvance, vRotation
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

    def expressNeutral(self):
        try:
            self.emotionalmotor_proxy.expressNeutral()
        except Exception as e:
            print e
            print "Error expressNeutral"

    def setJointAngle(self, angle):
        self.angleCamera = angle
        # print "Enviando anglulo", angle
        goal = RoboCompJointMotor.MotorGoalPosition()
        goal.name = 'servo'
        goal.position = angle
        self.jointmotor_proxy.setPosition(goal)

    def getEmotions(self):
        if not self.emotion_current_exist:
            frame = RoboCompEmotionRecognition.TImage()
            frame.width = self.image.shape[0]
            frame.height = self.image.shape[1]
            frame.depth = self.image.shape[2]
            frame.image = np.fromstring(self.image, np.uint8)
            self.currents_emotions = self.emotionrecognition_proxy.processimage(frame)
            self.emotion_current_exist = True
        return self.currents_emotions

    def __del__(self):
            self.active = False
