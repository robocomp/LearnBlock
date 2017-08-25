

#EXECUTION: python code_example.py config

global lbot
lbot = LearnBotClient.Client(sys.argv)

unidad = 1
max = 200
counter = 0
while counter < max:
	if functions.get("center_red_line")(lbot):
		functions.get("set_move")(lbot, 40, 0)
	elif functions.get("right_red_line")(lbot):
		functions.get("set_move")(lbot, 20, 0.2)
	elif functions.get("left_red_line")(lbot):
		functions.get("set_move")(lbot, 20, -0.2)
	else:
		functions.get("stop_bot")(lbot)
	counter += unidad
functions.get("stop_bot")(lbot)

