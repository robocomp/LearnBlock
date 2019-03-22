            
def sigue_linea_negra():

    if robot.is_center_black_line():
        robot.move_straight()
    elif robot.is_right_black_line():
        robot.move_right()
    elif robot.is_left_black_line():
        robot.move_left()
    else:
        robot.stop_bot()

