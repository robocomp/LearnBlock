class setConfiguration:

	def setconfigPhysical(self, value, name):
		fileName = "etc/configPhysical" + name
		file = open(fileName,"w+")
		file.write("# Proxies for required interfaces\n")
		file.write("DifferentialRobotProxy = differentialrobot:tcp -h " + value[0] + " -p " + value[6] + "\n" )
		file.write("LaserProxy = laser:tcp -h " + value[0] + " -p " + value[7] + "\n" )
		file.write("EmotionalMotorProxy = emotionalmotor:tcp -h " + value[0] + " -p " + value[8] + "\n" )
		file.write("JointMotorProxy = jointmotor:tcp -h " + value[0] + " -p " + value[9] + "\n" )
		#file.write("UltrasoundProxy = ultrasound:tcp -h odroid.local -p %d\n\n\n" % port2 )
		file.write("# This property is used by the clients to connect to IceStorm.\n")
		file.write("#TopicManager.Proxy=IceStorm/TopicManager:default -p 9999\n\n\n")
		file.write("Ice.Warn.Connections=0 \nIce.Trace.Network=0\nIce.Trace.Protocol=0\nIce.ACM.Client=10 \nIce.ACM.Server=10\n")
		
	def setconfigSimulated(self,value,name):
		fileName = "etc/configSimulate" + name
		file = open(fileName,"w+")
		#file = open("configSimulated","w+")
		file.write("# Proxies for required interfaces\n")
		file.write("DifferentialRobotProxy = differentialrobot:tcp -h localhost -p " + value[6] + "\n")
		file.write("Laser1Proxy = laser:tcp -h localhost -p " + value[10] + "\n")
		file.write("Laser2Proxy = laser:tcp -h localhost -p " + value[11] + "\n")
		file.write("Laser3Proxy = laser:tcp -h localhost -p " + value[12] + "\n")
		file.write("Laser4Proxy = laser:tcp -h localhost -p " + value[13] + "\n")
		file.write("Laser5Proxy = laser:tcp -h localhost -p " + value[14] + "\n")
		file.write("Laser6Proxy = laser:tcp -h localhost -p " + value[15] + "\n")
		file.write("Laser7Proxy = laser:tcp -h localhost -p " + value[16] + "\n")
		file.write("RGBDProxy = rgbd:tcp -h localhost -p " + value[17] + "\n\n\n")
		file.write("DisplayProxy = display:tcp -h localhost -p " + value[18] + "\n\n\n")
		file.write("JointMotorProxy = jointmotor:tcp -h localhost -p " + value[9] + "\n\n\n")
		file.write("# This property is used by the clients to connect to IceStorm.\n")
		file.write("#TopicManager.Proxy=IceStorm/TopicManager:default -p 9999\n\n\n")
		file.write("Ice.Warn.Connections=0 \nIce.Trace.Network=0\nIce.Trace.Protocol=0\nIce.ACM.Client=10 \nIce.ACM.Server=10\n")
		
	def setconfig(self,value,name):
		filename = "etc/config" + name
		file = open(filename,"w+")
		file.write("#Configuration of connection\n")
		file.write("learnbot.ip = '" + value[0] + "'\n")
		file.write("learnbot.user = '" + value[1] + "'\n")
		file.write("learnbot.pass = '" + value[2] + "'\n")
		file.write("learnbot.command.start = '" + value[3] + "'\n")
		file.write("learnbot.command.stop = '" + value[4] + "'\n")
		file.write("learnbot.command.start_simulator = '" + value[5] + "'\n")
		
