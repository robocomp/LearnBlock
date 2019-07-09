

def down_arm(lbot, angle):
    angle = lbot.angleArm + angle
    lbot.setJointAngle("ARM", angle)
