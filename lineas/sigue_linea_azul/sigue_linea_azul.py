            
def sigue_linea_azul():

    if robot.is_center_red_line():
        robot.move_straight()
    elif robot.is_right_red_line():
        robot.move_right()
    elif robot.is_left_red_line():
        robot.move_left()
    else:
        robot.stop_bot()

