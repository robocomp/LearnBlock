			
def sigue_linea_azul():

	if functions.get("center_blue_line")(lbot) :
		functions.get("move_straight")(lbot)
	elif functions.get("right_blue_line")(lbot) :
		functions.get("move_right")(lbot)
	elif functions.get("left_blue_line")(lbot) :
		functions.get("move_left")(lbot)
	else:
		functions.get("slow_down")(lbot)


