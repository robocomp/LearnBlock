						
def tags_a_emociones():

	if functions.get("seeing_the_tag")(lbot, 0) :
		functions.get("expressJoy")(lbot)
	elif functions.get("seeing_the_tag")(lbot, 1) :
		functions.get("expressFear")(lbot)
	elif functions.get("seeing_the_tag")(lbot, 2) :
		functions.get("expressSadness")(lbot)
	elif functions.get("seeing_the_tag")(lbot, 3) :
		functions.get("expressAnger")(lbot)
	elif functions.get("seeing_the_tag")(lbot, 4) :
		functions.get("expressDisgust")(lbot)
	elif functions.get("seeing_the_tag")(lbot, 5) :
		functions.get("expressSurprise")(lbot)
	else:
		functions.get("expressNeutral")(lbot)


