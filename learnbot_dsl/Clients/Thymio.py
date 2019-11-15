from learnbot_dsl.Clients.Client import *
from learnbot_dsl.Clients.Devices import *
from learnbot_dsl.functions import getFuntions
import dbus, dbus.mainloop.glib
from gi.repository import GObject
import math, traceback, sys, tempfile, os
from threading import Event

K = 3
L = 95


def valmap(value, istart, istop, ostart, ostop):
    return ostart + (ostop - ostart) * ((value - istart) / (istop - istart))


thymiohandlers = """
<!DOCTYPE aesl-source>
<network>


<!--list of global events-->
<event size="3" name="SetLEDsTop"/>
<event size="8" name="SetLEDsCircle"/>
<event size="4" name="SetLEDsButtons"/>
<event size="8" name="SetLEDsProxH"/>
<event size="2" name="SetLEDsProxV"/>
<event size="1" name="SetLEDsRC"/>
<event size="3" name="SetLEDsBottomLeft"/>
<event size="3" name="SetLEDsBottomRight"/>
<event size="2" name="SetLEDsTemperature"/>
<event size="1" name="SetLEDsSound"/>
<event size="1" name="SetSoundSystem"/>
<event size="2" name="SetSoundFreq"/>
<event size="1" name="SetSoundPlay"/>
<event size="1" name="SetSoundReplay"/>


<!--list of constants-->


<!--show keywords state-->
<keywords flag="true"/>


<!--node thymio-II-->
<node nodeId="65082" name="thymio-II">

onevent SetLEDsTop
call leds.top(event.args[0], event.args[1], event.args[2])

onevent SetLEDsCircle
call leds.circle(event.args[0], event.args[1], event.args[2], event.args[3], event.args[4], event.args[5], event.args[6], event.args[7])

onevent SetLEDsButtons
call leds.buttons(event.args[0], event.args[1], event.args[2], event.args[3])

onevent SetLEDsProxH
call leds.prox.h(event.args[0], event.args[1], event.args[2], event.args[3], event.args[4], event.args[5], event.args[6], event.args[7])

onevent SetLEDsProxV
call leds.prox.v(event.args[0], event.args[1])

onevent SetLEDsRC
call leds.rc(event.args[0])

onevent SetLEDsBottomLeft
call leds.bottom.left(event.args[0], event.args[1], event.args[2])

onevent SetLEDsBottomRight
call leds.bottom.right(event.args[0], event.args[1], event.args[2])

onevent SetLEDsTemperature
call leds.temperature(event.args[0], event.args[1])

onevent SetLEDsSound
call leds.sound(event.args[0])

onevent SetSoundSystem
call sound.system(event.args[0])

onevent SetSoundFreq
call sound.system(event.args[0])

onevent SetSoundPlay
call sound.play(event.args[0])

onevent SetSoundReplay
call sound.replay(event.args[0])


</node>


</network>"""
listfile = [f for f in os.listdir(tempfile.gettempdir()) if f.endswith("_thymiohandlers.aesl")]
if len(listfile) == 0:

    with tempfile.NamedTemporaryFile(suffix="_thymiohandlers.aesl", delete=False) as temp:
        name_thymiohandlers = temp.name
        with open(temp.name, "w") as t:
            t.write(thymiohandlers)
else:
    name_thymiohandlers = os.path.join(tempfile.gettempdir(), listfile[0])

print("Name of the file is:", name_thymiohandlers)


# addFunctions(getFuntions())

class Robot(Client):

    def __init__(self):
        Client.__init__(self, _miliseconds=100)
        self.lastCommand = False
        self.t = Thread(target=self.connectToRobot).start()
        self.addDistanceSensors(DistanceSensors(_readFunction=self.deviceReadLaser))
        self.addGroundSensors(GroundSensors(_readFunction=self.deviceReadGroundSensors))
        self.addBase(Base(_callFunction=self.deviceBaseMove))
        self.addAcelerometer(Acelerometer(_readFunction=self.deviceReadAcelerometer))
        self.addDisplay(Display(_setEmotion=self.deviceSendEmotion, _setImage=None))
        self.motorSpeed = [0, 0]
        self.prox = [0, 0, 0, 0, 0, 0, 0]
        self.prox_ground = [0, 0, 0]
        self.acc = [0, 0, 0]
        self.currentMotorSpeed = [-1, -1]
        self.event = Event()
        self.event.wait()
        self.currentEmotion = Emotions.NoneEmotion
        self.newEmotion = Emotions.NoneEmotion
        self.start()

    def connectToRobot(self):
        t = dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)
        bus = dbus.SessionBus()
        try:
            self.network = dbus.Interface(bus.get_object('ch.epfl.mobots.Aseba', '/'),
                                          dbus_interface='ch.epfl.mobots.AsebaNetwork')
        except Exception as e:
            raise Exception("Connection to thymio failed")
        node = self.network.GetNodesList()
        self.network.LoadScripts(name_thymiohandlers)
        self.loop = GObject.MainLoop()
        handle = GObject.timeout_add(100, self.comunicateRobot)
        self.event.set()
        self.loop.run()

    def comunicateRobot(self):
        try:
            self.network.GetVariable("thymio-II", "prox.horizontal", reply_handler=self.get_prox_horizontal_reply,
                                     error_handler=self.get_variables_error)
            self.network.GetVariable("thymio-II", "prox.ground.delta", reply_handler=self.get_prox_ground_reply,
                                     error_handler=self.get_variables_error)
            self.network.GetVariable("thymio-II", "acc", reply_handler=self.get_acelerometer_reply,
                                     error_handler=self.get_variables_error)
            if self.currentMotorSpeed[0] != self.motorSpeed[0]:
                self.network.SetVariable("thymio-II", "motor.left.target", [self.motorSpeed[0]])
                self.currentMotorSpeed[0] = self.motorSpeed[0]
            if self.currentMotorSpeed[1] != self.motorSpeed[1]:
                self.network.SetVariable("thymio-II", "motor.right.target", [self.motorSpeed[1]])
                self.currentMotorSpeed[1] = self.motorSpeed[1]
            if self.currentEmotion is not self.newEmotion:
                self.currentEmotion = self.newEmotion
                if self.newEmotion is Emotions.Joy:
                    self.send_event_name('SetLEDsTop', [0, 255, 0])
                    self.send_event_name('SetLEDsBottomLeft', [0, 255, 0])
                    self.send_event_name('SetLEDsBottomRight', [0, 255, 0])
                elif self.newEmotion is Emotions.Sadness:
                    self.send_event_name('SetLEDsTop', [0, 0, 255])
                    self.send_event_name('SetLEDsBottomLeft', [0, 0, 255])
                    self.send_event_name('SetLEDsBottomRight', [0, 0, 255])
                elif self.newEmotion is Emotions.Surprise:
                    self.send_event_name('SetLEDsTop', [255, 166, 0])
                    self.send_event_name('SetLEDsBottomLeft', [255, 166, 0])
                    self.send_event_name('SetLEDsBottomRight', [255, 166, 0])
                elif self.newEmotion is Emotions.Disgust:
                    self.send_event_name('SetLEDsTop', [0, 162, 0])
                    self.send_event_name('SetLEDsBottomLeft', [0, 162, 0])
                    self.send_event_name('SetLEDsBottomRight', [0, 162, 0])
                elif self.newEmotion is Emotions.Anger:
                    self.send_event_name('SetLEDsTop', [255, 0, 0])
                    self.send_event_name('SetLEDsBottomLeft', [255, 0, 0])
                    self.send_event_name('SetLEDsBottomRight', [255, 0, 0])
                elif self.newEmotion is Emotions.Fear:
                    self.send_event_name('SetLEDsTop', [124, 0, 255])
                    self.send_event_name('SetLEDsBottomLeft', [124, 0, 255])
                    self.send_event_name('SetLEDsBottomRight', [124, 0, 255])
                elif self.newEmotion is Emotions.Neutral:
                    self.send_event_name('SetLEDsTop', [0, 0, 0])
                    self.send_event_name('SetLEDsBottomLeft', [0, 0, 0])
                    self.send_event_name('SetLEDsBottomRight', [0, 0, 0])
            if self.lastCommand:
                self.loop.quit()
        except Exception as e:
            traceback.print_exc()
        return True

    def send_event_name(self, event_name, event_args):
        self.network.SendEventName(event_name, event_args,
                                   reply_handler=self.dbus_reply,
                                   error_handler=self.dbus_error)

    def dbus_reply(self):
        pass

    def dbus_error(self, e):
        print('error:')
        print(str(e))

    def disconnect(self):
        self.deviceBaseMove(0,0)
        self.lastCommand = True

    def get_prox_horizontal_reply(self, r):
        self.prox = r

    def get_prox_ground_reply(self, r):
        self.prox_ground = r
#        print(self.prox_ground[0], self.prox_ground[1])

    def get_acelerometer_reply(self, r):
        self.acc = r

    def get_variables_error(self, e):
        print('error:')
        print(str(e))

    def deviceReadAcelerometer(self):
        return self.acc

    def deviceBaseMove(self, SAdv, SRot):
        SRot_rad = math.radians(SRot)
        if SRot != 0.:
            #Rrot = SAdv / math.tan(SRot)
            Rrot = SAdv / SRot_rad

            Rl = Rrot - (L / 2)
            r_wheel_speed = SRot_rad * Rl * K

            Rr = Rrot + (L / 2)
            l_wheel_speed = SRot_rad * Rr * K
        else:
            l_wheel_speed = SAdv * K
            r_wheel_speed = SAdv * K
        self.motorSpeed = [l_wheel_speed, r_wheel_speed]

    def deviceReadLaser(self):
        p = [valmap(x, 0., 4230., 100., 0.) for x in self.prox]
        return {"front": p[1:4],  # The values must be in mm
                "left": p[:2],
                "right": p[3:5],
                "back": p[5:7]}

    def deviceReadGroundSensors(self):
        p = [self.prox_ground[0]//10, self.prox_ground[1]//10]  #range between 0 and 100
        return {"left": p[0],
                "right": p[1]}


    def deviceSendEmotion(self, _emotion):
        self.newEmotion = _emotion

#    def getColor(self):
#        print("sensor 0", self.prox_ground[0], "sensor 1", self.prox_ground[1])
#        return self.prox_ground

if __name__ == '__main__':
    try:
        robot = Robot()
    except Exception as e:
        print("hay un Error")
        traceback.print_exc()
        raise (e)
    print(dir(robot))
    time_global_start = time.time()

    robot.stop_bot()


    def elapsedTime(umbral):
        global time_global_start
        time_global = time.time() - time_global_start
        return time_global > umbral

    # try:
    #     while True:
    #
    #         if robot.front_obstacle(50):
    #             robot.stop_bot()
    #         else:
    #             robot.move_straight()
    #         print("bucle")
    # finally:
    #     print("quit")
