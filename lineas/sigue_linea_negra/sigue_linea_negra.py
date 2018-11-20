			
def sigue_linea_negra():

	if functions.get("center_black_line")(lbot) :
		functions.get("move_straight")(lbot)
	elif functions.get("right_black_line")(lbot) :
		functions.get("move_right")(lbot)
	elif functions.get("left_black_line")(lbot) :
		functions.get("move_left")(lbot)
	else:
		functions.get("slow_down")(lbot)


