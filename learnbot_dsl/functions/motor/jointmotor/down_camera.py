

def down_camera(lbot,angle):
    angle = lbot.angleCamera + angle
    lbot.setJointAngle("CAMERA", angle)
