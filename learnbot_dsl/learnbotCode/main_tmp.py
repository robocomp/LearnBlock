

#EXECUTION: python code_example.py config

global lbot
lbot = LearnBotClient.Client(sys.argv)

class User:
	def follow_red_line(self):
		if functions.get("center_red_line")(lbot):
			functions.get("set_move")(lbot, [40, 0])
		elif functions.get("left_red_line")(lbot):
			functions.get("set_move")(lbot, [20, 0.2])
		elif functions.get("right_red_line")(lbot):
			functions.get("set_move")(lbot, [20, -0.2])
		else:
			functions.get("stop_bot")(lbot)

while True:
	User().follow_red_line()

