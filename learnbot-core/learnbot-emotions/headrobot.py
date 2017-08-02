#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function

class BaseHead(object):
	def __init__(self):
		self.colour = "blue"
		self.size = None

	def set_colour(self, colour):
		self.colour = colour

	def set_size(self, x0, y0, x1, y1):
		self.size = [x0, y0, x1, y1]

	def get_colour(self):
		return self.colour

	def get_size(self):
		return self.size

class Eye(BaseHead):
	def __init__(self):
		BaseHead.__init__(self)

class Pupil(FaceBase):
    def __init__(self):
        BaseHead.__init__(self)
        self.reflex = Pupil_reflex()

class Pupil_reflex(FaceBase):
    def __init__(self):
        BaseHead.__init__(self)

class EyeLid(BaseHead):
	def __init__(self):
		BaseHead.__init__(self)

class EyeBrow(BaseHead):
	def __init__(self):
		BaseHead.__init__(self)

class Mouth(BaseHead):
	def __init__(self):
		BaseHead.__init__(self)


class Face():
	def __init__(self):
		self.left_eye = Eye()
		self.right_eye = Eye()
		self.left_eyebrow = EyeBrow()
		self.right_eyebrow = EyeBrow()
		self.eyelids = None
		self.mouth = Mouth()

	def set_eye(self, eye, position):
		if position == "left":
			self.left_eye = eye
		elif position == "right":
			self.right_eye = eye
		else:
			print("ERROR: Position eye set")
			exit()

	def get_eye(self, position):
		if position == "left":
			return self.left_eye
		elif position == "right":
			return self.right_eye
		else:
			print("ERROR: Position eye get")
			exit()

	def set_eyebrow(self, eyebrow, position):
		if position == "left":
			self.left_eyebrow = eyebrow
		elif position == "right":
			self.right_eyebrow = eyebrow
		else:
			print("ERROR: Position eyebrow set")
			exit()

	def get_eyebrow(self, position):
		if position == "left":
			return self.left_eyebrow
		elif position == "right":
			return self.right_eyebrow
		else:
			print("ERROR: Position eyebrow get")
			exit()

	def set_eyelids(self, lu_eyeLid, ld_eyeLid, ru_eyeLid, rd_eyeLid):
		self.eyelids = [lu_eyeLid, ld_eyeLid, ru_eyeLid, rd_eyeLid]

	def get_eyelids(self):
		return self.eyelids
