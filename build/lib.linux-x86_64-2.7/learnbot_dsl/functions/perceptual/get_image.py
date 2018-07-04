from __future__ import print_function

def get_image(lbot, params=None, verbose=False):
	frame = lbot.getImage()
	lbot.publish_topic("get_image")
	if verbose:
		print("Frame shape", frame.shape)
	return frame
