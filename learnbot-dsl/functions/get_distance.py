import ast

def get_distance(params=None):
	sonarsValue = ast.literal_eval(lbot.getSonars())
	return sonarsValue
