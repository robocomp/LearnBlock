from __future__ import print_function, absolute_import

def stop_bot(lbot, params=None, verbose=False):
	lbot.setBaseSpeed(0,0)
	if verbose:
		print('~ Learnbot stopped')
