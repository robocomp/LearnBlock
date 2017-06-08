import ast
import LearnBotClient as lbot

def get_distance(params=None):
	sonarsValue = ast.literal_eval(lbot.getSonars())
	return sonarsValue
