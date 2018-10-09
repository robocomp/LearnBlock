			
def sigue_linea_roja():

	if functions.get("center_red_line")(lbot) :
		functions.get("move_straight")(lbot)
	elif functions.get("left_red_line")(lbot) :
		functions.get("move_left")(lbot)
	elif functions.get("right_red_line")(lbot) :
		functions.get("move_right")(lbot)
	else:
		functions.get("slow_down")(lbot)


