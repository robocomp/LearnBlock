

#EXECUTION: python code_example.py config

global lbot
lbot = LearnBotClient.Client(sys.argv)

while True:
	if functions.get("center_red_line")(lbot):
		functions.get("set_move")(lbot, 40, 0)
	elif:
		functions.get("set_move")(lbot, 20, 0.2)
	elif:
		functions.get("set_move")(lbot, 20, -0.2)
	else:
		functions.get("stop_bot")(lbot)

