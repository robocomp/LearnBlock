

#EXECUTION: python code_example.py config

global lbot
lbot = LearnBotClient.Client(sys.argv)

main
functions.get("move_left")(lbot, [0])

