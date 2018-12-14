

def up_camera(lbot,angle):
    angle = lbot.angleCamera + angle
    lbot.setJointAngle(angle)
