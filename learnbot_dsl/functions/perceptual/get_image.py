from __future__ import print_function, absolute_import

def get_image(lbot, params=None, verbose=False):
	frame = lbot.getImage()
	if verbose:
		print("Frame shape", frame.shape)
	return frame
